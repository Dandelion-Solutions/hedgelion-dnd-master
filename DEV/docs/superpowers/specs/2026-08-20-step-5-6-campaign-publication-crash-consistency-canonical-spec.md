# Step 5.6 — Campaign Publication & Crash Consistency — Canonical Specification

Status: **CANONICAL — STEP 5.6 ARCHITECTURE CLOSED**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Owner-fixed repository boundary:

> **All runtime repository/GitHub work is owned and executed by deterministic Python core. LLM roles do not directly own repository publication.**

Canonical architecture direction:

> **PYTHON-OWNED SINGLE-REF CAS PUBLICATION**

Canonicalization basis:

- `../design/2026-08-20-step-5-6-campaign-publication-crash-consistency-task-brief.md`
- `../design/2026-08-20-step-5-6-campaign-publication-crash-consistency-research-draft.md`
- `../design/2026-08-20-step-5-6-campaign-publication-crash-consistency-analytical-challenge.md`
- `../design/2026-08-20-step-5-6-campaign-publication-crash-consistency-candidate-spec.md`
- `../design/2026-08-20-step-5-6-campaign-publication-crash-consistency-adversarial-review.md`
- `../design/2026-08-20-step-5-6-campaign-publication-crash-consistency-resolution-gate.md`

Step 5.6 defines physical campaign publication/crash-consistency semantics. It does not redefine Step-5.5 SOFT/HARD/SAVE meaning, Step-5.7 checkpoint/recovery selection, Step-5.8 live/campaign authority-transfer order, Step-5.9 fictional chronology, or later Story/transcript/delivery policy.

---

# 1. Canonical publication model

Within one ordinary campaign publication ref/domain:

```text
Step-5.5 required durable closure
        |
        v
PYTHON PERSISTENCE CORE
    freeze exact authority/dependency inputs
    derive complete pending path delta
    validate complete resulting campaign state
    normalize no-op paths
        |
        v
one base-tree-derived resulting tree
        |
        v
one single-parent commit C(parent = pinned H)
        |
        v
one non-force / fast-forward-only ref transition
        |
        v
confirmed durable campaign publication
```

This provides **single-ref authority atomicity**, not one network-atomic request.

Remote blobs/trees/commits may be prepared before the final ref transition. They are not campaign authority until selected by an authoritative ref lineage.

---

# 2. Canonical laws

## LAW 5.6-1 — PYTHON CORE IS SOLE RUNTIME REPOSITORY-TRANSPORT EXECUTOR

Runtime repository mutation SHALL be executed by deterministic Python core through a supported authenticated repository capability.

LLM roles SHALL NOT directly own:

- Git blob/tree/commit creation;
- campaign/live ref mutation;
- Git retry loops;
- repository conflict classification;
- ambiguous-write resolution;
- manual Base64 transport for semantic text;
- publication success determination.

LLM reasoning may contribute typed semantic intents/results upstream, but repository correctness cannot depend on natural-language reconstruction of a Git API sequence.

## LAW 5.6-2 — DEPLOYMENT MUST PROVIDE AUTHENTICATED `RepositoryPort`

Every runtime deployment profile that claims campaign persistence SHALL provide deterministic Python core a repository capability equivalent to:

```text
exact ref read
exact commit/tree/path read at pinned revision
bounded changed-path / ancestry comparison
base-tree-derived tree creation
single-parent commit creation
non-force ref transition
```

The capability SHALL preserve trustworthy acting-principal/delegated authorization evidence required by HDM policy.

Technical repository write permission is not gameplay authority.

Current built-in ChatGPT Data Analysis Python cannot itself make external web/API calls and therefore does not, by itself, satisfy this capability merely because ChatGPT has a connected app/plugin.

If a deployment lacks the required bridge, persistence is unavailable for that profile until a supported bridge exists. The runtime SHALL NOT fall back to LLM-owned Git choreography.

## LAW 5.6-3 — REPOSITORY CAPABILITY IS A PORT, NOT STATE AUTHORITY

`RepositoryPort` is a deterministic transport/capability boundary. It is not a new gameplay owner, recovery snapshot, transaction journal or generic cloud-storage authority.

The initial abstraction SHALL remain narrow to actual repository/Git requirements. Do not generalize to unrelated storage backends without a concrete requirement.

## LAW 5.6-4 — TRANSACTION INPUT IS FROZEN BEFORE REMOTE OBJECT MUTATION

Before the first remote Git object is created for one campaign publication attempt, Python core SHALL freeze and locally validate at least:

```text
repository identity
exact campaign target ref
acting principal + application authorization
pinned authoritative HEAD H
base tree T(H)
Step-5.5 durability roots relevant to this domain
exact frozen native owner generations/revisions or equivalent fingerprints
complete selected dirty/new/delete semantic roots
required reference/recovery/interpretation companions
final exact path operations/content
a bounded semantic read/dependency footprint
publication reason and named correctness edge where applicable
```

A newly discovered required path/owner after preparation invalidates the attempt. Do not publish it later as a second partial product commit.

## LAW 5.6-5 — RESULTING-TREE COMPLETENESS IS PROVEN LOCALLY BEFORE PREPARATION

Before remote object mutation, deterministic local validation SHALL prove that the planned resulting campaign tree contains every required companion needed by the selected closure and touched invariants.

Examples include, where applicable:

- new stable owner + required index entry;
- durable reference + referenced owner/materialization;
- CURRENT/routing target + required direct owner;
- root enrollment/routing evidence;
- checkpoint descriptor/pointer when independently required by the same edge;
- required operational/recovery records.

Validation remains bounded to selected/touched/dependent scope. It is not a campaign-wide audit.

## LAW 5.6-6 — REQUIRED DURABLE SOURCE CLOSURE IS NOT THE PHYSICAL WRITE SET

Already-sufficiently-durable dependencies participate in closure proof but SHALL NOT be rewritten merely because they are required dependencies.

Physical pending mutations are only the exact creates/updates/deletes necessary for this domain to satisfy its portion of the required closure.

## LAW 5.6-7 — PATH DELTA HAS EXPLICIT UPSERT/DELETE SEMANTICS

The normalized campaign delta conceptually consists of:

```text
UPSERT(path, exact content/blob)
DELETE(path)
```

An UPSERT byte-identical to the pinned base blob is removed.
A DELETE of an already-absent path is removed.

Semantic permission to delete a canonical owner is decided by the owner/lifecycle contract, not by transport.

## LAW 5.6-8 — EMPTY NORMALIZED DELTA CREATES NO COMMIT

After write-set normalization, if there is no actual path mutation or the resulting tree equals the pinned base tree:

```text
NO_WRITE_NEEDED
```

No heartbeat, timestamp-only commit, empty commit, checkpoint-only refresh or other repository mutation is created merely to update freshness bookkeeping.

## LAW 5.6-9 — EXISTING CAMPAIGN USES EXACT PINNED BASE TREE

For an existing campaign:

```text
T2 = exact T(H) + normalized semantic path delta
```

Every unaffected blob is inherited exactly.

Unchanged YAML/JSON/Markdown SHALL NOT be reserialized merely for convenience. Formatting drift alone is not semantic dirtiness.

Initial scaffold creation remains a separately owned from-scratch exception.

## LAW 5.6-10 — ONE LOGICAL CAMPAIGN DURABILITY TRANSACTION USES ONE TREE AND ONE COMMIT

All paths required by one logical campaign publication boundary SHALL enter one complete resulting campaign tree and one gameplay publication commit.

Do not create separate product commits for PC, CURRENT, indexes, LOG, scene, entity or other pieces of the same required campaign closure.

## LAW 5.6-11 — NORMAL CAMPAIGN PUBLICATION COMMIT IS SINGLE-PARENTED TO PINNED HEAD

Let pinned campaign HEAD be `H`.

Ordinary prepared campaign publication commit `C` SHALL have:

```text
exactly one parent
parent(C) = H
```

Normal publication SHALL NOT create merge commits to bypass semantic conflict resolution.

After authority movement, revalidate/reconcile first and construct a new single-parent result from the newly accepted authoritative HEAD.

## LAW 5.6-12 — PREPARED OBJECTS ARE NON-AUTHORITATIVE

Creating blobs, tree `T2`, or commit `C` does not change current campaign authority.

A prepared commit that never becomes reachable through the authoritative campaign ref lineage is not campaign canon.

Prepared/unreachable object cleanup belongs to Step 5.13.

## LAW 5.6-13 — PREFLIGHT REF PROBE IS ONLY AN EARLY-STALE OPTIMIZATION

Python core SHOULD probe the target ref after tree preparation and before commit creation to avoid known-stale commit creation and reduce orphan objects.

The probe is not the final concurrency guarantee because the ref may move immediately afterward.

## LAW 5.6-14 — FINAL STALE-WRITE GUARD IS SINGLE PARENT + NON-FORCE REF SELECTION

Final campaign publication safety is:

```text
parent(C) = pinned H
AND
update target ref -> C with force=false / fast-forward-only semantics
```

If another writer advances the branch from H before the final transition, a stale sibling C cannot overwrite that work via normal non-force publication.

Force update is forbidden.

## LAW 5.6-15 — AUTHORITY CHANGES ONLY AT AUTHORITATIVE REF SELECTION

`create_tree` success is not campaign durability success.
`create_commit` success is not campaign durability success.

Campaign authority changes only when the authoritative ref successfully selects a commit lineage containing the required current durable closure.

Readers see the old coherent ref-selected tree or the new coherent ref-selected tree, not a sequence of per-file campaign authority states.

## LAW 5.6-16 — FINAL REF OPERATION EXPOSES EPISTEMIC OUTCOME

Repository transport SHALL distinguish at least:

```text
CONFIRMED_ACCEPTED
CONFIRMED_REJECTED
INDETERMINATE
```

for the authority-changing operation.

A server-confirmed conflict/validation rejection is not the same as a lost/unknown response after dispatch.

Only `INDETERMINATE` enters ambiguity verification.

## LAW 5.6-17 — NORMAL CONFIRMED SUCCESS ADOPTS WITHOUT REDUNDANT CONFIRMATION READ

A confirmed accepted ref response identifying the selected commit is sufficient to establish that publication succeeded at that response point.

Python core MAY immediately update its last-known campaign frontier and covered durability bookkeeping without a gratuitous reread.

That last-known HEAD is not a lease. Later operations perform normal synchronization when their own concurrency policy requires it.

## LAW 5.6-18 — AMBIGUOUS REF OUTCOME CANNOT BE ACKNOWLEDGED OR BLINDLY RETRIED

After an indeterminate final ref operation, Python core SHALL NOT:

- say/imply `saved`;
- clear the frozen dirty generation by assumption;
- release a correctness-critical durability edge;
- replay gameplay semantics;
- blindly reissue publication without establishing actual current authority.

Targeted authoritative verification is required when available.

## LAW 5.6-19 — AMBIGUITY VERIFICATION USES BOUNDED EXACT LINEAGE EVIDENCE

Given intended commit `C` and current authoritative HEAD `D`, Python core MAY use a server-supported bounded exact compare/ancestry operation or equivalent repository evidence.

It SHALL NOT clone/pull or perform an unbounded history walk merely to resolve an ordinary acknowledgement ambiguity.

If bounded evidence is unavailable, the outcome remains ambiguous/recovery-required.

## LAW 5.6-20 — LINEAGE EVIDENCE AND CURRENT CLOSURE PROOF ARE DISTINCT

Ambiguity resolution interprets:

```text
D == C
    -> exact intended commit currently selected

C is reachable ancestor of D
    -> C is durable lineage evidence
    -> current D may have later changed/superseded C values

C not reachable from D
    -> C cannot by itself prove current durable closure
```

`C ancestor of D` alone SHALL NOT clear all dirty state or authorize continuation from stale local HOT state.

When `D != C`, Python core SHALL inspect/revalidate only D-vs-C changes relevant to the required closure and dependency footprint.

Only if current D provides a compatible current required durable closure may the durability promise/edge be treated as satisfied.

If D lawfully superseded C, D remains current authority. Never restore C merely to simplify acknowledgement.

## LAW 5.6-21 — UNEXPECTED NON-APPEND-ONLY HISTORY IS INTEGRITY EVIDENCE

Normal HDM campaign writers use non-force append-only publication.

If evidence suggests external force rewrite/history replacement, do not normalize it as ordinary optimistic concurrency and do not force C back into place.

Escalate affected scope to bounded integrity/recovery analysis.

## LAW 5.6-22 — UNRESOLVABLE AMBIGUITY REMAINS AMBIGUOUS

If current authoritative publication state cannot be proven:

- explicit save remains unconfirmed;
- unresolved dirty/exposure protection remains unresolved;
- correctness-critical durability edge remains blocked;
- Step-5.5 local/private friendly continuation MAY still apply where no independent hard edge exists;
- later suitable execution retries verification/republication from actual authority.

Do not invent either success or failure.

## LAW 5.6-23 — HEAD MOVEMENT IS CLASSIFIED USING BOUNDED SEMANTIC DEPENDENCIES

When authoritative HEAD moved from frozen H, conflict analysis SHALL consider a bounded footprint including, as applicable:

```text
physical write paths
semantic owner/dirty roots
accepted read/dependency footprint
authorization/ownership/routing dependencies
required recovery/reference dependencies
```

Different physical paths do not automatically imply semantic independence.

## LAW 5.6-24 — DISJOINT AUTHORITY MOVEMENT MAY USE TRANSPORT-ONLY REBUILD

If external changes are proven disjoint from the frozen transaction footprint, the established local semantic result remains valid.

Python core may:

```text
adopt new authoritative HEAD N
preserve accepted IDs/execution/RNG
rebuild the exact required delta on T(N)
retry publication
```

No gameplay re-resolution occurs merely because the Git base changed.

## LAW 5.6-25 — OVERLAP RECONCILIATION REQUIRES NATIVE OWNER SEMANTICS

When external changes overlap relevant state/dependencies, automatic reconciliation is permitted only if the affected native owner defines a deterministic safe reconciliation/merge rule.

No generic YAML/JSON/text merge becomes semantic authority.

Otherwise the persistence core returns a typed semantic revalidation/re-resolution requirement to the owning layer.

## LAW 5.6-26 — PERSISTENCE RETRY DOES NOT REPLAY ESTABLISHED GAMEPLAY BY DEFAULT

Repository conflict/retry operates on already-established state and stable execution/causal identities.

It SHALL preserve accepted IDs, fixed RNG experiment/results, receipts, temporal occurrence identities and committed semantic effects unless current authority invalidates the assumptions that made them applicable.

Git conflict alone never justifies rerolling.

## LAW 5.6-27 — SEMANTIC IDEMPOTENCY IS REQUIRED; PHYSICAL COMMIT IDENTITY IS NOT

Publication retry SHALL NOT duplicate gameplay semantics.

A retry MAY create a different resulting tree/commit SHA after base movement, reconciliation or write-set normalization.

Commit SHA/message/timestamp is not gameplay idempotency authority.

## LAW 5.6-28 — AUTOMATIC RETRY IS BOUNDED

Python core SHALL NOT loop indefinitely under repeated active contention.

After a bounded number/condition of automatic revalidation attempts, it returns a typed conflict/synchronization outcome to the owning workflow.

Exact retry count/backoff is implementation/configuration policy.

A correctness-critical dependent edge remains unresolved. Step-5.5 friendly local/private behavior remains applicable to non-hard risk-control/save failures.

## LAW 5.6-29 — AUTHORIZATION DEPENDENCIES ARE PART OF CONFLICT FOOTPRINT

If HEAD movement touches relevant PLAYER binding, campaign mode, join/access policy, creator-only policy, routing ownership or another authorization dependency, Python core SHALL revalidate application authorization before attempting publication against the new authority.

Successful technical Git credential use is not sufficient HDM authorization.

## LAW 5.6-30 — PYTHON BRIDGE MUST PRESERVE TRUSTWORTHY ACTING PRINCIPAL

A shared technical/service repository credential SHALL NOT silently become campaign/player authority.

The bridge must preserve trustworthy delegation/acting-principal evidence for existing application authorization rules.

If the selected bridge cannot preserve meaningful authenticated per-user Git authorship, machine realization must explicitly replace legacy rules that rely solely on technical commit `author.login` with a trusted application-principal mechanism. Arbitrary forgeable commit author metadata is not permission evidence.

## LAW 5.6-31 — POST-PREFLIGHT RACE WINDOW CONTAINS ONLY DETERMINISTIC FINALIZATION

After the final preflight ref check, the normal path SHOULD perform only already-frozen deterministic commit finalization and immediate ref transition.

Do not perform LLM calls, broad reads, new semantic derivation, external research or unrelated network work inside this narrow race window.

## LAW 5.6-32 — DIRTY CLEARING IS FROZEN-GENERATION-SPECIFIC

The publication plan freezes exact semantic owner/path generation/revision/fingerprint represented by its bytes.

On confirmed compatible publication:

```text
mark frozen generation G durable
clear dirty only if current local generation is still G
if a later generation G+1 exists:
    keep G+1 dirty
```

Never clear newer local work merely because an older frozen version published successfully.

Exact generation representation is implementation detail unless later machine design requires persisted fields.

## LAW 5.6-33 — LOCAL PUBLICATION BOOKKEEPING IS NOT AUTHORITY

`known_head`, `known_tree`, dirty markers, exposure clocks and attempt state are bookkeeping/recovery evidence, not duplicate gameplay owners.

If remote publication succeeded and the process dies before local clearing, cold recovery starts from actual authoritative repository/native sources.

Do not replay semantic gameplay merely because local bookkeeping was lost.

## LAW 5.6-34 — NO GENERIC PERSISTENT PUBLICATION JOURNAL IS INTRODUCED

Step 5.6 does not add a generic persisted publication/transaction journal solely to survive crash after remote success.

Native owners + repository authority + existing Step-3 idempotency/recovery identities remain the basis.

A later Step-5.7 or implementation finding may reopen this only with concrete evidence that current sources cannot resolve a required recovery case.

## LAW 5.6-35 — MULTI-DOMAIN PUBLICATION IS COMPOSED, NOT DISTRIBUTED-ATOMIC

When one durability promise spans independent native domains A/B:

```text
A publishes successfully
B fails
```

then:

- A remains real durable authority;
- the overall promise remains incomplete until required compatible current sources hold;
- actual A/B source composition is revalidated before dependent continuation;
- no rollback/force rewrite of A occurs merely to emulate a global transaction.

Exact live/campaign authority-transfer ordering/fencing remains Step 5.8.

## LAW 5.6-36 — CHECKPOINT CREATION IS NOT IMPLIED BY PUBLICATION

A normal campaign publication does not create a checkpoint.

If Step-5.7 policy independently requires checkpoint descriptor/pointer changes as part of the same durability edge and those paths are owned by the same campaign ref, they SHOULD join the same campaign tree transaction so that edge does not expose an avoidable same-ref partial state.

Otherwise checkpoint state may be absent or lag according to its owner.

## LAW 5.6-37 — NONCANONICAL PROJECTIONS DO NOT AUTOMATICALLY JOIN THE CAMPAIGN COMMIT

Story/transcript/render freshness is not forced by ordinary campaign publication.

Only projection/evidence material independently required by current recovery closure joins the physical campaign delta.

Steps 5.10–5.12 own normal projection durability, retention and delivery.

## LAW 5.6-38 — REPOSITORY CONFIGURATION FAILURE HAS NO UNSAFE FALLBACK

If repository permissions/rules/branch configuration reject the required non-force publication path, return a typed infrastructure/authorization failure.

Do not bypass through:

- force push;
- hidden alternate authority ref;
- per-file Contents publication;
- LLM Git fallback.

## LAW 5.6-39 — LOCAL PER-REF SERIALIZATION IS AN OPTIMIZATION ONLY

Python implementation MAY use an in-process per-repository/ref mutex to prevent self-induced overlapping publication attempts.

It does not replace remote non-force concurrency validation because other hosts/users/processes may write the same ref.

## LAW 5.6-40 — GIT STORAGE ORDER IS NOT FICTIONAL CHRONOLOGY

Campaign commit/ref order proves repository publication order only.

It SHALL NOT by itself establish fictional chronology for simultaneous/contested/cross-scene actions. Step 5.9 owns temporal reconciliation.

---

# 3. Canonical conceptual interface

Exact Python names are not fixed by architecture, but machine realization SHALL preserve equivalent separation:

```text
DurabilityRequest
    reason
    selected durability domain/scope
    named correctness-critical edge?
    required roots/closure evidence

FrozenPublicationAttempt       # in-process value; not mandatory persisted record
    repository/ref
    acting principal / authorization evidence
    pinned head/tree
    frozen owner generations
    exact UPSERT/DELETE path delta
    bounded semantic dependency footprint
    prepared tree/commit identities as produced

RepositoryPort
    exact ref/object/path reads
    bounded compare/ancestry
    create base-derived tree
    create one-parent commit
    non-force ref update with accepted/rejected/indeterminate outcome

PublicationOutcome
    NO_WRITE_NEEDED
    CONFIRMED_PUBLISHED
    CONFLICT_REVALIDATION_REQUIRED
    FAILED_PREPUBLICATION
    AMBIGUOUS
```

No universal persistent `PublicationPlan` class/record is required.

---

# 4. Canonical normal publication algorithm

Given current accepted campaign HEAD `H`:

```text
1. validate repository role/ref + acting principal/application authority
2. freeze selected Step-5.5 roots, owner generations and dependency footprint
3. derive campaign-domain required durable-source evidence
4. derive exact final UPSERT/DELETE path set
5. prove resulting-tree closure/invariants locally
6. normalize byte-identical/already-absent/no-longer-required operations
7. if no mutations remain:
       return NO_WRITE_NEEDED
8. resolve exact T(H)
9. prepare one T2 from T(H) + full normalized delta
10. if T2 == T(H):
       return NO_WRITE_NEEDED
11. preflight-read target ref
12. if ref != H:
       classify changed footprint
       revalidate authorization/dependencies
       transport-rebuild or return semantic revalidation requirement
13. create one commit C with parent(C)=H and tree(C)=T2
14. immediately request non-force ref transition -> C
15. CONFIRMED_ACCEPTED:
       publication succeeded at C
       generation-specifically adopt covered durability
16. CONFIRMED_REJECTED:
       classify conflict/infrastructure result
       repin/revalidate as appropriate
17. INDETERMINATE:
       do not ack/clear/replay
       perform bounded current-ref + lineage/current-closure verification
```

Automatic conflict retries are bounded.

---

# 5. Canonical ambiguity algorithm

Given intended prepared `C` after indeterminate ref operation:

```text
read current authoritative HEAD D

if D == C:
    prove required current closure at C
    -> CONFIRMED_PUBLISHED if compatible

else if bounded evidence proves C is ancestor/reachable in D lineage:
    C is durable lineage evidence
    inspect only D-vs-C changes intersecting required closure/dependency footprint
    if current D provides compatible required closure:
        adopt D as current authority
        -> CONFIRMED_PUBLISHED for the promise
    else:
        -> CONFLICT_REVALIDATION_REQUIRED

else if bounded evidence proves C not in current lineage:
    C does not prove current closure
    adopt/repin D
    -> conflict/revalidation/republication as required

else:
    -> AMBIGUOUS
```

No outcome restores stale C by force.

---

# 6. Crash-consistency matrix

| Failure/crash point | Authoritative state | Canonical response |
|---|---|---|
| before remote preparation | existing ref HEAD | retry/replan from accepted source |
| tree created, crash | existing ref HEAD | tree non-authoritative/orphan candidate |
| preflight sees HEAD movement | new external HEAD | no stale commit; dependency-aware revalidation |
| commit C created, crash before ref | current ref HEAD | C non-authoritative |
| final update confirmed rejected | current ref HEAD | C non-authoritative; bounded conflict/infrastructure handling |
| final update confirmed accepted | C was selected | publication success; no routine reread |
| update outcome lost | unknown | AMBIGUOUS until bounded verification |
| ambiguity D==C | C current | compatible closure confirms publication |
| ambiguity C ancestor of D | D current | lineage evidence + current closure revalidation |
| ambiguity C not in D | D current | C does not satisfy current closure proof |
| remote success, process crashes before local clearing | repository/native source is authority | cold recovery from actual source; no gameplay replay |
| later local G+1 after frozen G | remote may contain G | clear G only; G+1 remains dirty |
| repeated active contention | moving authority | bounded retry then typed sync/conflict outcome |
| campaign succeeds, other native domain fails | campaign success remains real | composed promise incomplete; revalidate actual source composition |

---

# 7. Explicit save consequences

Step-5.5 explicit-save semantics remain unchanged.

Within the campaign domain, explicit save materializes every selected established dirty campaign root + required campaign-domain dependencies into one complete campaign commit or proves that no write is needed because the required state is already durable.

Player-facing `saved` may be acknowledged only when the complete required multi-domain current durable closure is proven compatible.

A failed/ambiguous publication does not falsely acknowledge save and does not invent gameplay rollback. Friendly local/private continuation remains governed by Step 5.5.

---

# 8. Multiplayer/concurrency boundary

Step 5.6 defines only generic campaign publication conflict mechanics.

It does not decide live-epoch ownership transfer order.

For ordinary campaign HEAD movement:

```text
external change disjoint from write + semantic dependency + auth/recovery footprint
    -> preserve established result; transport-only rebuild allowed

owner-defined deterministic compatible overlap
    -> use owner reconciliation

material dependency/owner overlap without safe owner rule
    -> semantic revalidation/re-resolution required
```

Git text merge and commit order do not settle fictional conflict semantics.

Step 5.8 supplies concrete live/campaign authority/fencing/compaction rules.

---

# 9. Host/deployment prerequisite

Current external platform evidence establishes a concrete implementation dependency:

- OpenAI Help Center, `Data analysis with ChatGPT`: built-in Python data-analysis environment cannot make external web requests or API calls.
- OpenAI Help Center, `Developer mode and MCP apps in ChatGPT`: external write-capable integrations are separate app/MCP host capabilities and availability depends on supported product/workspace configuration.

Therefore:

> Python-owned repository transport is canonical, but a supported authenticated Python-to-repository bridge is a prerequisite for any deployable persistence-capable runtime profile.

This requirement must be feasibility-tested before implementation/release.

Step 6 should carry the host/deployment capability check alongside its existing platform/orchestration feasibility work.

No current architecture claim asserts that plain built-in ChatGPT sandbox Python alone can satisfy it.

---

# 10. Explicit implementation debt / required future tests

After the architecture sequence closes, machine realization must include focused tests for at least:

```text
clean NO_WRITE_NEEDED
one/many dirty paths -> one campaign commit
resulting-tree companion completeness
normalized empty delta suppression
stale preflight HEAD
post-commit ref race
confirmed ref rejection
lost ACK with D == C
lost ACK with C ancestor of D and compatible current closure
lost ACK with C ancestor of D but relevant later change
C absent from current lineage
bounded ambiguity verification
post-success process crash
semantic retry without reroll/re-execution
generation-specific dirty clearing
newer local generation survives older publication
authorization dependency changed concurrently
shared-credential acting-principal enforcement
bounded repeated contention
partial multi-domain success
checkpoint same-ref inclusion only when independently required
Python-only repository transport ownership
host RepositoryPort unavailable
no force push
no heartbeat/no-op commit
```

Current prose/string tests are insufficient evidence for the future Python transaction engine; executable deterministic failure-injection tests are required during implementation.

---

# 11. Deferred adjacent ownership

Step 5.6 deliberately leaves:

- exact checkpoint/recovery cut and hydration — Step 5.7;
- live/campaign authority transfer, fencing, compaction/rollover — Step 5.8;
- chronology reconciliation — Step 5.9;
- Story durability — Step 5.10;
- transcript retention — Step 5.11;
- host delivery/disclosure acknowledgement — Step 5.12;
- orphan object/ref cleanup — Step 5.13;
- full recovery/concurrency end-to-end challenge — Step 5.14;
- concrete Python module/package/bridge implementation — integrated implementation planning after architecture.

---

# 12. Step-5.6 closure statement

Step 5.6 closes with the following physical durability guarantee:

> Within one campaign Git ref, HDM prepares one complete validated resulting tree and one single-parent commit from a pinned authoritative HEAD. Prepared objects have no gameplay authority. A non-force ref transition is the authority-changing race guard. Confirmed success may be adopted without redundant reread; indeterminate success is resolved through bounded current-ref/lineage plus current-closure verification. Conflicts preserve established semantic identities and trigger bounded dependency-aware revalidation rather than blind merge, force push or gameplay replay. Repository transport is executed by deterministic Python core through a trustworthy authenticated host capability.

No Step-5.6 owner-level blocker remains. The Python-to-repository host bridge is an explicit deployment feasibility prerequisite, not an unresolved transaction-semantic decision.