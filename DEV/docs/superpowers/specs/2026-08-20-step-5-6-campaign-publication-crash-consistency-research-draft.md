# Step 5.6 — Campaign Publication & Crash Consistency — Research Draft

Status: **RESEARCH / DESIGN DERIVATION — NOT CANONICAL**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Recommended direction:

> **PYTHON-OWNED SINGLE-REF CAS PUBLICATION**

This draft derives the physical campaign publication contract from already-canonical Step 5.5 durability semantics and the owner decision that runtime repository/GitHub work belongs to deterministic Python core, not to LLM-owned tool choreography.

---

# 1. Information ledger

## FACT — current campaign transport already aims at one-ref atomicity

Current `GAME/CORE/PERSISTENCE.md` uses:

```text
create_tree(base pinned tree, complete dirty delta)
    -> ref probe
    -> create_commit(parent pinned HEAD)
    -> update_ref(force=false)
```

It already forbids Contents-API mutations inside an ordinary campaign transaction, requires one base-tree-derived tree, treats an unreachable prepared commit as non-authoritative, and forbids force-pushing after races.

## FACT — Git object preparation does not publish campaign authority

Creating blobs/trees/commits creates addressable Git objects. The branch-selected campaign state changes only when the authoritative campaign ref points to a commit containing the new tree.

GitHub's Git Trees documentation explicitly requires committing a created tree and then updating a branch reference for branch publication. GitHub's ref API defines `force=false` as requiring a fast-forward update rather than overwriting intervening work.

## FACT — current runtime has no general Python persistence subsystem

The shipped `GAME/TOOLS/` currently contains `init_campaign.py` but no general runtime repository gateway/persistence engine.

Therefore Python-owned persistence is a future machine-realization obligation, not an already-existing implementation to preserve unchanged.

## FACT — built-in ChatGPT data-analysis Python cannot directly call external APIs

Current OpenAI documentation states that the Python environment used for ChatGPT data analysis cannot make external web requests or API calls. Connected apps/plugins are a separate external-action integration surface.

Therefore a runtime profile that uses deterministic Python persistence requires a host-provided authenticated repository capability/bridge. The exact deployment mechanism is not solved by Step 5.6.

## CONSTRAINT — Python core owns repository mutation

Owner decision:

```text
LLM roles
    do not execute repository transport

Python deterministic core
    owns planning, validation, Git transport, conflict handling,
    ambiguity resolution, retry and local adoption
```

No correctness contract may depend on an LLM reproducing a GitHub API sequence or manually encoding textual payloads.

## CONSTRAINT — maximal atomicity inside one campaign ref

For one logical campaign publication domain:

```text
one logical durability transaction
    -> one complete resulting tree
    -> one commit
    -> one authoritative non-force ref transition
```

Per-record/product-step commits are forbidden when the records form one coherent campaign durability transaction.

## CONSTRAINT — no distributed transaction across native durability domains

Step 5.5 already establishes that a durability promise may compose multiple native sources. If native domain A publishes and B fails, A's publication remains real authority.

Step 5.6 must not invent rollback or force-rewrite semantics merely to emulate a global all-or-nothing commit.

## CONSTRAINT — semantic retry is not gameplay replay

Accepted execution, IDs, fixed RNG experiments/results, receipts and established native state are not re-executed merely because repository transport failed.

## CONSTRAINT — no heartbeat/no-op publication

If required closure is already durable and the physical pending write set is empty, successful save/durability acknowledgement may require zero repository mutation.

## ASSUMPTION A1 — normal campaign refs are append-only under HDM writers

HDM-owned campaign publication uses non-force fast-forward transitions. External history rewrite is not normal concurrency and must be treated as integrity/recovery evidence rather than silently normalized.

## ASSUMPTION A2 — backend can expose exact ref and commit/tree identities

The Python repository port must provide enough identity evidence to pin one ref revision, create/inspect exact Git objects, attempt conditional/non-force publication, and perform targeted ambiguity/conflict verification.

A backend that returns only prose-like "saved" status is insufficient.

---

# 2. Architecture recommendation

## 2.1 Responsibility split

Recommended conceptual layering:

```text
semantic/native owners + Step-5.5 durability policy
        |
        v
DurabilityRequest / required source closure
        |
        v
PYTHON PERSISTENCE CORE
    closure-domain selection
    transaction freeze
    pending write-set derivation
    local invariant validation
    dependency/read-footprint validation
    publication attempt
    conflict/ambiguity classification
    adoption + dirty/exposure updates
        |
        v
RepositoryPort
    exact Git object/ref operations
        |
        v
GitHub / repository backend
```

`RepositoryPort` is a narrow runtime capability boundary, not a generic cloud-storage abstraction.

Do not generalize it to arbitrary S3/Dropbox/filesystem semantics unless a real future deployment requires that. Git commit/tree/ref semantics are directly useful to the current product.

## 2.2 No mandatory persisted PublicationPlan

One transaction needs a frozen in-process plan, but Step 5.6 does not require a universal persistent `PublicationPlan` record.

Conceptually the Python core needs values equivalent to:

```text
CampaignPublicationAttempt {
    repository_identity
    target_ref
    authorization_context

    pinned_head_sha
    pinned_tree_sha

    durability_reason
    named correctness edge?       # if applicable
    required source evidence

    path mutations[]              # final exact content/delete intent
    semantic dirty roots[]
    dependency/read footprint[]

    prepared_tree_sha?
    prepared_commit_sha?
}
```

This can remain an in-memory typed value. Persistence of an attempt journal should be added only if later host/recovery analysis proves it necessary.

---

# 3. Transaction freeze and write-set derivation

## 3.1 Freeze before remote mutation

For one campaign publication attempt, Python core freezes:

```text
repository + exact target ref
validated write authorization
pinned authoritative HEAD H
base tree T(H)
Step-5.5 durability roots for this domain
complete established dirty/new/delete roots selected by policy
required semantic/recovery dependencies
final exact intended bytes/text for each changed path
dependency/read footprint used to establish compatibility
publication reason / blocked edge where relevant
```

No path may be appended ad hoc after tree preparation. New required state invalidates the plan and requires rebuild.

## 3.2 Required source closure is not the write set

For required durable source closure `R`:

```text
R = roots + accumulation + transitive required dependencies
```

Physical pending write set `W` is only material in `R` that is not already sufficiently durable at the pinned authoritative source composition, plus required dirty companion materializations.

Thus:

```text
already durable unchanged dependency
    -> closure evidence
    -> NO WRITE

dirty/new owner state
    -> WRITE

new durable reference to new ID
    -> referenced owner + required index/routing companion in SAME transaction
```

This prevents both incomplete saves and needless repository churn.

## 3.3 Exact base-tree preservation

For an existing campaign:

```text
new_tree = base_tree(H) + exact semantic path delta
```

Unchanged paths inherit exact blobs. Do not parse/reserialize unrelated YAML/JSON/Markdown.

A formatting-only difference is not a semantic write reason.

---

# 4. Single-ref atomicity model

Let:

```text
H = pinned current campaign commit
T = complete resulting tree derived from H
C = commit(parent=H, tree=T)
R = campaign ref
```

Preparation:

```text
create T
create C
```

changes no campaign authority.

The authority switch is:

```text
R: H -> C
```

performed with `force=false` / fast-forward semantics.

Therefore readers resolving the campaign ref see either:

```text
H / old coherent campaign tree
```

or:

```text
C / new coherent campaign tree
```

not a product-visible sequence where PC, CURRENT, indexes and LOG become durable in separate campaign commits.

This is maximal practical atomicity within one Git ref.

---

# 5. Preflight ref probe versus final race guard

The current pre-commit ref probe remains useful, but its role must be stated accurately.

## Preflight probe

Purpose:

- avoid creating a commit already known to have a stale parent;
- reduce orphan/prepared object creation;
- trigger earlier targeted revalidation.

It is **not** the final concurrency guarantee because the ref can move immediately afterward.

## Final guard

The actual final race guard is:

```text
prepared commit parent = H
AND
update ref to C with force=false
```

If another writer advanced `R` after the probe but before the ref update, `C(parent=H)` is no longer a fast-forward from current `R`; the update must not overwrite the other writer.

The resulting prepared commit may remain unreachable. That is storage garbage/debt for later cleanup, not gameplay authority.

---

# 6. Publication outcome model

Recommended conceptual outcomes:

```text
NO_WRITE_NEEDED
CONFIRMED_PUBLISHED
CONFLICT_REVALIDATION_REQUIRED
FAILED_PREPUBLICATION
AMBIGUOUS
```

A successful acknowledgement may additionally include:

```text
published_commit_sha
observed_authoritative_head_sha
```

where the observed current HEAD may already be a descendant of the published commit after ambiguity resolution or concurrent later work.

## NO_WRITE_NEEDED

Required durable closure already holds and there is no physical write set.

No tree, commit, ref update, heartbeat or timestamp mutation occurs.

## CONFIRMED_PUBLISHED

Evidence proves the intended semantic publication has entered authoritative history and the required current source composition is compatible.

Normal case: successful final ref update response selects `C`.

Ambiguity-recovery case: current authoritative ref is later `D`, but `C` is proven an ancestor of `D`; adopt/revalidate `D` as current rather than pretending `C` is still HEAD.

## CONFLICT_REVALIDATION_REQUIRED

Authoritative state moved in a way that prevents publishing the frozen plan unchanged or requires semantic compatibility analysis.

This is not a gameplay rollback and not automatically a corruption state.

## FAILED_PREPUBLICATION

The failure is known to have happened before authoritative ref selection, e.g. authorization failure, local completeness failure, tree/commit creation failure before ref mutation, or a definitely rejected non-force ref update.

## AMBIGUOUS

The core cannot determine whether the authority-changing ref transition happened.

Do not say `saved`; do not clear corresponding dirty state; do not replay gameplay semantics.

Targeted authoritative verification is required when available.

---

# 7. Ambiguous acknowledgement protocol

This is the largest gap in the current runtime prose.

Suppose Python core created intended commit `C` and attempted:

```text
R -> C
```

but the transport response is lost.

A later ref read returns current HEAD `D`.

## Case A — D == C

Publication is confirmed.

Adopt C and clear only dirtiness proven covered by C.

## Case B — C is an ancestor of D

Publication is also confirmed for C's semantic transaction.

This can occur if the update to C succeeded and another correct writer then advanced the ref from C to D before ambiguity verification.

The runtime must:

```text
confirm C entered authoritative history
adopt D as current authoritative HEAD
inspect/revalidate only relevant D-vs-C changes
clear local dirty roots only to the extent still semantically covered
```

It must not downgrade the working frontier back to C.

## Case C — C is not reachable from D under normal append-only history

The intended commit is not part of the current authoritative lineage.

Do not treat it as successful publication.

Repin D, perform targeted conflict/dependency revalidation and rebuild as needed.

If evidence indicates unexpected force-rewrite/history replacement rather than ordinary fast-forward concurrency, escalate affected scope to integrity/recovery handling.

## Case D — authoritative verification itself unavailable

Remain `AMBIGUOUS`.

Per Step 5.5:

- coherent local/private HOT play may continue if no independent correctness-critical edge blocks it;
- save success is not acknowledged;
- correctness-critical durability edge remains unresolved;
- later suitable execution performs targeted verification/retry.

This protocol requires the repository port to support an exact ancestry/reachability test or equivalent bounded commit comparison.

---

# 8. Conflict classification after HEAD movement

Do not use one generic "merge" policy.

Given old base `H` and new authoritative head `N`, determine the changed-path/semantic dependency overlap with the frozen attempt.

## Class 1 — transport-only rebase/rebuild

External changes are disjoint from:

```text
local physical write paths
local semantic dirty roots
accepted action dependency/read footprint
authorization/ownership dependencies
required recovery closure dependencies
```

Then the already-established local result may remain valid.

Python core may:

```text
adopt N as base
reuse established semantic result and fixed RNG
rebuild exact path delta onto T(N)
retry publication
```

No gameplay re-resolution is needed.

## Class 2 — owner-defined deterministic reconciliation

Overlap exists, but the owning native contract explicitly defines a safe deterministic reconciliation operation.

Use that owner rule and then rebuild.

Do not infer this merely because a YAML object can be textually merged.

## Class 3 — semantic revalidation/re-resolution required

External changes touch an assumption/dependency or writable owner in a way that can change the meaning/legality/result of the established local action.

The persistence subsystem returns a typed revalidation requirement to the appropriate deterministic/semantic owner.

It does not blindly merge or silently choose a winner based on Git text order.

Already accepted random values remain associated with their experiment when the same experiment still applies. New randomness is allowed only when semantic re-resolution establishes that the prior experiment no longer represents the current action.

---

# 9. Semantic versus physical idempotency

## Semantic idempotency is required

Retrying repository publication must not duplicate:

- gameplay transitions;
- MechanicalEvents;
- IDs/allocations;
- payments/items/resources;
- RNG experiments/results;
- temporal firing occurrences;
- accepted player intent.

Retry operates on established state and stable execution/causal identities.

## Physical Git-object idempotency is not required

A retry after base-head movement may legitimately create a new tree and a new commit SHA.

Protocol correctness does not require "same semantic transaction always has the same commit SHA".

Commit messages/timestamps are audit/presentation metadata, not idempotency authority.

A future implementation may choose deterministic commit metadata where useful, but Step 5.6 should not make this a semantic requirement.

---

# 10. Crash/failure matrix

| Point | Campaign authority | Recovery / retry |
|---|---|---|
| before object preparation | old ref HEAD | retry frozen/renewed plan after normal validation |
| tree created, process dies | old ref HEAD | tree is non-authoritative object; restart from actual ref |
| ref moved before commit | newer external HEAD | discard stale transaction; targeted revalidation/rebuild |
| commit C created, no ref update | old/current ref HEAD | C non-authoritative/unreachable; restart from current ref |
| update_ref definitely rejects race | newer external HEAD | C remains non-authoritative; targeted revalidation/rebuild |
| update_ref succeeds normally | C authoritative at response point | adopt C; clear covered dirty state; no routine reread |
| update_ref response lost | unknown | enter AMBIGUOUS; verify current ref + ancestry of C |
| remote success then process dies before local adoption | repository is authority | restart hydrates actual ref; never replay gameplay merely because local dirty flags survived/lost |
| C published, then another writer advances to D | D current, C historical ancestor | adopt/revalidate D; C's publication remains real |
| another required native domain fails after campaign success | campaign publication remains real | overall composed promise incomplete; retry missing domain from actual source composition |

No failure mode authorizes force-push to recreate the runtime's preferred old view.

---

# 11. Local adoption and dirty clearing

On normal confirmed publication to `C`, Python core may atomically update its local working metadata conceptually as:

```text
known_head = C
known_tree = T(C)
mark covered state durable at C
remove/adjust only dirty roots whose intended state is proven represented
update scope exposure baseline for covered state
release named correctness edge only if its complete required closure now holds
```

If later authoritative HEAD `D` is already known, adopt `D`, not C, and reconcile local dirty coverage against D.

Local bookkeeping is not authority. A process crash between remote success and local clearing is recovered from repository/native-source truth.

This means an implementation may conservatively retain stale dirty markers after an uncertain local crash; after hydration, it must detect already-satisfied intended state and avoid producing duplicate semantic effects or no-op commits.

---

# 12. Multi-domain publication

Step 5.6 establishes only generic physical rules:

```text
for each native durability domain:
    publish through that domain's own authority protocol
    successful native publication remains real

overall promise succeeds only when:
    required compatible native source composition holds
```

There is no rollback of a successful campaign commit because a separate live/source publication later failed.

Likewise no generic two-phase commit, transaction coordinator, global commit ID or cross-ref lock is introduced.

Step 5.8 must design live/campaign authority-transfer order so every intermediate state retains a valid authority owner.

---

# 13. Checkpoint and projections

## Checkpoint

Publication does not create a checkpoint by default.

If independent 5.7 policy later requires a checkpoint and it is a path owned by the same campaign ref for the same logical boundary, it may join that one campaign tree transaction.

If no checkpoint is needed, do not create/update checkpoint paths or MANIFEST pointers.

## Story/transcript/projections

Noncanonical Story/transcript/render projections do not automatically join campaign durability closure.

They may lag until their Steps 5.10–5.12 contracts require publication.

A specific exact message/evidence item that remains irreducible recovery evidence is different: while required by Step 5.2/5.5 recovery closure, it participates as recovery-critical material rather than merely a presentation projection.

---

# 14. Python repository capability boundary

The runtime requires a deterministic repository capability with operations semantically equivalent to:

```text
read exact ref -> commit SHA
read exact commit/tree identity
read/fetch exact affected paths at pinned commit
compare/ancestry test between exact commits
create tree from base tree + exact delta
create commit with exact parent/tree
attempt non-force ref transition
```

Exact method names/API transport are implementation details.

The capability must preserve authenticated application authorization separately from mere repository write permission.

## Host/deployment prerequisite

Built-in ChatGPT data-analysis Python currently cannot issue external web/API requests. Therefore the baseline product cannot assume that a local sandbox script can directly call GitHub merely because ChatGPT has a connected GitHub app.

Step 5.6 recommendation:

- keep repository ownership in Python deterministic core as decided;
- define authenticated `RepositoryPort` as a required host capability;
- treat the concrete Python-to-GitHub bridge as a deployment/host feasibility obligation;
- do not fall back to LLM-owned Git choreography to hide a missing bridge.

If a supported baseline deployment cannot provide such a bridge, that is a host-profile feasibility blocker to resolve before implementation/release, not a reason to weaken transaction semantics.

---

# 15. Alternatives challenged

## Alternative A — per-record commits

Rejected.

It introduces product-visible partial states, larger conflict windows, repository noise, and failure points between records that belong to one durability closure.

## Alternative B — LLM directly executes GitHub tool choreography

Rejected by owner decision and technical analysis.

It couples correctness to natural-language orchestration, adds latency/tool-call overhead, makes deterministic retry harder, and exposes encoding/transport details to the wrong layer.

## Alternative C — preflight ref check is sufficient concurrency protection

Rejected.

The ref may move after the probe. Final correctness requires non-force/conditional ref selection against a commit parented from the pinned base.

The probe remains a useful optimization.

## Alternative D — always confirmation-read after successful update_ref

Rejected for normal success.

A successful authoritative response is sufficient to adopt the write. A mandatory reread wastes latency and violates current hot-path goals.

Targeted read/ancestry verification is required only after ambiguous acknowledgement, external movement, conflict, recovery or another explicit resync reason.

## Alternative E — blindly rebase every established delta after HEAD movement

Rejected.

Disjoint changes may be transport-rebased, but dependency overlap can invalidate the action's semantic assumptions. Revalidation is owner/dependency-aware.

## Alternative F — roll back domain A when domain B fails

Rejected.

Step 5.5 already establishes that successful native publication remains real authority. Cross-domain rollback would require history rewrite/distributed transaction semantics and can overwrite other valid work.

## Alternative G — generic cloud-storage abstraction

Rejected for now.

Current product depends specifically on Git commit/tree/ref properties for versioned campaign authority and optimistic concurrency. A narrow repository port is enough. Generalize only on concrete need.

---

# 16. Preliminary decision status

No new owner-level product decision has emerged from the physical transaction analysis.

The recommended architecture follows mechanically from:

- owner-mandated Python repository ownership;
- Step-5.5 durability semantics;
- existing one-tree/one-commit campaign direction;
- no-force optimistic concurrency;
- native-source authority preservation.

The only newly exposed external dependency is the host capability required to let deterministic Python core perform authenticated repository operations. Current ChatGPT built-in data-analysis Python does not itself satisfy that capability. This is recorded as a deployment prerequisite and must be resolved before machine implementation can claim the baseline runtime profile is viable.

Next gate: adversarial challenge of this model, especially ambiguous acknowledgement ancestry proof, stale-head semantic revalidation, post-success crash adoption and host repository bridge assumptions.
