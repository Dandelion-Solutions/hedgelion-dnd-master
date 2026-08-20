# Step 5.6 — Campaign Publication & Crash Consistency — Candidate Specification

Status: **CANDIDATE — ADVERSARIAL REVIEW REQUIRED**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Architecture direction:

> **PYTHON-OWNED SINGLE-REF CAS PUBLICATION**

This candidate formalizes physical campaign publication only. Step 5.5 remains authority for SOFT/HARD/SAVE meaning and required durable closure. Step 5.7 owns checkpoint/recovery selection. Step 5.8 owns exact live/campaign authority-transfer semantics.

---

# 1. Core invariant

All runtime repository mutation is executed by deterministic Python core through an authenticated repository capability. LLM roles do not own Git/GitHub transport.

Within one ordinary campaign publication domain/ref:

```text
Step-5.5 required durability closure
    -> deterministic pending write set
    -> one base-tree-derived resulting tree
    -> one single-parent commit
    -> one non-force authoritative ref transition
```

The ref transition provides maximal **authority atomicity** for the campaign domain. Git object preparation itself is not a network-atomic transaction and may leave unreachable objects after failure/race.

---

# 2. Canonical-candidate laws

## LAW 5.6-1 — PYTHON CORE OWNS REPOSITORY TRANSPORT

Runtime Git/repository mutation, conflict classification, ambiguity handling, retry orchestration and publication adoption SHALL be deterministic Python-core responsibilities.

LLM roles SHALL NOT directly:

- create repository blobs/trees/commits;
- update/delete refs;
- perform transport retry loops;
- construct backend wire payloads;
- manually Base64-encode textual repository payloads;
- infer durability success from natural-language/tool-call impressions.

Higher layers may request durability through typed semantic/runtime interfaces but do not own backend call sequencing.

## LAW 5.6-2 — HOST MUST PROVIDE AUTHENTICATED REPOSITORY CAPABILITY

The runtime host SHALL provide Python core an authenticated `RepositoryPort` or equivalent deterministic capability sufficient for exact repository/ref operations required by this specification.

The port MUST preserve trustworthy acting-principal/delegated authorization context; technical repository access alone is not gameplay authority.

Built-in ChatGPT data-analysis Python, which currently cannot issue external web/API requests, is not by itself evidence that this capability exists.

If a deployment profile cannot provide the required capability, campaign persistence is unsupported in that profile until the capability is supplied. The runtime SHALL NOT silently fall back to LLM-owned Git choreography.

## LAW 5.6-3 — REPOSITORY PORT IS NARROW, NOT GENERIC STORAGE AUTHORITY

The initial runtime port SHALL expose repository/Git semantics required by current HDM architecture, such as exact ref reads, pinned object/path reads, bounded compare/ancestry checks, tree creation, commit creation and non-force ref transition.

It is not a generic cloud-storage abstraction and does not become gameplay-state authority.

## LAW 5.6-4 — TRANSACTION INPUT FREEZES BEFORE REMOTE MUTATION

Before creating remote Git objects for one campaign publication attempt, Python core SHALL freeze/revalidate as applicable:

```text
repository identity
exact target ref
acting principal + application authorization
pinned authoritative HEAD H
base tree T(H)
Step-5.5 durability roots for this domain
frozen native owner generations/revisions
complete semantic dirty/new/delete roots selected for the attempt
required recovery/reference/interpretation dependencies
final exact intended path contents/deletions
a bounded semantic read/dependency footprint
publication reason / named correctness edge if applicable
```

If later local semantic work changes material included in the frozen plan before publication, the affected plan is invalidated/rebuilt rather than patched ad hoc after preparation.

## LAW 5.6-5 — REQUIRED DURABLE CLOSURE IS DISTINCT FROM PENDING WRITE SET

Required dependencies that are already sufficiently durable at the pinned compatible source set participate in closure proof but SHALL NOT be rewritten merely because they are dependencies.

The pending write set contains only material that must change/create/delete to make this campaign domain satisfy its portion of the Step-5.5 closure, including required dirty companion indexes/routing/provenance.

## LAW 5.6-6 — NORMALIZED EMPTY DELTA PRODUCES ZERO REPOSITORY MUTATION

Before commit creation, Python core SHALL eliminate path mutations that are byte-identical/no-longer-required after current validation.

If the resulting pending write set is empty or the resulting tree equals the pinned base tree:

```text
outcome = NO_WRITE_NEEDED
```

No tree/commit/ref heartbeat or timestamp-only mutation is created.

Stale local dirty bookkeeping is repaired independently of repository mutation.

## LAW 5.6-7 — EXISTING CAMPAIGN PUBLICATION PRESERVES BASE TREE EXACTLY

For an existing campaign, resulting tree construction uses the exact pinned HEAD tree as `base_tree`/equivalent and applies only the validated semantic path delta.

Unchanged blobs are inherited exactly. Parsing/reserializing an unchanged YAML/JSON/Markdown path is not allowed merely for convenience.

The initial scaffold remains the separately owned from-scratch exception.

## LAW 5.6-8 — ONE LOGICAL CAMPAIGN PUBLICATION USES ONE RESULTING TREE AND ONE COMMIT

All paths required by one logical campaign durability transaction SHALL be represented together in one resulting campaign tree and one gameplay publication commit.

Do not split PC/CURRENT/index/LOG/entity/companion paths into separate product commits when they form one closure.

## LAW 5.6-9 — NORMAL CAMPAIGN PUBLICATION COMMIT HAS EXACTLY ONE PARENT

Let `H` be pinned campaign HEAD. The prepared ordinary campaign publication commit `C` SHALL have exactly one parent and that parent SHALL equal `H`.

Normal campaign publication does not use merge commits to bypass semantic conflict resolution.

If external authority moved, reconcile/revalidate against the new authoritative source first, then prepare a new single-parent commit from that source.

## LAW 5.6-10 — PREPARED GIT OBJECTS ARE NOT CAMPAIGN AUTHORITY

Blob/tree/commit object creation does not advance campaign current-state authority.

A prepared/unreachable object MAY exist after failure/race and is not gameplay canon merely because its SHA is known.

Garbage/orphan cleanup policy belongs to Step 5.13.

## LAW 5.6-11 — PREFLIGHT REF PROBE IS AN OPTIMIZATION, NOT FINAL RACE AUTHORITY

A ref probe after tree preparation and before commit creation SHOULD be used to avoid creating a commit already known to be stale.

However the final concurrency guard is the combination of:

```text
C.parent == pinned H
update_ref(C, force=false) / equivalent fast-forward-only selection
```

The ref may move after preflight; no correctness assumption may depend on the probe remaining current.

## LAW 5.6-12 — AUTHORITY CHANGES ONLY AT SUCCESSFUL NON-FORCE REF SELECTION

For one campaign ref, current authoritative campaign revision remains the old ref-selected commit until a successful non-force transition selects the complete new commit.

`create_tree` success is not save success.
`create_commit` success is not save success.

A prepared commit rejected by the final ref transition remains non-authoritative.

## LAW 5.6-13 — FORCE UPDATE IS FORBIDDEN FOR NORMAL/RECOVERY CAMPAIGN PUBLICATION

Concurrency conflict, stale state, ambiguous acknowledgement or retry SHALL NOT be resolved by force-updating campaign/live refs.

Unexpected history rewrite is integrity/recovery evidence, not a normal retry mechanism.

## LAW 5.6-14 — TRANSPORT OUTCOME MUST PRESERVE EPISTEMIC STATUS

The repository capability SHALL distinguish at least:

```text
CONFIRMED_ACCEPTED
CONFIRMED_REJECTED
INDETERMINATE
```

for the authority-changing operation.

A server-confirmed rejection and a lost/unknown response are not equivalent.

Only `INDETERMINATE` enters ambiguity resolution.

## LAW 5.6-15 — NORMAL CONFIRMED SUCCESS REQUIRES NO CONFIRMATION REREAD

When the authority-changing ref operation returns a confirmed accepted result identifying the selected commit/ref state, Python core may adopt that result without an immediate redundant ref/file reread.

Targeted reads are reserved for ambiguity, conflict, explicit resync/recovery or another actual dependency reason.

## LAW 5.6-16 — AMBIGUOUS REF OUTCOME MUST BE VERIFIED BEFORE SAVE ACKNOWLEDGEMENT

If final ref selection outcome is indeterminate, Python core SHALL NOT:

- say/imply `saved`;
- clear the corresponding frozen dirty generation merely by assumption;
- replay gameplay semantics;
- blindly retry the ref update without determining current authority.

It SHALL perform targeted authoritative verification when available.

## LAW 5.6-17 — AMBIGUITY RESOLUTION SEPARATES HISTORICAL PUBLICATION FROM CURRENT COMPATIBILITY

Given intended prepared commit `C` and current authoritative HEAD `D` after an indeterminate update:

```text
D == C
    -> historical publication proven; current head = C

C reachable as ancestor of D
    -> C entered current authoritative lineage
    -> historical publication proven
    -> current compatibility still requires targeted D-vs-C revalidation

C not reachable from D
    -> C cannot satisfy current durable-source proof
    -> repin/revalidate D; do not claim successful current closure from C
```

Ancestry does not prove C's values remain current in D; later valid commits may supersede them.

Unexpected non-append-only history is escalated to integrity/recovery handling rather than repaired by force rewrite.

## LAW 5.6-18 — UNRESOLVABLE AMBIGUITY REMAINS AMBIGUOUS

If authoritative verification is unavailable after an indeterminate outcome:

- save remains unconfirmed;
- corresponding dirty/exposure protection remains unresolved;
- correctness-critical durability edge remains blocked;
- coherent local/private HOT play MAY continue only as permitted by Step 5.5;
- later suitable execution retries verification/republication from actual authority.

Do not invent success or failure.

## LAW 5.6-19 — HEAD MOVEMENT USES BOUNDED DEPENDENCY-AWARE CLASSIFICATION

When the authoritative campaign HEAD changes relative to a frozen publication base, Python core compares external change footprint against the bounded transaction footprint comprising, as applicable:

```text
physical write paths
semantic dirty/native owner roots
accepted read/dependency footprint
authorization/ownership/routing dependencies
required recovery/reference dependencies
```

Path disjointness alone does not prove semantic independence.

## LAW 5.6-20 — DISJOINT EXTERNAL CHANGES MAY USE TRANSPORT-ONLY REBUILD

If external changes are proven semantically disjoint from the frozen transaction footprint, the already-established local semantic result remains valid.

Python core may:

```text
adopt new authoritative HEAD N
preserve established IDs/execution/RNG
rebuild exact delta onto T(N)
retry publication
```

No gameplay re-resolution is required merely because the physical base commit changed.

## LAW 5.6-21 — OVERLAP RECONCILIATION MUST BE OWNED, NOT GENERIC TEXT MERGE

If overlap exists, Python core may reconcile automatically only when the affected native owner contract defines a deterministic safe reconciliation/merge for that overlap.

No generic YAML/JSON/text merge is semantic authority.

Absent an owner-defined safe reconciliation, return targeted semantic revalidation/re-resolution requirement.

## LAW 5.6-22 — PERSISTENCE CONFLICT MUST NOT REPLAY ESTABLISHED SEMANTICS BY DEFAULT

Repository conflict/retry operates on existing established state and stable execution/causal identities.

It SHALL preserve accepted IDs, fixed RNG values/experiments, receipts and established transitions unless current authoritative changes invalidate the semantic assumptions that made them applicable.

A new random draw is not justified merely by Git conflict.

## LAW 5.6-23 — SEMANTIC IDEMPOTENCY IS REQUIRED; COMMIT-SHA IDEMPOTENCY IS NOT

The same established semantic result SHALL NOT be duplicated by publication retry.

A retry MAY legitimately produce a different tree/commit SHA after base-head movement or normalized write-set change.

Commit message/timestamp/SHA is not gameplay idempotency authority.

## LAW 5.6-24 — DIRTY ADOPTION/CLEARING IS GENERATION-SPECIFIC

Publication freezes exact native owner/path semantic generations or equivalent fingerprints represented by the prepared bytes.

After confirmed publication:

```text
mark frozen generation G durable
clear dirty for owner/path only if current local generation is still G
if a later generation G+1 exists, keep G+1 dirty
```

Do not clear an entire path/owner merely because an older frozen version was published.

Exact representation of dirty generation is an implementation detail unless later schema work requires persistence.

## LAW 5.6-25 — LOCAL BOOKKEEPING IS NOT AUTHORITY

`known_head`, `known_tree`, dirty flags, exposure clocks and publication-attempt metadata are local/recovery bookkeeping, not duplicate gameplay state owners.

If remote publication succeeded and process crashes before local adoption, cold recovery starts from actual authoritative repository/native sources.

Do not replay gameplay merely because local post-write bookkeeping was lost.

## LAW 5.6-26 — NO GENERIC PERSISTENT PUBLICATION JOURNAL IS REQUIRED

Step 5.6 introduces no mandatory persistent transaction/publication journal solely to survive crash between remote success and local adoption.

Existing native authority + Step-3 idempotency/recovery identities remain the recovery basis. Revisit only if later Step-5.7/implementation evidence proves a journal is necessary.

## LAW 5.6-27 — MULTI-DOMAIN SUCCESS IS COMPOSED, NOT DISTRIBUTED-ATOMIC

When one Step-5.5 promise requires native domains A and B:

```text
A succeeds
B fails
```

then:

- A remains real durable authority;
- overall composed promise remains incomplete until required compatible source closure holds;
- actual current A/B sources are revalidated before dependent continuation;
- no rollback/force rewrite of A occurs to recreate an imagined global transaction.

Exact live/campaign transfer ordering remains Step 5.8.

## LAW 5.6-28 — SAME-REF CHECKPOINT MATERIAL MAY SHARE THE CAMPAIGN TRANSACTION ONLY WHEN INDEPENDENT POLICY REQUIRES IT

Campaign publication itself does not create a checkpoint.

If Step-5.7 policy later determines that a checkpoint descriptor/pointer is required by the same durability edge and those paths belong to the same campaign ref, they SHOULD join the same one-tree campaign transaction.

Otherwise checkpoint creation may be omitted or lag according to its own owner.

## LAW 5.6-29 — LAGGING PROJECTIONS DO NOT AUTOMATICALLY JOIN CAMPAIGN TRANSACTION

Story/transcript/render projections are not synchronized merely because campaign canon is published.

Only projection/evidence material independently required by current recovery closure joins the transaction. Steps 5.10–5.12 own normal projection durability/retention/delivery.

## LAW 5.6-30 — REPOSITORY CONFIGURATION FAILURE HAS NO UNSAFE FALLBACK

If repository rules/permissions/branch configuration reject the required non-force publication path, return a typed infrastructure/authorization failure.

Do not bypass by:

- force push;
- hidden alternate authoritative ref;
- per-file Contents writes;
- LLM-owned fallback publication.

## LAW 5.6-31 — LOCAL PER-REF SERIALIZATION MAY OPTIMIZE BUT DOES NOT REPLACE REMOTE CONCURRENCY SAFETY

A Python implementation MAY serialize simultaneous publication attempts to the same repository/ref inside one process to avoid self-induced races.

Remote non-force validation and dependency-aware revalidation remain required because other processes/users can mutate the ref.

---

# 3. Conceptual Python interface

No exact implementation names are canonical here, but the runtime needs equivalent separation:

```text
DurabilityRequest
    reason
    target durability scope/domain
    named blocking edge?
    required roots/closure evidence

PublicationPlan       # in-process typed value, not mandatory persisted record
    repository/ref/principal
    pinned head/tree
    frozen owner generations
    exact path mutations
    dependency footprint

RepositoryPort
    read_ref_exact()
    read_commit_tree_exact()
    read_paths_at_commit()
    compare_or_is_ancestor()
    create_tree_from_base()
    create_single_parent_commit()
    update_ref_non_force()

PublicationOutcome
    no_write_needed
    confirmed_published
    conflict_revalidation_required
    failed_prepublication
    ambiguous
```

Exact packaging/module/class decomposition is deferred to implementation planning after architecture closes.

---

# 4. Normal campaign publication protocol

Given pinned authoritative HEAD `H`:

```text
1. validate repository role, target ref and acting principal
2. freeze Step-5.5 selected roots + exact owner generations
3. derive required campaign-domain durable closure evidence
4. derive exact pending write set
5. normalize/drop byte-identical or no-longer-required mutations
6. if write set empty:
       return NO_WRITE_NEEDED
7. resolve base tree T(H)
8. create one resulting tree T2 = T(H) + complete delta
9. if T2 == T(H):
       return NO_WRITE_NEEDED
10. preflight read ref
11. if ref != H:
       classify/revalidate/rebuild from new authority
12. create C(tree=T2, single parent=H)
13. immediately request non-force ref update -> C
14. if confirmed accepted:
       adopt publication generation-specifically
15. if confirmed rejected:
       repin/classify/revalidate
16. if indeterminate:
       enter targeted ambiguity protocol
```

The exact number of backend calls is implementation/performance detail, but ordinary successful publication should avoid redundant confirmation reads.

---

# 5. Failure/ambiguity matrix

| Failure point | Current authority | Candidate disposition |
|---|---|---|
| local validation fails | current ref HEAD | no remote mutation; retain dirty; typed failure |
| tree object created then crash | current ref HEAD | tree non-authoritative; restart from actual ref |
| preflight sees ref moved | new ref HEAD | no commit from stale base; targeted revalidation |
| commit created then process stops before ref update | current ref HEAD | prepared commit non-authoritative |
| final update confirmed rejected | current ref HEAD | conflict/infrastructure classification; C non-authoritative |
| final update confirmed accepted | new C selected | adopt exact generations; no normal reread |
| update dispatched, response indeterminate | unknown | no ack/clearing; read current ref + ancestry |
| ambiguity verifies D==C | C current | confirmed publication |
| ambiguity verifies C ancestor of D | D current | historical publication proven; targeted D-vs-C compatibility/adoption |
| ambiguity verifies C not reachable from D | D current | C cannot satisfy current source proof; revalidate/rebuild |
| success then process crash before local clearing | repository source is authority | cold recovery from actual ref; no semantic replay |
| campaign succeeds, another native domain fails | successful campaign source remains real | whole promise incomplete; compose/revalidate actual sources |

---

# 6. Explicit save consequences

Explicit save retains Step-5.5 semantics.

For one campaign ref, all campaign-owned dirty roots selected by save + required campaign-domain recovery closure are published in one campaign transaction.

Successful save acknowledgement requires:

- every required native domain of the save promise has a compatible durable source composition;
- any campaign-domain write is confirmed/verified as published or was already durable with no write needed;
- no required root remains only in volatile state.

A failed/ambiguous save does not falsely claim success and does not hard-lock otherwise coherent local/private play under Step 5.5.

---

# 7. Security and authorization consequences

Python repository ownership is not repository-account ownership.

The persistence subsystem must bind every mutation to an authenticated acting principal and applicable HDM authorization rule before transport.

A remote Python service/bridge using a shared technical credential MUST NOT infer that the service account's GitHub write permission grants gameplay authority.

Deployment must preserve enough trusted identity/delegation evidence for:

- creator-only singleplayer writes;
- active PLAYER-bound multiplayer writes;
- storage-owner-only metadata writes;
- creator-only mode/access/engine-policy operations.

Legacy runtime logic that relies on GitHub commit `author.login` as creator/audit evidence must be revisited during machine realization if the selected bridge cannot preserve per-user authenticated authorship reliably. Do not solve that by forging untrusted author metadata.

---

# 8. Deployment prerequisite

Current OpenAI ChatGPT Data Analysis Python cannot make external API/web requests. Therefore local built-in Python alone cannot directly implement the required authenticated GitHub `RepositoryPort` merely because the ChatGPT surface has a connected GitHub app.

This candidate records a required host capability:

> Every deployment profile claiming campaign persistence SHALL provide deterministic Python core a supported authenticated repository bridge/capability satisfying Step 5.6.

Concrete bridge topology is deferred to host/deployment feasibility work, including Step 6 where platform call topology/capability profiles are finalized.

This prerequisite is not permission to weaken Python ownership or transaction safety.

---

# 9. Deferred machine realization

After the architecture program closes, implementation planning must cover at least:

- Python persistence subsystem/runtime package location;
- authenticated RepositoryPort implementation/host bridge;
- exact typed request/outcome structures;
- bounded dependency/read footprint representation;
- dirty-generation/fingerprint tracking;
- GitHub error-to-epistemic-outcome mapping;
- ambiguity ancestry/current-compatibility verification;
- targeted compare/read strategy;
- per-ref local serialization;
- update of stale `PERSISTENCE.md`, `STORAGE.md`, `SAVE_CONTRACT.md`, multiplayer/live contracts as later slices finalize;
- replacement/extension of persistence regression tests for ambiguity, post-success crash, Python ownership and generation-specific clearing.

No implementation begins in Step 5.6 architecture.

---

# 10. Candidate exit assessment

The candidate satisfies the Step-5.6 agenda if adversarial review confirms:

- one campaign ref never exposes a partial product save;
- every Git transport/crash window has one authoritative-state interpretation;
- normal success avoids redundant reads;
- ambiguity is resolved without gameplay replay or false acknowledgement;
- concurrency uses dependency-aware revalidation rather than blind merges;
- partial multi-domain publication never invents rollback;
- Python core, not LLM, owns repository transport;
- the host bridge prerequisite is explicit rather than silently assumed.

Next gate: adversarial review.