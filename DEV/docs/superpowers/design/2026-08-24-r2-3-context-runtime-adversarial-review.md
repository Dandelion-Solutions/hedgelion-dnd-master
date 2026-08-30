# R2.3 — Context Runtime Adversarial Review

Status: **ADVERSARIAL REVIEW COMPLETE — CORRECTIVE AMENDMENTS REQUIRED / NO NEW OWNER TRADE-OFF**

Date: 2026-08-24

Reviewed candidate:

- `2026-08-24-r2-3-context-runtime-candidate-spec.md`

Owner direction remains:

> **Bounded Multi-Channel Discovery + Packet-First Allocation**

The review attacks false-negative discovery, packet completeness, secrecy, routed HOT/live currentness, monolithic indexes, physical sharding and accidental SQLite authority.

## AR-1 — Packet closure cannot be assumed fully known before all required owners are inspected

### Attack

A static `ContextNeedProfile` may say “load Actor + relevant knowledge”, but loading the Actor/current task evidence may reveal a registered dependency that is itself mandatory for a correct decision: a specific active effect, contract, owner, exact source, procedure state or another typed dependency.

If packet membership is frozen before such a dependency can be discovered, the assembler can return a formally complete but semantically incomplete packet.

### Resolution

Required-packet construction SHALL support **bounded staged closure**.

The need profile defines the allowed requirement classes and dependency relations. During targeted loading/verification, a loaded required owner may expose a registered dependency that extends the required packet. That extension is deterministic, typed, cycle-safe and bounded by the same profile/work limits.

The LLM does not invent the dependency relation.

If bounded required closure cannot be completed, assembly returns `UNSATISFIABLE` rather than silently dropping the dependency.

### Amendment

Add canonical law:

> **REQUIRED PACKET IS A BOUNDED TYPED CLOSURE, NOT NECESSARILY A STATIC FLAT LIST.**

## AR-2 — Discovery frontier must not claim global completeness

### Attack

Multi-channel discovery can still miss something semantically relevant if every cheap hint is stale/incomplete. Calling the resulting candidate frontier “complete” would create a new false closed-world guarantee.

Open-ended questions such as “who nearby could notice this?” are especially dangerous because they may not name the missing entity explicitly.

### Resolution

The assembler SHALL distinguish:

- **task-complete required closure** — complete relative to a registered need profile and the authoritative/current sources that profile requires;
- **candidate discovery frontier** — bounded best available candidate set from admitted channels, not a universal proof that nothing else exists.

A registered consumer that requires exhaustive scope must name an authoritative exhaustive source/contract for that scope. Derived indexes/Story/scene hints cannot manufacture exhaustiveness.

If a task cannot establish the required exhaustive scope from an owner contract, it must degrade/reframe/fail safely rather than infer universal absence.

### Amendment

Add canonical law:

> **BOUNDED DISCOVERY IS NOT GLOBAL CLOSED-WORLD PROOF. EXHAUSTIVENESS MUST COME FROM AN OWNER CONTRACT.**

## AR-3 — Eligibility checking may itself require targeted policy/owner reads

### Attack

The candidate wording says eligibility precedes semantic content use, but some eligibility decisions depend on knowledge/disclosure/current-observation owners that cannot be decided from a bare ID/path descriptor.

A naive implementation might either read the whole secret entity before checking eligibility or refuse to load enough metadata to determine eligibility.

### Resolution

Discovery and eligibility use a two-boundary model:

1. deterministic assembly may perform the **minimum targeted internal read** required to resolve routing/currentness/eligibility;
2. semantic material is admitted to the receiving logical role only after eligibility succeeds.

Internal eligibility reads are not equivalent to role evidence and are not automatically added to the prompt/bundle.

Trace access remains restricted.

### Amendment

Clarify R2.3-L6 accordingly; no new subsystem required.

## AR-4 — HOT current owner versus disposable SQLite must remain explicit

### Attack

“SQLite is disposable” can be misread as “Git YAML always outranks SQLite”. That would contradict Step-5 SOFT semantics: established HOT state may be newer current truth than the last durable Git frontier.

Conversely, treating every SQLite cache/index row as current authority would create duplicate owners.

### Resolution

Authority is semantic-owner-relative, not storage-format-relative.

During a live local runtime, an owning world/runtime record may be physically represented in HOT/SQLite and be the current established owner state even when not yet durable. Losing that environment may lawfully lose unpublished SOFT state and recovery then returns to durable native sources.

A disposable **cache/index/projection** in SQLite never gains authority merely from freshness or query convenience.

### Amendment

Add canonical wording:

> **SQLITE MAY PHYSICALLY HOST CURRENT ESTABLISHED OWNER STATE; SQLITE FORMAT ITSELF IS NEVER THE SOURCE OF THAT AUTHORITY.**

## AR-5 — Monolithic index debt is acceptable only if it does not become a correctness dependency on directory enumeration

### Attack

Keeping one `ITEM_INDEX.yaml`/`NPC_INDEX.yaml` is deliberately simple, but an implementation might still list the entire sharded entity directory to rebuild/validate it during ordinary turns, defeating lazy loading and reintroducing GitHub directory-scale pressure.

### Resolution

Current monolithic indexes remain permitted and intentionally unpartitioned.

Ordinary Context Runtime lookup SHALL use the monolithic index artifact directly when needed; it SHALL NOT require ordinary-turn enumeration of every physical record directory merely to answer an indexed lookup.

Index rebuild/audit is maintenance/recovery work, not the hot-path lookup contract.

Repartitioning remains dormant until the approved measured-scale trigger fires.

No additional index hierarchy is introduced now.

## AR-6 — Record sharding must not leak into semantic identity or reference contracts

### Attack

If callers begin storing/deriving semantics from paths such as `WORLD/NPC/012/...`, future shard-policy migration becomes semantically dangerous and refs become path-coupled.

### Resolution

Stable record identity remains the reference contract. Physical path is routing metadata.

Shard directory, bucket number and file path SHALL NOT be used to infer kind, fictional location, chronology, ownership, relevance or authority beyond the storage-routing contract that resolved the path.

A future shard migration may change paths without changing IDs or semantic refs, subject to ordinary migration/index consistency rules.

## AR-7 — Optional ranking/fairness must not accidentally become cross-turn mutable state

### Attack

S02/S40 could lead to a persistent starvation/recurrence database whose maintenance costs and authority semantics exceed the demonstrated need.

### Resolution

Baseline ranking uses currently available deterministic metadata and request-local/group-coverage rules. Persistent cross-turn starvation state remains unintroduced.

Reopen only if evaluation proves chronic exclusion that cannot be corrected without such state.

## AR-8 — Long-range retrieval fallback must remain bounded and dependency-specific

### Attack

“Broader targeted search” can become an escape hatch that silently means “scan all history until something looks relevant”.

### Resolution

Any escalation must name:

- the unresolved registered dependency/question;
- the eligible source family/domain;
- a finite work/result bound;
- the success/failure condition.

Failure to find sufficient evidence within the allowed bounded escalation produces the consumer's safe fallback or `UNSATISFIABLE`; it does not authorize unbounded search.

## Review conclusion

No finding invalidates owner-approved Alternative B, the monolithic-index decision or deterministic high-cardinality record sharding.

Required canonical amendments are:

1. required packet = bounded typed closure, not necessarily static flat list;
2. discovery frontier is not universal closed-world proof;
3. eligibility may use minimum internal targeted reads before role admission;
4. distinguish current owner state physically held in SQLite/HOT from non-authoritative SQLite caches/indexes;
5. monolithic index hot-path lookup must not require entity-directory enumeration;
6. shard paths remain routing-only and migration-safe;
7. no persistent fairness ledger without evidence;
8. historical fallback must be dependency-specific and bounded.

These are completeness corrections within the approved architecture, not new product trade-offs.
