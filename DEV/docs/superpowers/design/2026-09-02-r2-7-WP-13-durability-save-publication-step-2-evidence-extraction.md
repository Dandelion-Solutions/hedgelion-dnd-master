# R2.7 WP-13 — Durability / SAVE / Publication — Step 2 Evidence Extraction

Status: **STEP 2 COMPLETE — EVIDENCE / COMPLETENESS GATE PASSED**

Date: 2026-09-02

Step-1 authority:

- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-task-brief.md`
- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-source-manifest.md`
- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-task-brief-critic.md`
- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-senior-recovery-fixed-gameplay-repository-transport.md`

This document records evidence only. It does not select a new architecture, begin implementation, start WP-14, or reopen accepted upstream decisions.

---

## 1. Reopen test

Step 2 found **no contradiction, unsatisfied new consumer or material insufficiency** in the accepted Step-5 / R2.6 / WP-11 / WP-12 architecture.

The current gap remains machine realization and stale shipped-contract reconciliation.

```text
UPSTREAM_ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED:              NO
```

---

## 2. R2.6 fixed gameplay repository transport

Current accepted cross-stage authority is:

```text
deterministic Python/core
    prepare/freeze exact semantic publication input
    own currentness/conflict/retry decision
        |
        v
GitHub Connector
    perform the supported Git-data/ref operations
        |
        v
authoritative non-force ref transition
```

Repository transport selection is closed.

The shipped gameplay/runtime must not probe, compare or fall back to `gh`, shell/native remote Git, clone/fetch/pull/push/ls-remote/SSH Git, direct private HTTP/GitHub API/token workarounds, alternate App/MCP/backend write services, GitHub Actions as a gameplay bridge, transparent local-commit push assumptions, or an equivalent alternate transport.

Missing required Connector capability is a **supported-profile capability failure**, not an alternate-transport trigger.

R2.7 must map the actual publication envelope and preserve integrated fixed-Connector currentness/CAS/conflict/ambiguous-failure/capability-failure coverage.

`AGENTS.md` and `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md` govern development-agent repository work only and are not gameplay architecture authority.

---

## 3. Step-5.1 / 5.2 source and closure evidence

### 3.1 Domain typing

Every correctness-relevant progress/revision/frontier claim is domain typed. No implicit order exists across campaign commit, live source revision, chronology evidence, checkpoint, session-observed HEAD, RNG frontier or another unrelated marker.

`durable_frontier_time` therefore cannot be repaired by renaming it into a universal frontier. Current campaign ref, live source revision and owner-generation dirtiness remain distinct axes.

### 3.2 Resumable Runtime Closure

RRC is a correctness property over compatible domain-native durable sources, not a first-class state owner or global snapshot.

For a promised durable point:

- every current owner/recovery dependency required for honest resume must be recoverable;
- root discovery is bounded and typed;
- transitive closure includes only correctness-required dependencies;
- derived caches/projections rebuild;
- already-durable compatible dependencies participate in closure proof without forced rewrite;
- lost unpublished HOT/SOFT state is never invented;
- campaign + live + operational durable sources may compose without a scalar cross-domain frontier.

No campaign-wide scan, global root registry, generic pending table or merged writable authority is admitted.

---

## 4. Step-5.3 / 5.4 execution-continuity and handoff evidence

Temporal/pending work keeps its native owner. Step 5.3 rejects a generic scheduler/job/pending ledger and requires continuous bounded recovery reachability when an acknowledged durable edge changes owner/root membership.

Accepted execution identity, fixed RNG and materialized mandatory child/firing identity survive retry/recovery. Persistence retry cannot use missing continuity as permission to replay mechanics.

Controlled handoff:

- freezes only affected mutation scope;
- promises actual durable compatible RRC, not attempted publication;
- may succeed without a heartbeat write when the closure is already durable;
- treats session records as coordination hints, not authority;
- does not create a global lease/lock;
- cannot acknowledge recovery-safe handoff on ambiguous or failed durability.

These constraints become named durability-edge inputs; WP-13 does not create a handoff owner.

---

## 5. Step-5.5 durability/SAVE evidence

The complete relevant law set yields the following machine obligations.

### 5.1 Establishment versus durability

```text
ESTABLISHED
    != necessarily DURABLE

SOFT
    = established + volatile/dirty + MAY_DEFER

HARD
    = MUST_BE_DURABLE_BEFORE(named edge)
```

HARD is edge-bound and owner-defined. There is no persistent `hard=true`, universal HARD queue or campaign-global save owner.

### 5.2 Scope-owned policy

Durability policy is attached to actual semantic/authority/visibility scope or partition.

There is no architecture-wide requirement for:

- one global dirty timeout;
- one scalar durability frontier;
- one cadence across independently writable scopes;
- one global save transaction.

Unpublished exposure is scope-relative and begins when still-relevant established/recovery state becomes unpublished. It is not measured from age of the last campaign commit alone.

### 5.3 Durable closure versus pending write set

Required durable source closure is larger than physical writes. It contains every native source/dependency needed for the promised recovery point; only the subset not already sufficiently durable enters the pending write set.

Closure begins from policy roots plus the policy-owned dirty accumulation scope and expands only correctness-required transitive dependencies.

### 5.4 Explicit SAVE

Successful explicit SAVE means every established gameplay-significant dirty root in the selected save scope plus required recovery/reference/interpretation dependencies is actually durable through a compatible set of native durable sources.

SAVE may compose multiple native durability domains. It is not one global transaction, one campaign commit, one total order or a distributed transaction.

The selected save scope is quiesced strongly enough that acknowledgement has one definite meaning; this is not a global host lock.

The runtime may say `saved` only when the entire promised closure is confirmed durable.

Already-durable clean SAVE requires no write.

Partial native success remains real: if A publishes and B fails, A remains authoritative while overall SAVE remains incomplete. No rollback/force rewrite is invented.

Failure of risk-control/explicit-save publication does not invalidate coherent local/private established HOT state, but a named correctness-critical edge cannot be falsely crossed.

### 5.5 Risk-control exposure

Risk-control exposure policy may request opportunistic publication at a suitable safe runtime point. Failure degrades protection but is not by itself a correctness barrier for deferrable private/local state.

No background execution implies no exact wall-clock flush guarantee. Clean state never produces heartbeat publication.

The current global one-hour `durable_frontier_time` contract is explicitly noncanonical.

---

## 6. Step-5.6 campaign-publication evidence

One campaign-domain durability transaction has this semantic shape:

```text
freeze exact attempt input
-> derive exact normalized UPSERT/DELETE delta
-> prove bounded resulting-tree completeness
-> base on exact pinned tree T(H)
-> optional early stale-ref probe
-> create one single-parent commit C(parent=H)
-> non-force ref transition
-> classify authority-changing outcome
-> generation-specifically adopt only confirmed durable state
```

### 6.1 Frozen attempt minimum basis

Before first remote Git-object creation the attempt freezes at least:

- repository identity / target ref;
- acting principal + application authorization basis;
- pinned authoritative HEAD/tree;
- durability roots for this domain;
- exact native owner generations/revisions/fingerprints;
- selected dirty/new/delete roots;
- required recovery/reference/interpretation companions;
- exact final path operations/content;
- bounded semantic read/dependency footprint;
- publication reason and named correctness edge where applicable.

A newly discovered required owner/path invalidates that attempt.

### 6.2 Resulting-tree proof

Before remote mutation, Python/core proves the planned resulting campaign tree is complete for the selected closure and directly touched invariants. Validation stays bounded to selected/touched/dependent scope; it is not a campaign-wide audit.

WP-11 adds that known IDs derive direct routes and a required discovery index update shares publication closure with its native record.

### 6.3 Physical publication

For an existing campaign, unaffected base-tree blobs are inherited exactly. Byte-identical UPSERT and absent DELETE normalize away. Empty normalized delta returns `NO_WRITE_NEEDED`.

One logical campaign publication boundary uses one tree + one single-parent gameplay commit. Merge commits and Contents-API per-file campaign publication are not the normal authority path.

Prepared blobs/tree/commit are non-authoritative until the authoritative ref selects their lineage.

### 6.4 Outcome epistemics

The final authority-changing operation exposes at least:

```text
CONFIRMED_ACCEPTED
CONFIRMED_REJECTED
INDETERMINATE
```

Confirmed success may be adopted without a redundant confirmation read.

Indeterminate outcome cannot be acknowledged, dirty-cleared, used to release a HARD edge, replayed or blindly retried. It requires bounded exact current-ref/lineage evidence where available.

Lineage evidence is distinct from current-closure proof. `C ancestor of D` proves durable lineage, not necessarily that C's values remain current. Only a compatible current required closure may satisfy the promise.

If bounded proof remains unavailable, ambiguity remains ambiguity.

### 6.5 HEAD movement

Conflict footprint includes physical paths plus semantic dirty roots, accepted reads/dependencies, authorization/routing and recovery/reference dependencies.

Proven disjoint movement permits transport-only rebuild on new authority while preserving accepted IDs, execution and fixed RNG.

Relevant overlap uses native-owner deterministic reconciliation if one exists; otherwise it returns owner-specific semantic revalidation/re-resolution. Generic YAML/text merge is not authority.

Automatic retries are bounded. Git conflict alone never rerolls.

### 6.6 Adoption

Confirmed compatible publication marks exactly frozen generation G durable. Dirty clears only when the current local generation is still G. G+1 remains dirty.

`known_head`, `known_tree`, dirty markers, exposure state and attempt state are bookkeeping, not authority.

No persistent generic publication journal is authorized.

---

## 7. Step-5.7 checkpoint boundary

Ordinary recovery is current-authority-first and may read zero checkpoints.

Checkpoint is optional immutable recovery/maintenance evidence. It is not current state, root registry, global frontier, SAVE proof or handoff proof.

Checkpoint absence does not invalidate a SAVE whose native durable closure is satisfied.

WP-14 owns checkpoint/recovery machine repair; WP-13 only preserves this boundary.

---

## 8. Step-5.8 live/native publication boundary

For live-claimed mutable authority:

- routing selects the exact live authority;
- every authoritative transition expects the exact prior source revision;
- exact-source CAS is the fence;
- accepted/rejected/indeterminate outcomes are explicit;
- shared consequence crosses write-before-reveal only after confirmed compatible publication;
- stale rejection invalidates prepared source state;
- live close is itself exact-source CAS;
- no TTL/heartbeat correctness dependency exists;
- campaign and live do not become one writable authority.

WP-12 further requires pre-CAS live prospective state to remain non-current and post-CAS SQLite to perform adoption only.

WP-13 may compose this native durability edge into SAVE/HARD promises. WP-16 still owns final live machine realization.

---

## 9. Step-5.14 integrated constraints

Step 5 is architecture-closed with zero unresolved architecture blockers.

The integration review confirms:

- source basis is domain-composed and ephemeral;
- campaign/live/execution markers are not a universal frontier;
- partial multi-live technical freezes are not partial fictional commitment;
- physical feasibility problems may restrict/reject a deployment profile but may not silently weaken accepted semantics;
- checkpoint/session/Story/routing/prepared objects remain non-authoritative;
- campaign/live CAS + ambiguity handling is an implementation-debt cluster, not a new architecture question.

R2.6 later resolves the repository-transport feasibility direction for the supported MVP by fixing the Connector path.

---

## 10. WP-11 / WP-12 realization constraints

### WP-11

- semantic identity derives one direct family-local route;
- path/index/shard order is never identity/currentness/chronology/authority;
- known-ID read never enumerates a directory or loads an index;
- each required discovery index remains derived;
- current discoverable record and required index update share publication closure;
- index absence cannot prove semantic absence;
- WP-11/F02 routes record+required-index publication closure directly to WP-13.

### WP-12

- SQLite is local HOT substrate only;
- dirty bookkeeping is owner-generation-specific and scope-relative;
- no global dirty generation, global `durable_frontier_time`, universal HARD queue, save clock or generic scheduler;
- frozen publication attempt carries source/currentness/auth basis, owner generations, closure, dependency footprint, path delta and reason;
- repository I/O occurs outside SQLite transactions;
- publication success clears exact frozen G only;
- live pre-CAS state remains prospective/non-current;
- post-CAS local adoption cannot roll back accepted remote authority;
- cold recovery begins from native durable authority, not surviving local bytes.

---

## 11. Current shipped machine/test classification

| Surface | Evidence | Step-2 disposition |
|---|---|---|
| `GAME/CORE/PERSISTENCE.md` | Base-tree `CAMPAIGN_TREE_TXN`, ref probe, single parent, non-force update, no mixed Contents API, no checkpoint implication are substantially aligned. It still inherits one-hour framing, uses an under-specified frozen snapshot, treats stale movement mostly as abort/rebuild, and says to clear the published dirty set without G qualification. | **PARTIAL / REALIZATION DEBT** |
| `GAME/CORE/SAVE_CONTRACT.md` | Strong structured-state/materialization/no-summary semantics are valuable, but `SAVE_ALL_DIRTY -> one CAMPAIGN_TREE_TXN` is campaign-centric and cannot represent accepted multi-native-domain SAVE composition; success/clearing is not generation-specific. | **PARTIAL / REALIZATION DEBT** |
| `GAME/CORE/DURABILITY_GUARD.md` | Correctly separates boundary classification from transport and protects zero-I/O turns/no heartbeat. Its global one-hour + `durable_frontier_time` rule is explicitly superseded by Step-5.5 scope-relative exposure semantics. Several named HARD boundaries are legitimate but their reason/roots belong to their owners. | **MIXED: VALID ROUTING + STALE GLOBAL POLICY** |
| `GAME/CORE/STORAGE.md` | Correct campaign/native storage separation, direct bounded reads and independent storage metadata transaction. Its `known durable-frontier time` remains stale global-timer debt. | **PARTIAL / REALIZATION DEBT** |
| `GAME/CORE/DIEGETIC_ONBOARDING.md` | `PROVISIONAL_IDENTITY` is a real named durability edge; it requires coherent durable protagonist/setup closure before further dependent fiction. | **CURRENT CONSUMER / EDGE OWNER** |
| `GAME/CORE/CHARACTER_READINESS.md` | READY_PC/PLAY_READY requires a confirmed durable reconstructable character frontier. | **CURRENT CONSUMER / EDGE OWNER** |
| `GAME/CORE/MULTIPLAYER.md` | Membership deactivation is explicit HARD; active-live deactivation composes live close/absorption with campaign membership write. Current one-file live details remain WP-16 debt. | **CURRENT CONSUMER + DOWNSTREAM LIVE DEBT** |
| `DEV/ARCHITECTURE/ACCESS_CONTROL.md` | Application authority is distinct from repository capability; uncertain authority denies write. | **CURRENT OWNER** |
| `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md` | Policy/grant adoption is campaign-persistent authority; mechanical grant/revoke is a named HARD access-control persistence boundary. | **CURRENT CONSUMER / EDGE OWNER** |
| `DEV/TESTS/EXPLICIT_SAVE_CASES.md` | S02/S09/S13/S14/S15/S17–S20 remain valuable. S01/S12 assume campaign-only SAVE; S16 blanket-clears included dirty records. | **MIXED TEST EVIDENCE / STALE EXPECTATIONS** |
| `DEV/TESTS/PERSISTENCE_TRANSACTION_CASES.md` | PT02–PT09/PT17/PT21–PT31 preserve useful campaign transaction invariants. PT10 blanket-clears dirty state; PT19 reflects old live realization. | **MIXED TEST EVIDENCE / STALE EXPECTATIONS** |
| `DEV/TESTS/test_hourly_durability_contract.py` | Directly asserts the rejected global one-hour frontier contract. | **STALE EXECUTABLE DEBT** |

No runtime/schema/test implementation is changed in WP-13 architecture work.

---

## 12. Newly activated direct consumer discovered in Step 2

`GAME/CORE/ENGINE_UPDATES.md` is a direct campaign-publication consumer, not merely a later migration owner:

- creator-authorized same-version provenance refresh may join the next otherwise-valid coherent campaign persistence transaction;
- true semantic-version adoption must first satisfy required durability/concurrency gates and then publish one coherent campaign metadata/data delta through `PERSISTENCE.md`;
- storage-baseline update remains a separate storage-owner transaction;
- successful campaign update cannot be claimed before required GitHub publication succeeds.

Therefore Step 2 activates:

- `GAME/CORE/ENGINE_UPDATES.md` — **REQUIRED WP-13 CONSUMER EVIDENCE**;
- `DEV/TESTS/ENGINE_UPDATE_CASES.md` — **REQUIRED TEST/DEBT EVIDENCE** for durability-before-maintenance, non-force conflict handling and independent storage/campaign transaction outcomes.

This does not start WP-20 migration design and does not reopen engine-update semantics.

No other inspected conditional consumer created a new WP-13 semantic owner.

---

## 13. Conditional owner routes triggered and bounded

### Step 5.1

Triggered by current `frontier` terminology. Inspection confirms domain typing/no implicit cross-domain order and that dirty set is not a frontier.

### Step 5.9

Triggered because current multiplayer/persistence prose can observe Git commit order during conflict handling. Inspection confirms Git/ref/ID/storage order never establishes fictional chronology. WP-13 therefore preserves that prohibition only; chronology design remains closed.

### Step 5.13

Triggered by prepared/unreachable commit artifacts after race/ambiguity. Inspection confirms unreachable/prepared object reclamation is cleanup/host-GC concern and never publication authority. WP-13 needs no GC protocol.

Step-5.10/5.11/5.12 were not promoted to direct WP-13 owners: Step-5.5/5.6/5.8 already supply the required projection/secrecy/write-before-reveal boundaries for this realization. They remain downstream/conditional evidence if later candidate wording touches their owned semantics.

---

## 14. Evidence matrix

| Boundary / flow | Semantic owner | Required durable roots / closure | Native durability domain | Result rule | Current debt / forward route |
|---|---|---|---|---|---|
| ordinary deferrable local state | Step 5.5 scope policy + native owners | still-relevant dirty owner generations + required RRC dependencies when policy requests flush | usually campaign ref for campaign-owned partition | failure may degrade RPO while coherent HOT continues | replace global one-hour timer with scope-relative exposure evaluation |
| `PROVISIONAL_IDENTITY` | `DIEGETIC_ONBOARDING.md` | established Player/Actor/setup/world/routing dependencies promised by edge | campaign | edge cannot be acknowledged before durable closure | preserve sparse early boundary, no universal flush semantics |
| READY_PC / PLAY_READY | `CHARACTER_READINESS.md` + lifecycle owner | reconstructable committed character closure + required routing/projections | campaign | activation/readiness edge waits for confirmed durability | exact WP-11 paths/index closure; no checkpoint requirement |
| explicit SAVE | Step 5.5 + `SAVE_CONTRACT` consumer | all selected established dirty roots + required recovery/reference/interpretation closure | composed native domains | ack only after all required domains confirmed durable | current contract is campaign-only; needs composite result |
| controlled handoff | Step 5.4 | promised RRC for affected scopes | composed native domains | recovery-safe ack only after compatible actual durability | session metadata cannot prove success |
| campaign publication | Step 5.6 | frozen campaign-domain portion of closure | campaign ref | accepted/rejected/indeterminate; non-force CAS-style selection | machine lacks full outcome/ambiguity/G-specific contract |
| membership/policy adoption | access/multiplayer/house-rules owner | affected native authority + authorization/routing dependencies | campaign, plus live close/absorption when applicable | deny uncertain authority; named HARD edge waits | current live realization later WP-16 |
| live shared mutation | Step 5.8 | exact live-native transition + required dependency basis | selected live source/ref | exact-source CAS accepted/rejected/indeterminate | final machine later WP-16; WP-13 only composes |
| engine/rules provenance/adoption | `ENGINE_UPDATES.md` + access owner | required pre-maintenance durable closure + authorized coherent campaign delta | campaign; storage baseline separate | no update success before confirmed publication | direct WP-13 consumer; migration mechanics remain WP-20 |
| clean SAVE / clean policy evaluation | Step 5.5/5.6 | already compatible durable closure | none | `NO_WRITE_NEEDED` / acknowledge guarantee | no heartbeat commit |
| partial multi-domain SAVE | Step 5.5/5.6 + native domain owners | each independently required domain | multiple | accepted domains remain accepted; overall promise incomplete until complete | requires composite native outcome, no distributed rollback |

---

## 15. Completeness gate

```text
[x] fresh branch/process/current-progress/roadmap/bootstrap read
[x] repaired Step-1 package + SR13-01 consumed
[x] R2.6 fixed gameplay transport sources extracted
[x] Step-3 retry/RNG/segment continuity inspected
[x] Step-5.1 frontier/domain typing inspected after trigger
[x] Step-5.2 RRC laws/qualifiers extracted
[x] Step-5.3 temporal/pending owner continuity inspected
[x] Step-5.4 handoff/quiescence/durability-success contract extracted
[x] Step-5.5 full relevant durability/SAVE law set accounted
[x] Step-5.6 full relevant publication/currentness/ambiguity law set accounted
[x] Step-5.7 checkpoint optionality/current-authority boundary extracted
[x] Step-5.8 live exact-source CAS boundary extracted
[x] Step-5.9 chronology prohibition inspected after trigger
[x] Step-5.13 prepared-object/cleanup boundary inspected after trigger
[x] Step-5.14 integrated closure inspected
[x] WP-11 F02 route/index closure extracted
[x] WP-12 dirty-generation/frozen-attempt/live-CAS handoff extracted
[x] Access / onboarding / readiness / multiplayer / policy consumers inspected
[x] current PERSISTENCE / SAVE / DURABILITY / STORAGE machine surfaces classified
[x] principal save/persistence/hourly tests classified
[x] new direct ENGINE_UPDATES consumer + tests added to manifest delta
[x] no architecture claim depends on roadmap/search snippet alone
[x] no unresolved contradiction/new consumer insufficiency remains
```

### Gate result

```text
SOURCE_MANIFEST_COMPLETE_FOR_STEP_3: YES
UNRESOLVED_EVIDENCE_GAPS:            0
UPSTREAM_REOPEN_REQUIRED:            NO
HUMAN_DECISION_REQUIRED:             NO
```

Step 3 may synthesize from this evidence.