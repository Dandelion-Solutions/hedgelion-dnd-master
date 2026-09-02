# R2.7 WP-13 — Durability / SAVE / Publication — Step 5 Candidate Specification

Status: **STEP 5 COMPLETE — CANDIDATE FOR WHOLE-PROJECT ADVERSARIAL REVIEW**

Date: 2026-09-02

Accepted direction:

> **SCOPE-EVALUATED NATIVE-DOMAIN DURABILITY COMPOSITION + IMMUTABLE EPHEMERAL PUBLICATION ATTEMPTS**

This candidate is implementation-facing architecture, not runtime implementation. It consumes accepted Step-5, R2.6, WP-11 and WP-12 authority and does not reopen their semantics.

---

# 1. Scope

WP-13 realizes:

- scope-relative durability evaluation;
- explicit SAVE composition across admitted native durability domains;
- campaign publication envelope and currentness/conflict/ambiguity handling;
- WP-11 record/index path closure;
- WP-12 owner-generation adoption;
- fixed R2.6 Connector transport boundary;
- machine-facing failure/result semantics.

It does not own final checkpoint/recovery machine (WP-14), final live machine (WP-16), bootstrap/migration orchestration (WP-19/WP-20), executable implementation/tests (WP-22), performance tuning (WP-24) or documentation cleanup (WP-26).

---

# 2. Canonical machine split

The following are conceptual typed operation values. Exact Python names/serialization are not fixed.

```text
DurabilityEvaluation          ephemeral
FrozenCampaignPublicationAttempt  immutable ephemeral
RefTransitionOutcome          ephemeral exact authority-operation result
NativeDurabilityResult        ephemeral native-domain result
DurabilityPromiseResult       ephemeral composed boundary result
```

None is a semantic gameplay owner or mandatory persistent record.

---

# 3. Durability evaluation laws

## LAW WP13-1 — Establishment and durability remain independent

WP-13 never reclassifies candidate/prospective state as established. Native owner/execution/live contracts decide establishment. Durability machinery only evaluates/proves whether established state is sufficiently durable for the requested boundary.

## LAW WP13-2 — Durability obligation is scope-relative and owner-triggered

Every request identifies an applicable durability-policy scope/partition and a reason/edge supplied by the owning contract.

WP-13 introduces no global save owner, persisted HARD flag, universal HARD queue or central semantic trigger table.

## LAW WP13-3 — No campaign-global durability frontier/timer

Implementation SHALL NOT use one campaign-global `durable_frontier_time`, global save clock, global dirty generation or equivalent scalar as architecture authority.

Risk-control exposure is evaluated for the applicable policy scope from actual still-relevant unpublished established/recovery state.

## LAW WP13-4 — Exposure basis follows oldest still-relevant unpublished state

For each scope whose policy uses unpublished-exposure risk control, machine state must support determining the oldest still-relevant unpublished basis.

The representation may be aggregate or owner-relative, but:

- unrelated publication cannot reset another still-dirty scope;
- partial publication cannot erase exposure for still-relevant unpublished roots;
- superseded/non-required dirty intermediates need not retain exposure;
- no exact threshold/cadence is selected by WP-13.

## LAW WP13-5 — Required durable closure is distinct from pending write set

A durability boundary first derives a compatible Step-5.2 required durable source closure. The pending write set contains only closure material that is not already sufficiently durable/current.

Already-durable compatible dependencies prove closure without rewrite.

## LAW WP13-6 — Closure construction is bounded

Roots come from owner policy roots plus policy-owned dirty accumulation scope and expand only correctness-required recovery/reference/interpretation dependencies.

No ordinary durability evaluation requires campaign/WORLD/history traversal, broad directory enumeration or generic dependency-graph materialization.

## LAW WP13-7 — Named HARD semantics remain with the owner

The owner defines `MUST_BE_DURABLE_BEFORE(edge)`, policy roots/scope and success postcondition. Shared WP-13 machinery evaluates and attempts to satisfy the closure.

Failure leaves the named edge incomplete; only the dependent scope is gated under the owning law.

---

# 4. Explicit SAVE composition

## LAW WP13-8 — Explicit SAVE freezes one definite promise scope

After explicit SAVE intent is accepted, affected mutation scope is frozen/quiesced enough that the acknowledgement refers to one definite selected save root set and owner generations.

This is not a global host lock, campaign lease or persistent state owner. OOC and independent scopes may continue where safe.

## LAW WP13-9 — SAVE composes native durability domains

The selected required closure is partitioned by already-admitted native durability domains.

Campaign ref, selected live source and another independent native durability domain retain their own authority/publication/atomicity rules. Participation does not create cross-domain scalar order or distributed transaction semantics.

## LAW WP13-10 — Domain execution order is dependency-owned, not globally semantic

When native authority-transfer/dependency contracts require an order, that order is followed. Otherwise implementation may choose a deterministic safe operational order without creating chronology, dominance or a universal cross-domain transaction order.

## LAW WP13-11 — Already-durable domain work is no-write

A native domain whose required portion of the promised closure is already proven compatible/durable returns a domain-level no-write result and performs no heartbeat mutation.

Empty campaign path delta alone does not prove overall SAVE; every required native domain must satisfy its closure.

## LAW WP13-12 — Partial native success remains real

If required domain A confirms durability and domain B later rejects/fails/remains indeterminate:

- A remains authoritative/durable;
- overall SAVE remains incomplete;
- no rollback/force rewrite of A is invented;
- current composed source basis is revalidated before dependent continuation;
- only unresolved dependent scope is gated where correctness requires it.

## LAW WP13-13 — SAVE acknowledgement requires complete confirmed closure

The runtime says/implies `saved` only after all required native domains prove a compatible durable source closure.

Prepared/attempted/ambiguous publication is not success.

Failed explicit SAVE does not itself invalidate coherent established local/private HOT state; independent HARD edges still control their own continuation.

---

# 5. Campaign publication attempt

## LAW WP13-14 — Campaign publication attempt is immutable and ephemeral

Before the first remote Git-object mutation, deterministic Python/core freezes one campaign publication attempt containing at least:

```text
repository identity
target ref
acting principal + authorization evidence/basis
pinned authoritative HEAD H
base tree T(H)
frozen owner generations/fingerprints
campaign-domain durability roots
required recovery/reference/interpretation companions
bounded semantic read/dependency/currentness footprint
exact owner-authorized UPSERT/DELETE path operations
required derived index/projection companions
publication reason / named edge where applicable
```

The value is not persisted as a generic journal/transaction owner.

Discovery of a new required owner/path invalidates the attempt before publication.

## LAW WP13-15 — Authorization basis is evidence, not a permission lease

Frozen acting-principal/authorization evidence does not override current access authority.

Mutable PLAYER binding, mode, join policy, creator/policy grant, routing or another authorization dependency participates in the conflict footprint and is revalidated at the owner-required pre-mutation boundary.

Technical repository permission alone never authorizes gameplay publication.

## LAW WP13-16 — Exact WP-11 paths and required companions form the campaign delta

For every frozen native owner identity, derive its exact WP-11 route or admitted fixed/exceptional route.

The normalized path delta includes every owner-authorized UPSERT/DELETE plus every required derived index/projection companion that must share the same campaign publication closure.

A required discovery index is non-authoritative but its current record update/removal is publication-coherent with the native record when the index contract requires it.

## LAW WP13-17 — Resulting-tree proof is bounded and pre-remote

Before the first remote Git-object mutation, local deterministic validation proves the planned resulting campaign tree satisfies the selected closure and directly touched invariants.

The proof uses frozen HOT/current owner state, exact routes and known pinned base evidence. It is not a campaign-wide scan.

## LAW WP13-18 — Normalize semantic no-ops

Byte-identical UPSERT and DELETE of an already-absent path are removed. Unchanged files are inherited exactly from the pinned base tree and are not reserialized for convenience.

If the normalized campaign-domain delta is empty and the required campaign-domain source closure is already proven compatible/durable, return campaign-domain `NO_WRITE_NEEDED`.

---

# 6. Fixed gameplay transport

## LAW WP13-19 — Shipped repository transport is fixed by R2.6

Supported gameplay/runtime repository publication is:

```text
deterministic Python/core
-> GitHub Connector Git-data/ref operations
-> authoritative non-force ref transition
```

`AGENTS.md` / `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md` development-agent discipline is not the source of this shipped runtime law.

## LAW WP13-20 — No runtime alternate-transport probing/fallback

Gameplay/setup/save/recovery/multiplayer publication SHALL NOT probe or fall back to `gh`, shell/native remote Git, clone/fetch/pull/push/ls-remote/SSH Git, direct private HTTP/API/token workarounds, alternate App/MCP/backend write transport, GitHub Actions gameplay bridge, transparent local-commit push assumptions or equivalent alternate paths.

Missing required Connector capability is a typed supported-profile capability failure.

## LAW WP13-21 — Ordinary existing-campaign Connector envelope

For an existing campaign with pinned `H`:

```text
prepare/freeze attempt locally
-> Connector create base-derived tree T2 from T(H) + full normalized delta
-> Connector read/probe target ref
-> if still H, Connector create one commit C(parent=H, tree=T2)
-> immediately Connector update target ref to C with force=false
```

The preflight ref probe is an orphan-reduction optimization, not final concurrency authority. Final safety is single parent + non-force ref selection.

No LLM call, external research, broad read or new semantic derivation occurs in the post-preflight race window.

## LAW WP13-22 — One campaign boundary publishes one coherent tree/commit

All paths required by one logical campaign-domain durability boundary enter one base-tree-derived resulting tree and one single-parent gameplay commit.

No per-file Contents publication, merge commit, staging ref or force update substitutes for the ordinary campaign transaction.

Storage-owner default-branch metadata remains a separate transaction and never joins campaign owner-state publication.

---

# 7. Publication result epistemics

## LAW WP13-23 — Final ref transition has exact tri-state epistemics

The authority-changing final ref operation exposes:

```text
CONFIRMED_ACCEPTED
CONFIRMED_REJECTED
INDETERMINATE
```

A pre-dispatch capability/validation failure is not a confirmed ref rejection.

## LAW WP13-24 — Broader native result preserves cause class

A domain-level result may additionally represent:

```text
NO_WRITE_NEEDED
FAILED_PREPUBLICATION
REVALIDATION_REQUIRED
CAPABILITY_FAILURE
```

but must preserve whether an authority-changing ref operation was dispatched and what is actually known about its result.

## LAW WP13-25 — Confirmed accepted publication may adopt without gratuitous reread

A confirmed accepted ref response selecting intended C establishes campaign publication at that response point. The runtime may adopt the returned commit/tree/source basis immediately.

That knowledge is not a lease; later operations synchronize when their own currentness policy requires it.

## LAW WP13-26 — Indeterminate result cannot be acknowledged or blindly retried

After an indeterminate final ref operation:

- no SAVE/HARD success acknowledgement;
- no frozen-generation dirty clear by assumption;
- no dependent correctness edge release;
- no gameplay replay/reroll/reallocation;
- no blind second ref transition.

Targeted bounded authoritative verification is required when available.

## LAW WP13-27 — Ambiguity verification uses exact current ref + bounded lineage/current-closure proof

Given intended C and current authoritative D:

```text
D == C
    -> prove required closure at C

C proven reachable ancestor of D
    -> C is durable lineage evidence only
    -> inspect bounded D-vs-C intersection with required closure/dependency footprint
    -> accept only if current D still satisfies compatible required closure

C proven absent from D lineage
    -> C does not prove current closure
    -> repin/revalidate from D

bounded evidence unavailable
    -> remain INDETERMINATE / recovery-required
```

Never restore stale C by force.

Prepared/unreachable object cleanup remains Step-5.13/host concern.

---

# 8. Currentness and conflict

## LAW WP13-28 — Conflict footprint is semantic, not path-only

HEAD movement is classified against the frozen bounded footprint including as applicable:

- exact write paths;
- semantic owner/dirty roots;
- accepted read/dependency footprint;
- authorization/ownership/routing dependencies;
- required recovery/reference/interpretation dependencies.

Different path names do not prove semantic independence.

## LAW WP13-29 — Proven-disjoint movement permits transport-only rebuild

If external movement is proven disjoint from the frozen semantic footprint:

```text
adopt newer authoritative HEAD N
preserve established semantic result / IDs / fixed RNG / execution evidence
rederive exact path delta on T(N)
create a fresh immutable attempt
retry publication
```

No gameplay re-resolution occurs merely because the Git base moved.

## LAW WP13-30 — Relevant overlap uses native-owner reconciliation only

If movement overlaps a relevant dependency, automatic reconciliation is allowed only when the affected native owner defines a deterministic safe merge/reconciliation rule.

Otherwise return typed owner-specific revalidation/re-resolution.

Generic YAML/JSON/text merge, Git merge order or last-writer-wins is not semantic authority.

## LAW WP13-31 — Automatic retry is bounded

Repeated contention/revalidation does not loop indefinitely. After a bounded implementation-defined condition the workflow returns a typed unresolved conflict/synchronization result.

A HARD dependent edge remains unresolved; Step-5.5 friendly local/private behavior may still apply to non-hard failed save/risk-control publication.

## LAW WP13-32 — Git/storage order never establishes fictional chronology

Commit/ref/tree/path/ID ordering is publication evidence only. It cannot decide contested/simultaneous fictional chronology. Step 5.9 remains authority.

---

# 9. Generation-specific adoption and crash behavior

## LAW WP13-33 — Publication adoption is exact-generation-specific

For every frozen owner generation G covered by confirmed compatible publication:

```text
mark G durable under confirmed source basis
if current local generation == G:
    clear dirty membership for G
else:
    keep newer current G+1 dirty
```

Never blanket-clear a path/scope merely because an older frozen version published.

## LAW WP13-34 — Partial campaign-domain adoption cannot reset unrelated exposure

Only owners/generations actually proven durable may leave the still-relevant unpublished set. Scope exposure basis is recomputed/preserved from remaining dirty/recovery-relevant state.

Unrelated successful publication cannot reset another scope.

## LAW WP13-35 — Crash after remote success needs no generic publication journal

If remote/native publication succeeded but local bookkeeping/adoption was lost, cold recovery starts from actual current native authorities and exact pins.

Surviving SQLite/attempt metadata does not override remote authority. Do not replay mechanics to recreate the lost local bookkeeping.

---

# 10. Live/checkpoint/storage integration boundaries

## LAW WP13-36 — Live authoritative establishment remains exact-source CAS

For live-claimed mutable consequence:

```text
prospective deterministic result
-> exact-source live CAS native durability edge
-> confirmed accepted live authority
-> local HOT adoption
```

WP-13 may include this domain in a SAVE/HARD promise but cannot replace it with campaign publication or SQLite transaction. Final live machine remains WP-16.

## LAW WP13-37 — Checkpoint never proves SAVE/publication success

Checkpoint is optional immutable recovery/maintenance evidence. A valid SAVE/campaign publication may create no checkpoint. Checkpoint existence cannot establish SAVE, handoff or current-state authority.

WP-14 owns final checkpoint/recovery realization.

## LAW WP13-38 — Session/local bookkeeping remains non-authoritative

Session `base_head_sha`/`last_published_head_sha`, local known-head/tree values, dirty/exposure metadata and cached source basis are coordination/operation evidence only.

They cannot grant authority, prove currentness by themselves or replace native-source validation.

## LAW WP13-39 — Engine/rules maintenance consumes, not owns, campaign publication

An owner-authorized engine/rules provenance/adoption delta may enter the same campaign-domain publication protocol after its own compatibility/durability/access gates are satisfied.

Storage baseline maintenance remains a separate storage-owner transaction. WP-13 does not select runtime package/migration semantics.

---

# 11. Required implementation/test consequences

Later implementation/TDD must revise current machine/tests so that:

- global one-hour `durable_frontier_time` is not architecture/current correctness authority;
- scope-relative oldest-relevant-unpublished evaluation replaces that global rule;
- valid sparse/no-heartbeat behavior remains;
- `SAVE_CONTRACT` expresses multi-native-domain promise rather than universal campaign-only transaction;
- campaign-only SAVE remains one coherent campaign transaction when no other domain participates;
- `PERSISTENCE` frozen attempt includes owner generation, auth, dependency/read/currentness basis and exact path/index closure;
- stale disjoint/relevant overlap behavior matches WP13-28..31;
- ref outcome tri-state and ambiguity verification are explicit;
- dirty clearing is G-specific;
- R2.6 Connector path/failure coverage is executable;
- checkpoint/live/storage/access/engine-update consumers retain their owner boundaries.

WP-22 and implementation planning own the actual executable changes after architecture approval.

---

# 12. Candidate disposition

```text
CANDIDATE_DIRECTION:        ACCEPTED FOR STEP-6 ATTACK
UPSTREAM_REOPEN_REQUIRED:   NO
HUMAN_DECISION_REQUIRED:    NO
KNOWN_UNRESOLVED_BLOCKING:  0
KNOWN_UNRESOLVED_SIGNIFICANT: 0
```

Step 6 must adversarially attack this candidate against the whole project before any final canonicalization.