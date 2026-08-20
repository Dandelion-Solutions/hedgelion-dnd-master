# Step 5.6 — Campaign Publication & Crash Consistency — Analytical Challenge

Status: **ANALYTICAL CHALLENGE — NOT CANONICAL**

Date: 2026-08-20

Challenges:

- `2026-08-20-step-5-6-campaign-publication-crash-consistency-task-brief.md`
- `2026-08-20-step-5-6-campaign-publication-crash-consistency-research-draft.md`

Preliminary verdict:

> **PASS WITH MATERIAL TECHNICAL REFINEMENTS; NO NEW OWNER-LEVEL PRODUCT DECISION FOUND**

The recommended **PYTHON-OWNED SINGLE-REF CAS PUBLICATION** direction survives challenge. Several details must be tightened before canonicalization.

---

# 1. Challenge — does one tree/commit really give campaign atomicity?

## Attack

GitHub still receives multiple object-creation requests before the branch update. A crash can occur after some blobs/tree/commit objects exist.

Therefore calling the whole operation "atomic" could be misleading.

## Finding

Distinguish **object preparation atomicity** from **authoritative publication atomicity**.

The operation is not one network transaction. It is nevertheless authority-atomic for one campaign ref because prepared objects are not selected current campaign state.

Canonical wording should be:

> Maximal single-ref authority atomicity: all changed paths are prepared into one resulting tree and one single-parent commit; the old campaign ref remains authoritative until one non-force ref transition selects the complete new commit.

Prepared/unreachable objects are non-authoritative garbage, not partial campaign canon.

**Disposition: refinement, direction retained.**

---

# 2. Challenge — can `force=false` substitute for true expected-SHA CAS?

## Attack

GitHub's ref update API takes target SHA + `force=false`; it does not require the caller to submit an explicit expected-old SHA.

Could another writer move the ref after preflight and still let our stale write through?

## Finding

For ordinary campaign publication, require the prepared campaign commit to have **exactly one parent: pinned HEAD H**.

If another writer advances the ref from H to sibling/descendant D before our update, target C(parent=H) is not a descendant of current D, so a non-force update to C is not a fast-forward and must be rejected.

Thus safety depends jointly on:

```text
single-parent C(parent = pinned H)
+ non-force fast-forward ref transition
```

The preflight ref probe remains an orphan-avoidance/performance optimization, not the final race guard.

Do not create merge commits in the normal campaign publication path; merge/reconciliation semantics belong above object transport and produce a newly validated single-parent result against the new authoritative HEAD.

**Disposition: add explicit single-parent invariant.**

---

# 3. Challenge — ancestry after lost ACK is sufficient proof of what?

## Attack

Research draft says if intended commit C is an ancestor of current D, publication is confirmed.

But D may later change/revert values introduced by C. Therefore ancestry does not prove that C's exact state remains current.

Also C might enter D through an externally created merge rather than because the runtime's specific ref-update request succeeded.

## Finding

Separate two claims:

### HISTORICAL_PUBLICATION_PROVEN

`C` is reachable from the current authoritative lineage.

This proves C's semantic transaction became durable authoritative history, regardless of whether it entered by our exact lost-ACK transition or was later incorporated through another valid fast-forward history construction.

For explicit save acknowledgement, this is enough to establish that the saved frontier existed durably, subject to current-source compatibility before continuing from local HOT state.

### CURRENT_COMPATIBILITY_PROVEN

Current authoritative HEAD D still composes coherently with the local working state and any dependent continuation.

This requires targeted D-vs-C inspection over relevant changed paths/dependencies when D != C.

Consequences:

- ancestry alone may confirm historical durability;
- ancestry alone SHALL NOT clear all current dirtiness or authorize continuation from stale local state;
- adopt/revalidate D;
- if D lawfully superseded C's values, use D as current authority rather than restoring C;
- if D conflicts with unresolved local continuation assumptions, return semantic revalidation requirement.

**Disposition: significant refinement.**

---

# 4. Challenge — what if C is absent from current lineage after ambiguous ACK?

## Attack

A later force rewrite by an external actor could remove a commit that had in fact been published earlier. Then `C not ancestor of D` does not logically prove C was never selected historically.

## Finding

Under HDM's normal append-only/no-force writer contract, non-ancestry means C is not part of current authoritative lineage and cannot satisfy current recovery-source proof.

Unexpected history rewrite is outside normal optimistic concurrency. Treat evidence of it as integrity/recovery escalation rather than trying to reconstruct a vanished historical ref-selection fact from ordinary gameplay transport.

For Step 5.6 acknowledgement semantics:

- do not claim current durable closure from an unreachable C;
- repin actual authoritative D;
- revalidate/rebuild from D;
- if history rewrite is detected/credible, mark affected scope suspect under integrity policy.

No force rewrite is used to restore C.

**Disposition: retain append-only assumption as explicit normal-operation contract.**

---

# 5. Challenge — no-op commit can still arise with a non-empty planned write set

## Attack

The semantic planner can mark a path dirty even though after normalization/revalidation its final bytes already equal the base blob. Or a stale dirty marker can survive a crash after successful remote publication.

A naive core could create a tree identical to base and then create an empty commit.

## Finding

No-heartbeat law must apply after physical delta normalization as well as before planning.

Before commit creation:

```text
remove byte-identical/no-longer-required path mutations
recompute required pending write set
if resulting tree == base tree / write set empty:
    NO_WRITE_NEEDED
    no commit
```

Dirty bookkeeping is repaired/adopted separately; it does not justify a repository write.

**Disposition: add normalized-empty-delta guard.**

---

# 6. Challenge — clearing dirty state after publish can erase newer local work

## Attack

A transaction freezes owner/path state at generation G. While network I/O is in flight, later allowed work may produce generation G+1, possibly in the same logical owner or physical path.

If success simply says "clear this dirty path", G+1 can be lost from the dirty set.

## Finding

Dirty clearing must be **version/generation-specific**, not path-wide.

Conceptually transaction freeze records exact owner/path semantic revision or dirty generation represented in the prepared bytes.

On adoption:

```text
mark frozen generation G durable
clear dirty only if current local generation == G
if current generation > G:
    keep later generation dirty
```

Step 5.5 scoped quiescence reduces this case for explicit save roots, but transport architecture must still be correct for independent/newer mutations and other publication boundaries.

No universal persisted generation schema is required by Step 5.6; implementation may use owner revisions/fingerprints/dirty generations already available or introduce an in-process equivalent.

**Disposition: significant refinement.**

---

# 7. Challenge — disjoint changed paths are not always semantically disjoint

## Attack

Another writer may change file A while our transaction writes file B, but B's result was derived from A. Path disjointness alone would incorrectly permit transport-only rebase.

## Finding

Transaction validation needs a bounded **semantic dependency/read footprint**, not merely write-path intersection.

Safe transport-only rebuild requires external changes to be disjoint from at least:

```text
write footprint
accepted read/dependency footprint
owner/routing/authorization dependencies
required recovery/reference dependencies relevant to the transaction
```

The footprint must be bounded and owner-derived; it is not permission for campaign-wide dependency capture.

If changed paths overlap a dependency, targeted semantic revalidation is required even if physical write paths differ.

**Disposition: retain research model, make footprint normative.**

---

# 8. Challenge — same physical file but independent fields

## Attack

Multiplayer runtime currently allows structural reconciliation when concurrent changes touch independent data in the same file.

A strict path-overlap rule would cause unnecessary re-resolution.

## Finding

Step 5.6 should not define a generic JSON/YAML merge engine.

If a native owner defines a deterministic field/substructure merge/revalidation contract, Python core may use it. Otherwise same-owner/path overlap is conservatively semantic revalidation/conflict.

Repository structure should continue reducing false sharing by keeping independently mutable owners in separate files.

**Disposition: owner-defined reconciliation only.**

---

# 9. Challenge — physical idempotency via deterministic commit SHA

## Attack

Could retries be simplified by making every semantic transaction produce exactly one deterministic commit SHA?

## Finding

Not reliably useful as a semantic requirement:

- base HEAD may legitimately change;
- commit metadata can change;
- retry may omit writes already satisfied by external/current authority;
- current semantic state can require a different resulting tree.

Require semantic idempotency via stable execution/native identities and current-source revalidation. Physical object identity is incidental.

Deterministic metadata may be an implementation optimization but cannot be authority.

**Disposition: reject deterministic-SHA requirement.**

---

# 10. Challenge — process dies after successful update but before local adoption

## Attack

If there is no persistent publication-attempt journal, how can restart know whether the previous request succeeded?

## Finding

For cold process loss, repository/native sources are authority. The volatile attempt state does not need to survive merely to preserve a local acknowledgement flag.

On cold recovery:

- hydrate actual authoritative source set;
- Step-3 stable execution/receipt identities prevent semantic replay where required;
- do not recreate old HOT state from memory guesses;
- stale local dirty bookkeeping cannot override repository truth.

A persistent generic transaction journal is therefore not justified by this failure alone.

If the host preserves an exact invocation retry identity across restart, the normal Step-3 idempotency/recovery path can determine whether the semantic result is already durable.

Checkpoint/source-selection details remain Step 5.7.

**Disposition: no generic publication journal introduced.**

---

# 11. Challenge — server-confirmed failure vs transport ambiguity

## Attack

A generic exception type `write failed` cannot distinguish:

- server definitely rejected the ref update;
- request may have reached server but response was lost.

Treating both the same either creates unnecessary reads or risks false retry/acknowledgement.

## Finding

`RepositoryPort` must expose outcome epistemics, not just success/failure.

Conceptually:

```text
CONFIRMED_ACCEPTED
CONFIRMED_REJECTED
INDETERMINATE
```

for the authority-changing operation.

HTTP 200-equivalent authoritative success is confirmed accepted.
A server-originated explicit conflict/validation rejection is confirmed rejected for that attempt.
Network timeout/connection loss after dispatch may be indeterminate unless the backend can prove non-delivery.

Only `INDETERMINATE` requires ambiguity verification.

**Disposition: add transport epistemic contract.**

---

# 12. Challenge — authorization with a Python bridge/service account

## Attack

Current campaign policy distinguishes repository permission from gameplay authority and in places derives creator/audit identity from GitHub commit history.

A Python persistence service using one shared service identity could accidentally collapse all players into one repository actor and bypass the intended authorization/audit model.

## Finding

Python ownership does **not** imply service-account ownership.

`RepositoryPort` must carry authenticated **acting principal/delegated authorization context** sufficient to enforce the existing campaign/player/storage-owner rules.

The bridge must not convert "Python service can write repository" into gameplay authority.

Preferred deployment property:

```text
requesting authenticated user/player
    -> delegated/scoped repository credential or trusted acting-principal evidence
    -> Python core authorization validation
    -> repository operation
```

If a deployment uses a technical service credential, it still requires cryptographically/trustworthily bound acting-principal authorization; commit author metadata alone must not be forged and trusted as permission evidence.

This may require later adjustment of legacy creator-detection/audit mechanics if the chosen host cannot preserve authenticated per-user GitHub authorship. That is a deployment/access-control realization issue, not permission to weaken 5.6 transaction correctness.

**Disposition: record mandatory authenticated-principal bridge requirement.**

---

# 13. Challenge — built-in ChatGPT Python cannot access GitHub

## Attack

Owner mandates Python repository ownership, but current OpenAI documentation states ChatGPT data-analysis Python cannot make external web/API requests. A connected GitHub app is a separate integration surface.

Therefore the architecture could be unimplementable in the baseline plain-ChatGPT host.

## Finding

This is a real deployment prerequisite, but it does not invalidate the transaction architecture.

Step 5.6 can canonically require:

> The runtime host SHALL provide deterministic Python core an authenticated `RepositoryPort` capable of the required exact Git/ref operations.

Step 5.6 should not choose the bridge product prematurely.

Possible later realization classes include:

- host-native callable repository capability exposed to Python core;
- external deterministic Python persistence service;
- remote MCP/custom app bridge where plan/tier/security support it;
- another explicitly supported runtime host.

Current plain ChatGPT Data Analysis Python alone is **not** evidence that this requirement is satisfied.

Because the owner explicitly chose Python-core repository ownership, the missing bridge is recorded as a host/deployment feasibility blocker to resolve before implementation/release of any profile claiming campaign persistence.

Do **not** silently fall back to LLM-owned Git writes.

**Disposition: deployment prerequisite/deferred feasibility, no owner decision needed now.**

---

# 14. Challenge — branch protection / repository configuration

## Attack

A repository may reject direct ref updates because of branch/ruleset configuration even when application-level authorization is valid.

## Finding

Repository write capability is an environmental precondition. The Python core must distinguish authorization/configuration rejection from concurrency conflict and surface a typed infrastructure failure.

HDM cannot promise direct campaign publication to a ref whose repository rules forbid the required non-force write path.

Do not bypass repository protection by force, alternate hidden ref rewrites, or per-file Contents writes.

**Disposition: environment capability validation required; no semantic fallback.**

---

# 15. Challenge — multi-domain partial success

## Attack

If campaign domain A succeeds and live/native domain B fails, continuing from A may be incompatible with still-current B. Preserving A alone is not sufficient recovery logic.

## Finding

Step 5.5 already says A remains real. Step 5.6 must additionally require composed-source **compatibility revalidation** before dependent continuation.

Generic rule:

```text
publish A -> success
publish B -> failure

A remains authority
whole promise = incomplete
re-read/revalidate actual required source composition
block only dependent edge/scope until compatible closure holds
```

Exact authority-transfer ordering for live/campaign compaction belongs to 5.8.

**Disposition: retained with compatibility refinement.**

---

# 16. Challenge — checkpoint same transaction

## Attack

If a checkpoint is independently required, putting it in a later commit can leave a short period where campaign state is durable but the intended checkpoint pointer/evidence is not.

Conversely always including checkpoint creates noise and duplicate authority pressure.

## Finding

If independent checkpoint policy says checkpoint creation/update is part of the **same required campaign durability edge** and checkpoint paths live on the same campaign ref, its descriptor and any pointer updates should join the same one-tree campaign transaction.

If checkpoint is merely an optional later optimization, it may lag.

Step 5.7 must define which case applies. Step 5.6 supplies the atomic same-ref mechanism but does not force checkpoint creation.

**Disposition: interface rule retained.**

---

# 17. Strongest counterargument to the recommendation

A much simpler implementation could serialize all campaign writes through one centralized Python service/lock and skip optimistic conflict machinery.

This would make campaign commits easy to reason about and might reduce races.

Why it is not recommended as the architecture baseline:

- it creates a new global availability bottleneck and service dependency;
- multiplayer/live already needs independently scoped authority and cheap local/live paths;
- one global lock can serialize unrelated scenes/players unnecessarily;
- crash/recovery still needs exact durable-source proof;
- it does not remove the need to detect external/noncooperating repository writes;
- current architecture deliberately avoids campaign-global writable authority where scoped optimistic ownership is sufficient.

A local per-ref mutex inside one Python process is still a useful implementation optimization to prevent self-induced concurrent publication attempts, but remote non-force validation remains correctness authority.

---

# 18. Refined recommended model

```text
STEP-5.5 DURABILITY REQUEST
        |
        v
PYTHON PERSISTENCE CORE
    freeze exact owner generations + dependency footprint
    derive/normalize exact write set
    if empty -> NO_WRITE_NEEDED
    build one tree from pinned H
    preflight ref probe (optimization)
    create one single-parent commit C(parent=H)
    non-force ref transition (final race guard)
        |
        +--> confirmed accepted
        |       -> historical publication proven
        |       -> adopt exact current authority
        |       -> generation-specific dirty clearing
        |
        +--> confirmed rejected/conflict
        |       -> repin + dependency-aware revalidation
        |
        +--> indeterminate
                -> targeted current-ref + ancestry verification
                -> separate historical publication proof
                   from current semantic compatibility
```

Repository/object preparation never becomes semantic authority.

No force push, no per-record product commits, no heartbeat, no generic merge, no gameplay replay, no global distributed transaction, no LLM-owned repository choreography.

---

# 19. Exit from analytical challenge

**Verdict: PASS WITH MATERIAL TECHNICAL REFINEMENTS.**

No unresolved product-semantic choice requires owner escalation.

Candidate specification should incorporate:

1. single-parent commit invariant;
2. authority-atomic rather than network-atomic terminology;
3. transport outcome epistemics (`accepted/rejected/indeterminate`);
4. ambiguous ACK split into historical-publication proof + current compatibility proof;
5. normalized-empty-delta/no-op suppression;
6. generation-specific dirty adoption;
7. bounded semantic dependency/read footprint for conflict classification;
8. native-owner-only structural reconciliation;
9. authenticated acting-principal requirement for Python repository bridge;
10. host-provided RepositoryPort as mandatory deployment capability;
11. multi-domain compatibility revalidation after partial success;
12. no generic persistent publication journal absent later evidence.
