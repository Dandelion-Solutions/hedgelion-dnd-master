# R2.7 WP-13 — Durability / SAVE / Publication — Canonical Specification

Status: **CANONICAL WP-13 RESULT — STEPS 1-8 COMPLETE / MANDATORY FINAL SENIOR AUDIT PENDING**

Date: 2026-09-02

Canonical direction:

> **SCOPE-EVALUATED NATIVE-DOMAIN DURABILITY COMPOSITION + IMMUTABLE EPHEMERAL PUBLICATION ATTEMPTS**

Canonicalization basis:

- repaired Step-1 Task Brief / Source Manifest / whole-project critic;
- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-senior-recovery-fixed-gameplay-repository-transport.md` (`SR13-01`);
- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-step-2-evidence-extraction.md`;
- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-source-manifest-step-2-expansion.md`;
- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-step-3-decision-brief.md`;
- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-step-4-collaborative-review.md`;
- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-step-5-candidate-spec.md`;
- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-step-6-whole-project-adversarial-review.md`;
- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-step-7-resolution-gate.md`.

This file is the final WP-13 implementation-facing architecture source of truth, subject to mandatory final Senior audit. Earlier Step-5 candidate wording is derivation where it differs from this canonical result.

---

# 1. Scope and ownership

WP-13 realizes already-accepted durability/SAVE/publication semantics over current R2.7 physical owner/routing/HOT contracts.

It owns the implementation-facing machine contract for:

- scope-relative durability evaluation;
- explicit SAVE composition across admitted native durability domains;
- campaign publication freeze/tree/ref/currentness/conflict/ambiguity behavior;
- WP-11 exact path + required index/projection publication closure;
- WP-12 exact owner-generation durability adoption;
- fixed R2.6 gameplay repository transport boundary;
- typed native-domain / overall durability-result semantics.

It does **not** create a new gameplay semantic owner.

WP-13 does not own or reopen:

- Step-3 execution semantics;
- Step-5.2 RRC semantics;
- Step-5.3 temporal/pending ownership;
- Step-5.4 handoff semantics;
- Step-5.5 durability/SAVE product semantics;
- Step-5.6 publication/crash-consistency semantics;
- Step-5.7 checkpoint/recovery source selection;
- Step-5.8 live ownership/CAS/absorption semantics;
- Step-5.9 chronology;
- Step-5.13 cleanup/GC;
- WP-10 durable family allocation;
- WP-11 identity/routing/index authority;
- WP-12 local HOT/SQLite transaction authority;
- R2.6 repository transport selection;
- final checkpoint machine (`WP-14`);
- final live machine (`WP-16`);
- bootstrap/migration orchestration (`WP-19` / `WP-20`);
- executable implementation/tests (`WP-22` / later approved implementation planning);
- performance partitioning (`WP-24`);
- stale documentation cleanup (`WP-26`).

---

# 2. Conceptual machine values

Equivalent typed in-memory values are required; exact Python names/serialization remain implementation detail.

```text
DurabilityEvaluation
    ephemeral evaluation of one requested durability boundary

FrozenCampaignPublicationAttempt
    immutable ephemeral campaign-domain publication attempt

RefTransitionOutcome
    exact epistemic result of the authority-changing final ref operation

NativeDurabilityResult
    one native durability-domain operation result

DurabilityPromiseResult
    ephemeral composition result for SAVE/HARD/risk-control operation
```

None is:

- gameplay state authority;
- a universal frontier;
- a persistent scheduler/job queue;
- a distributed transaction record;
- a generic recovery cut;
- a persistent publication journal.

---

# 3. Durability evaluation

## LAW WP13-1 — Establishment and durability remain independent

WP-13 evaluates durability only for already-established state.

Native owner / Step-3 / Step-5.8 contracts remain authority for whether a semantic consequence is established. A prospective/unaccepted value cannot become established merely because persistence machinery serialized it.

## LAW WP13-2 — Durability obligation is scope-relative and owner-triggered

Every durability request resolves an applicable native/authority/visibility policy scope and a reason/edge supplied by the owning contract.

No global save owner, persisted HARD flag, universal HARD queue or central semantic trigger table is introduced.

## LAW WP13-3 — No campaign-global durability frontier/timer

Implementation SHALL NOT use one campaign-global `durable_frontier_time`, global save clock, global dirty generation or equivalent scalar as durability/currentness authority.

Domain-native revision/currentness markers remain domain typed under Step 5.1.

## LAW WP13-4 — Exposure basis follows actual oldest still-relevant unpublished state

For a scope whose accepted risk-control policy considers unpublished exposure, implementation must be able to determine the oldest still-relevant unpublished established/recovery basis for that scope.

Representation may be aggregate or owner-relative, but:

- unrelated publication cannot reset another still-dirty scope;
- partial publication cannot erase exposure for still-relevant unpublished roots;
- superseded/non-required dirty intermediates need not retain exposure;
- covered owner generations leave exposure only when current closure proves them durable;
- no numeric threshold/cadence is selected by WP-13.

## LAW WP13-5 — Required durable source closure differs from pending write set

A durability request first derives the compatible Step-5.2 required durable source closure.

The physical pending write set contains only closure material not already sufficiently current/durable in its native domain.

Already-durable compatible native dependencies participate in closure proof without forced rewrite.

## LAW WP13-6 — Closure construction is bounded and native-routed

Required closure begins from:

```text
owner-defined policy roots
+
policy-owned accumulated dirty scope
+
correctness-required recovery/reference/interpretation dependencies
```

Ordinary durability evaluation SHALL NOT require:

- whole campaign/WORLD scans;
- broad directory enumeration;
- full Git history;
- generic dependency-graph materialization;
- Story/transcript reconstruction where native owners suffice.

## LAW WP13-7 — Named HARD semantics remain with their owner

The owning contract defines:

```text
MUST_BE_DURABLE_BEFORE(edge)
policy scope / roots
success postcondition
```

WP-13 machinery evaluates/satisfies the closure only.

Failure leaves that dependent edge unresolved; unrelated scopes are not globally blocked.

---

# 4. Risk-control durability

## LAW WP13-8 — Scope-relative exposure risk control remains MAY_DEFER

A risk-control exposure threshold/condition over deferrable local/private state does **not** itself create a named HARD edge.

At a suitable safe established-state point the runtime may/should request opportunistic durability according to the owning policy.

If that publication fails while coherent local/private HOT survives:

- protection is degraded/retry-due;
- ordinary local/private play may continue;
- the failed risk-control attempt does not invalidate established HOT;
- a separate owner-defined HARD edge still blocks its own dependent continuation;
- no elapsed-time threshold silently upgrades state to HARD.

This law explicitly prevents the current one-hour blocking contract from surviving under a renamed scope-relative clock.

## LAW WP13-9 — Clean risk-control evaluation creates no heartbeat

If no applicable still-relevant unpublished state exists, elapsed time/risk-control evaluation alone creates no commit/checkpoint/timestamp mutation.

No background exact wall-clock flush guarantee exists when the host does not run.

---

# 5. Explicit SAVE promise

## LAW WP13-10 — Explicit SAVE freezes one definite selected promise scope

After explicit SAVE intent is accepted, the affected local mutation scope is quiesced enough that one acknowledgement refers to one definite selected root set and owner generations.

The freeze is ephemeral/local operation state, not a campaign-global lock/lease or persistent owner.

Independent scopes and OOC communication may continue where they cannot change the promise.

## LAW WP13-11 — SAVE composes admitted native durability domains

The required durable source closure is partitioned by already-admitted native durability domains.

Campaign ref, selected live source, storage-owner metadata or another admitted independent domain retain their own authority/publication/atomicity rules.

Participation creates no:

- scalar cross-domain frontier;
- global revision;
- universal total order;
- distributed transaction.

## LAW WP13-12 — Cross-domain execution order is dependency-owned

Where authority transfer / dependency contracts require an order, follow that owner-defined order.

Otherwise implementation may choose a deterministic safe operational order without giving it semantic chronology/dominance meaning.

Live close/absorption order remains Step 5.8-owned.

## LAW WP13-13 — No-write result is operation-current closure proof

A native domain may return `NO_WRITE_NEEDED` only when **this durability operation** has sufficient lawful currentness evidence to prove that its required native source closure is currently compatible/durable.

Therefore:

```text
no local dirty paths
cached known_head
empty normalized campaign delta
```

are not sufficient by themselves.

A new remote read is unnecessary only when the applicable native currentness protocol already provides adequate current evidence for this operation.

If current authority moved over relevant owner/recovery/authorization/routing/dependency state, revalidate before no-write success.

## LAW WP13-14 — Partial native success remains real

If A confirms durability and B rejects/fails/remains indeterminate:

- A remains real authoritative/durable evidence;
- overall SAVE remains incomplete;
- no rollback/force rewrite of A occurs;
- only affected dependent scope remains gated where correctness requires it;
- current composed source basis is revalidated before dependent continuation.

## LAW WP13-15 — Overall SAVE/HARD success requires one current compatible source composition

At the success/acknowledgement boundary, the runtime SHALL prove one current compatible composition of every required native durable source under each participating owner's currentness/routing rules.

Earlier native-domain successes remain real durability/lineage evidence but do not alone prove present overall success if current authority materially moved afterward.

The final compatibility proof:

- is bounded to participating sources and required dependency/authorization/routing footprint;
- creates no stored/global source cut;
- uses domain-native exact revisions/currentness evidence;
- revalidates only affected participating portions when one source moves.

## LAW WP13-16 — SAVE acknowledgement requires complete confirmed current closure

The runtime says/implies `saved` only after LAW WP13-15 succeeds for the full promised closure.

Prepared, attempted, rejected, ambiguous or historically durable-but-currently-incompatible state is not enough.

Failed explicit SAVE does not by itself invalidate coherent local/private established HOT; independent named HARD edges still govern continuation.

## LAW WP13-17 — SAVE quiescence has explicit terminal dispositions

### Success

After final current compatible composition proof:

- adopt covered source bases/generations;
- release local SAVE quiescence;
- continue from accepted current basis.

### Confirmed failed/abandoned SAVE while host survives

If coherent HOT remains usable, current native authority/dependency basis can be revalidated and no independent HARD edge blocks continuation:

- do not claim saved;
- safely abandon the SAVE attempt;
- release the local freeze after required revalidation;
- continue under Step-5.5 failure semantics.

### Indeterminate/unresolved authority

Keep only the affected dependent scope gated until currentness is established or owner rules permit safe abandonment against an accepted current basis.

No persistent lock/lease/host generation is introduced.

---

# 6. Campaign publication attempt

## LAW WP13-18 — Campaign publication attempt is immutable and ephemeral

Before the **first remote Git-object mutation**, deterministic Python/core freezes at least:

```text
repository identity
target campaign ref
trustworthy resolved acting principal + authorization evidence/basis
pinned authoritative HEAD H
base tree T(H)
frozen owner generations/revisions/fingerprints
campaign-domain durability roots
required recovery/reference/interpretation companions
bounded semantic read/dependency/currentness footprint
exact owner-authorized UPSERT/DELETE path operations
required derived index/projection companions
publication reason / named edge when applicable
```

Discovery of another required owner/path invalidates the attempt before publication.

The attempt is not persisted as a generic journal/transaction owner.

## LAW WP13-19 — Trustworthy acting principal is mandatory where application authorization requires it

Publication consumes a trustworthy resolved acting-principal/delegation identity from the admitted authentication/identity boundary.

These are insufficient by themselves:

- technical repository write capability;
- caller-supplied commit author/login metadata;
- arbitrary forgeable identity fields.

Creator/player/policy semantics remain owned by Access Control/native identity contracts.

If the supported host/Connector profile cannot supply required trustworthy principal evidence, return typed capability/authorization-unavailable failure and do not publish or try another transport.

## LAW WP13-20 — Authorization evidence is not a permission lease

Frozen authorization evidence does not override current authority.

Mutable PLAYER binding, mode, join policy, creator/policy grant, routing or another authorization dependency participates in the semantic conflict footprint and is revalidated at its owner-required pre-mutation boundary.

## LAW WP13-21 — WP-11 exact paths + required companions form the campaign delta

For each frozen native owner identity derive its exact WP-11 route or admitted fixed/exceptional route.

The path delta contains every owner-authorized UPSERT/DELETE plus every required derived discovery/index/projection companion that must share the campaign publication closure.

A derived index never becomes state authority or semantic absence proof.

DELETE-side index/projection effects are included when required by the current owner/index contract.

## LAW WP13-22 — Resulting-tree proof is bounded and pre-remote

Before the first remote Git-object mutation, local deterministic validation proves the planned resulting campaign tree satisfies:

- selected campaign-domain durable closure;
- exact owner/path identity constraints;
- directly touched recovery/index/routing/projection invariants;
- owner-required local completeness rules.

The proof uses frozen HOT/current owner state + pinned base evidence and is not a campaign-wide audit.

## LAW WP13-23 — Semantic no-ops are normalized

Byte-identical UPSERT and DELETE of an already absent path are removed.

Unchanged base-tree blobs remain byte-identical and are inherited rather than parsed/reserialized for convenience.

If the normalized campaign delta is empty, campaign-domain no-write still requires LAW WP13-13 current closure proof.

---

# 7. Fixed gameplay repository transport

## LAW WP13-24 — R2.6 fixed transport is binding shipped architecture

Supported gameplay/runtime repository publication is:

```text
deterministic Python/core
-> GitHub Connector Git-data/ref operations
-> authoritative non-force ref transition
```

This is current accepted cross-stage architecture, separate from development-agent transport rules in `AGENTS.md` / `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md`.

## LAW WP13-25 — No runtime alternate transport probing/fallback

Gameplay/setup/save/recovery/multiplayer publication SHALL NOT probe or fall back to:

- `gh` / GitHub CLI;
- shell/native remote Git;
- clone/fetch/pull/push/ls-remote/SSH Git;
- direct private HTTP/GitHub API/token workarounds;
- alternate GitHub App/MCP/custom backend/write service;
- GitHub Actions gameplay persistence bridge;
- transparent local-commit push assumptions;
- equivalent alternative transport paths.

Missing required Connector capability is a supported-profile capability failure.

## LAW WP13-26 — Ordinary existing-campaign Connector envelope

Given frozen H/T(H):

```text
1. deterministic Python/core prepares/finalizes the immutable attempt locally
2. Connector creates one base-derived tree T2 = T(H) + normalized delta
3. Connector probes/reads target ref
4. if still H, Connector creates one commit C(parent=H, tree=T2)
5. immediately request Connector ref transition to C with force=false
```

The preflight probe reduces avoidable orphan commits but is not final concurrency authority.

Only already-frozen deterministic finalization occurs in the post-preflight race window. No LLM calls, broad reads, external research or new semantic derivation occur there.

## LAW WP13-27 — One campaign durability boundary means one coherent tree + one parent commit

One logical campaign-domain durability boundary publishes its complete normalized path delta through one base-tree-derived tree and one single-parent gameplay commit.

Normal campaign publication does not use:

- per-file Contents mutations;
- merge commits;
- staging refs/commits;
- force update.

Storage default-branch metadata remains a separate storage-owner transaction.

---

# 8. Publication outcome epistemics

## LAW WP13-28 — Authority-changing final ref transition is tri-state

The final ref operation exposes exactly the epistemic distinction:

```text
CONFIRMED_ACCEPTED
CONFIRMED_REJECTED
INDETERMINATE
```

A capability/validation failure before dispatch is not a confirmed ref rejection.

## LAW WP13-29 — Broader native result preserves dispatch/cause class

A native durability operation may additionally return:

```text
NO_WRITE_NEEDED
FAILED_PREPUBLICATION
REVALIDATION_REQUIRED
CAPABILITY_FAILURE
AUTHORIZATION_FAILURE
CONFIGURATION_FAILURE
INFRASTRUCTURE_FAILURE
```

Exact names may differ, but implementation must preserve:

- whether the final authority-changing operation was dispatched;
- what is known about its result;
- the cause class needed for lawful retry/failure behavior.

## LAW WP13-30 — Confirmed accepted publication may be adopted without gratuitous reread

A confirmed accepted response selecting intended C establishes campaign publication at that response point.

The runtime may immediately adopt the returned commit/tree/source basis for covered generations. This is current operation evidence, not a lease against later movement.

## LAW WP13-31 — Confirmed rejection is classified before retry

A `CONFIRMED_REJECTED` final ref result SHALL be classified:

```text
STALE_OR_NON_FAST_FORWARD
    -> bounded currentness/semantic-footprint revalidation

AUTHORIZATION_REJECTED
    -> typed authorization failure; no automatic semantic retry until authority permits

CONFIGURATION_OR_RULE_REJECTED
    -> typed repository/profile configuration failure; no force/hidden-ref/per-file bypass

CAPABILITY_OR_INFRASTRUCTURE_REJECTED
    -> typed supported-profile/infrastructure failure; no alternate transport

UNCLASSIFIED_CONFIRMED_REJECTION
    -> fail closed as unresolved publication/infrastructure rejection
```

Only stale/currentness conflict enters normal repin/rebuild logic by default.

## LAW WP13-32 — Indeterminate result cannot be acknowledged, cleared or blindly retried

After `INDETERMINATE`:

- no SAVE/HARD success acknowledgement;
- no dirty-generation clear by assumption;
- no dependent correctness-edge release;
- no gameplay replay/reroll/reallocation;
- no blind second ref transition.

Perform targeted bounded authoritative verification when available.

## LAW WP13-33 — Ambiguity verification uses exact current ref + bounded lineage/current-closure evidence

Given intended C and current authoritative D:

```text
D == C
    -> prove required current closure at C

C proven reachable ancestor of D
    -> C is durable lineage evidence only
    -> inspect bounded D-vs-C intersection with required closure/dependency footprint
    -> accept only if current D supplies compatible current required closure

C proven absent from D lineage
    -> C does not prove current closure
    -> repin/revalidate from D

bounded evidence unavailable
    -> remain INDETERMINATE / recovery-required
```

Never restore stale C by force.

Prepared/unreachable object cleanup remains Step-5.13/host concern.

---

# 9. Currentness, conflict and retry

## LAW WP13-34 — Conflict footprint is semantic, not path-only

Campaign movement is classified against the frozen bounded footprint including as applicable:

```text
exact write paths
semantic owner/dirty roots
accepted read/dependency footprint
authorization/ownership/routing dependencies
required recovery/reference/interpretation dependencies
```

Different physical paths do not prove semantic independence.

## LAW WP13-35 — Proven-disjoint movement permits transport-only rebuild

If external movement is proven disjoint:

```text
adopt newer authoritative HEAD N
preserve established semantic result
preserve accepted IDs / fixed RNG / execution evidence
rederive exact path delta on T(N)
create a fresh immutable attempt
retry publication
```

No gameplay re-resolution occurs merely because Git base changed.

## LAW WP13-36 — Relevant overlap requires native-owner reconciliation/revalidation

If movement overlaps relevant state/dependencies, automatic reconciliation is allowed only when the affected native owner defines a deterministic safe relation/merge.

Otherwise return typed owner-specific revalidation/re-resolution.

Generic YAML/JSON/text merge, Git merge order or last-writer-wins is not semantic authority.

## LAW WP13-37 — Automatic retry is bounded

Repeated contention/revalidation SHALL NOT loop indefinitely.

After a bounded implementation-defined condition return typed unresolved synchronization/conflict outcome.

A named HARD edge remains unresolved. Deferrable local/private state retains Step-5.5 failure behavior.

## LAW WP13-38 — Git/storage order never establishes fictional chronology

Commit/ref/tree/path/ID order is repository publication evidence only and cannot decide simultaneous/contested fictional chronology.

Step 5.9 remains chronology authority.

---

# 10. Generation adoption and crash recovery

## LAW WP13-39 — Campaign publication adoption is exact-generation-specific

For every frozen native owner generation G covered by confirmed compatible publication:

```text
mark G durable under confirmed source basis
if current local generation == G:
    clear dirty membership for G
else:
    keep current newer G+1 dirty
```

Never blanket-clear a path/scope because an older frozen version published.

## LAW WP13-40 — Partial adoption cannot reset unrelated exposure

Only owner generations actually proven durable may leave the still-relevant unpublished set.

Scope exposure basis is preserved/recomputed from remaining dirty/recovery-relevant state.

Unrelated successful publication cannot reset another scope.

## LAW WP13-41 — Crash after remote success requires no generic publication journal

If remote/native publication succeeded but local bookkeeping/adoption was lost, cold recovery begins from actual current native authorities and exact pins.

Surviving SQLite/attempt metadata is not authority.

Do not replay gameplay merely to reconstruct lost local bookkeeping.

---

# 11. Native-domain integration boundaries

## LAW WP13-42 — Live authoritative establishment remains exact-source CAS

For live-claimed mutable consequences:

```text
prospective deterministic result
-> Step-5.8 exact-source live CAS native durability edge
-> confirmed accepted live authority
-> WP-12 local HOT adoption
```

WP-13 may include this native domain in SAVE/HARD composition but cannot replace it with campaign commit or SQLite transaction.

WP-16 owns final live physical machine/ref/schema/identity realization.

## LAW WP13-43 — Checkpoint never proves SAVE/publication/handoff success

Checkpoint is optional immutable recovery/maintenance evidence.

A valid SAVE/campaign publication may create no checkpoint. Checkpoint existence cannot establish current state, SAVE success or handoff success.

WP-14 owns final checkpoint/recovery machine repair.

## LAW WP13-44 — Session/local persistence bookkeeping is non-authoritative

Session `base_head_sha` / `last_published_head_sha`, local `known_head`/tree, dirty/exposure metadata and cached source bases are coordination/operation evidence only.

They cannot grant write authority, prove currentness alone or override current native-source validation.

## LAW WP13-45 — Storage metadata publication remains separate

`DND_STORAGE` baseline maintenance is a storage-owner operation and never joins campaign owner-state SAVE/publication as one transaction.

Success/failure of storage baseline and campaign publication remain independently real.

## LAW WP13-46 — Engine/rules maintenance consumes campaign publication

An owner-authorized engine/rules provenance/adoption delta may use the same campaign-domain publication protocol after its own compatibility/durability/access gates succeed.

WP-13 does not own runtime package selection or migration semantics.

A non-creator cannot gain MANIFEST adoption authority merely because the persistence transport can write.

---

# 12. Canonical explicit SAVE algorithm

For an explicit SAVE request:

```text
1. accept SAVE intent and determine selected promise scope under owning SAVE semantics
2. establish scoped local quiescence for affected mutable promise roots
3. freeze implicated current owner generations / dirty roots
4. derive complete required RRC-compatible durable source closure
5. partition closure by native durability domain
6. for each domain:
       establish operation-current source/currentness basis
       classify already-durable vs pending work
       if already durable -> NO_WRITE_NEEDED for that domain
       else execute its native publication protocol
       preserve confirmed accepted native results
       classify rejection/ambiguity/capability failures without fallback
7. after required domain operations, prove one current compatible source composition
   satisfying the promised closure at the acknowledgement boundary
8. if complete:
       generation-specifically adopt covered durability
       release SAVE quiescence
       acknowledge saved
9. if incomplete:
       do not acknowledge saved
       preserve every real accepted native publication
       revalidate/abandon/release local quiescence where owner rules allow
       keep only unresolved correctness-critical dependent scope gated
```

There is no distributed rollback.

---

# 13. Canonical campaign publication algorithm

For existing campaign HEAD H:

```text
A. PREPARE / FREEZE
   resolve trustworthy acting principal/application authority
   freeze exact owner generations + roots + dependencies + auth/currentness basis
   derive WP-11 exact UPSERT/DELETE + required index/projection companions
   prove bounded resulting-tree closure/invariants locally
   normalize semantic no-ops

B. NO-WRITE PATH
   if normalized delta empty:
       prove operation-current compatible campaign source closure
       -> NO_WRITE_NEEDED

C. REMOTE OBJECT PREPARATION
   resolve exact base tree T(H) before first remote object mutation
   Connector create base-derived T2

D. PREFLIGHT
   Connector read target ref
   if ref != H:
       classify bounded semantic footprint
       disjoint -> fresh attempt on N
       relevant -> owner-specific reconcile/revalidate
       other failure -> typed result

E. FINALIZE NARROW RACE WINDOW
   Connector create one commit C(parent=H, tree=T2)
   immediately Connector update_ref(C, force=false)

F. OUTCOME
   CONFIRMED_ACCEPTED
       -> exact-generation adoption / current source basis

   CONFIRMED_REJECTED
       -> classify stale vs auth/config/capability/infrastructure before retry disposition

   INDETERMINATE
       -> no ack/clear/replay/blind retry
       -> bounded exact current ref + lineage/current-closure verification
```

No alternate gameplay repository transport is attempted.

---

# 14. Current shipped-machine disposition

WP-13 does not edit implementation in this architecture step, but the following current surfaces are explicitly classified for later implementation/TDD.

| Surface | Canonical disposition |
|---|---|
| `GAME/CORE/DURABILITY_GUARD.md` | Preserve owner-routing/zero-I/O/no-heartbeat concepts; replace the noncanonical campaign-global one-hour / `durable_frontier_time` correctness policy with scope-relative accepted exposure policy; risk-control failure is not HARD by itself. |
| `GAME/CORE/SAVE_CONTRACT.md` | Preserve structured materialization/no-summary/no-checkpoint semantics; replace universal campaign-only `SAVE_ALL_DIRTY -> one CAMPAIGN_TREE_TXN` model with native-domain SAVE composition. Campaign-only SAVE remains one campaign transaction when it is the only pending native domain. |
| `GAME/CORE/PERSISTENCE.md` | Preserve base-tree/non-force/one-tree/one-parent/no-Contents campaign transaction discipline; add full frozen generation/auth/dependency footprint, exact result epistemics, rejection classification, disjoint-vs-overlap handling, bounded ambiguity proof and G-specific adoption. |
| `GAME/CORE/STORAGE.md` | Preserve storage/campaign separation and bounded reads; remove global durable-frontier-time authority. |
| `GAME/CORE/MULTIPLAYER.md` / `LIVE_SCENE.md` | Preserve owner semantics and route into Step-5.8; final live machine remains WP-16. |
| `GAME/CORE/ENGINE_UPDATES.md` | Consume canonical campaign publication after its own authorization/compatibility/durability gates; storage baseline remains independent. |
| current explicit-save/persistence/hourly tests | Preserve conforming sparse/transaction/integrity cases; rewrite stale campaign-only SAVE, blanket dirty clear and global-hourly assertions during implementation. |

---

# 15. Mandatory downstream verification obligations

Later approved implementation/TDD must prove at least:

1. semantic establishment cannot be created by persistence serialization;
2. no global one-hour/frontier/save-clock/HARD-queue architecture remains;
3. scope exposure follows actual oldest still-relevant unpublished state;
4. risk-control failure does not become HARD without a separate named edge;
5. closure differs from pending write set;
6. ordinary closure computation is bounded/native-routed;
7. explicit SAVE freezes one definite promise scope;
8. explicit SAVE composes native domains and does not invent global order/rollback;
9. domain no-write requires operation-current compatible closure;
10. partial native success remains real but cannot produce overall false save acknowledgement;
11. final SAVE success proves one current compatible participating-source composition;
12. SAVE quiescence releases only through safe success/abandonment/currentness rules;
13. frozen campaign attempt occurs before first remote object mutation;
14. frozen attempt includes exact owner generations, auth, reads/dependencies/currentness basis and exact path/index closure;
15. trustworthy acting principal is required and arbitrary commit author metadata cannot grant authority;
16. WP-11 record + required index/projection UPSERT/DELETE closure is coherent;
17. resulting-tree preflight is bounded and detects missing required path/invariant;
18. byte-identical/no-op paths do not create publication;
19. supported gameplay transport is Python/core -> GitHub Connector -> non-force ref transition only;
20. missing Connector capability never triggers alternate transport;
21. one campaign boundary produces one base-derived tree + one single-parent commit;
22. final ref outcome preserves ACCEPTED/REJECTED/INDETERMINATE distinction;
23. confirmed rejection cause is classified before retry;
24. indeterminate result cannot ack/clear/release/replay/blind-retry;
25. ambiguity uses bounded current-ref + lineage/current-closure proof;
26. disjoint source movement preserves accepted IDs/RNG/semantics and rebuilds transport basis only;
27. relevant overlap cannot use generic text merge as authority;
28. automatic retry is bounded;
29. G publication clears only G and preserves G+1;
30. partial/unrelated adoption cannot reset another dirty exposure basis;
31. crash after remote success/local adoption loss recovers from native authority without journal/gameplay replay;
32. live exact-source CAS remains live establishment authority;
33. checkpoint is optional and cannot prove SAVE/handoff/current state;
34. session/local cached HEAD fields are not authority;
35. storage baseline transaction is independent from campaign SAVE;
36. engine/rules maintenance uses campaign publication without broadening adoption authority;
37. Git/ref order cannot become fictional chronology;
38. current stale regression cases are dispositioned explicitly rather than preserved accidentally.

WP-22 and later approved implementation planning own executable realization of these obligations.

---

# 16. Forward obligations

| Target | WP-13 obligation |
|---|---|
| WP-14 | Recovery/checkpoint machine must consume current-authority-first sources; checkpoint remains optional/non-SAVE authority. |
| WP-16 | Live machine must preserve exact-source CAS, accepted/rejected/indeterminate outcomes, current source compatibility and fixed Connector path. |
| WP-19 / WP-20 | Bootstrap/migration may reuse publication protocol but cannot weaken exact authority/access/durability rules. |
| WP-22 | Implement full WP-13 conformance, concurrency, ambiguity, capability-failure and stale-machine regression coverage. |
| WP-24 | Measure publication/closure/Connector performance before optimization; no global timer/index partitioning assumption. |
| WP-26 | Existing Storage-v2 prose cleanup remains separate documentation consistency work. |
| implementation planning | Define exact Python APIs/local metadata/typed error codes/retry bounds under this canonical contract, then implement via TDD. |

---

# 17. Canonical closure state

Step-6 findings:

```text
F01 BLOCKING    final composed current-source proof
F02 BLOCKING    operation-current NO_WRITE_NEEDED proof
F03 SIGNIFICANT trustworthy acting-principal evidence
F04 SIGNIFICANT confirmed-rejection cause classification
F05 SIGNIFICANT SAVE quiescence release/abandonment
F06 SIGNIFICANT risk-control failure remains MAY_DEFER
```

All were mechanically resolved in Step 7 and incorporated here.

```text
STEP_6_BLOCKING:        2
STEP_6_SIGNIFICANT:     4
UNRESOLVED_BLOCKING:    0
UNRESOLVED_SIGNIFICANT: 0
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPENED:       NO
```

WP-13 architecture is ready for the mandatory final Senior audit.

WP-14 and implementation planning remain blocked until the required gate authorizes the next unit.