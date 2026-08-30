# Step 5.6 — Campaign Publication & Crash Consistency — Resolution Gate

Status: **RESOLUTION GATE — READY FOR CANONICALIZATION**

Date: 2026-08-20

Reviewed chain:

- task brief
- research draft
- analytical challenge
- candidate specification
- adversarial review

Architecture direction:

> **PYTHON-OWNED SINGLE-REF CAS PUBLICATION**

---

# 1. Owner decision status

No new owner-level decision is required.

The governing owner decision remains:

> Runtime repository/GitHub work belongs to deterministic Python core; LLM roles do not own repository transport.

Adversarial findings do not reopen product semantics, authority ownership or accepted risk. They mechanically strengthen the physical protocol required to realize that decision and Step-5.5 durability semantics.

---

# 2. Required refinements accepted for canonicalization

The canonical specification SHALL incorporate all of the following.

## R1 — authority-atomic terminology

Do not call the multi-request Git object construction one network-atomic transaction.

Within one campaign ref, atomicity means:

```text
old ref-selected coherent revision
    -> one non-force ref selection
    -> new complete coherent revision
```

Prepared objects may exist without authority.

## R2 — single-parent publication commit

Ordinary campaign publication commit has exactly one parent equal to frozen/pinned HEAD H.

Together with non-force ref update, this is the final stale-write guard.

## R3 — preflight ref probe is optimization only

Use it to avoid known-stale commit creation and reduce orphan objects. Do not rely on it for final correctness.

## R4 — current closure, not ancestry alone, governs acknowledgement

After ambiguous update:

- C == current HEAD gives exact selection evidence;
- C in current lineage gives durable lineage evidence;
- if current HEAD D != C, targeted D-vs-C dependency/source revalidation determines whether current required closure is compatible;
- only compatible current closure may release the durability promise/edge.

Never restore C merely because it simplifies acknowledgement.

## R5 — bounded lineage verification

Ambiguity resolution uses repository/server-supported bounded exact comparison/ancestry evidence. No ordinary clone/pull/unbounded history walk.

If evidence cannot be obtained, remain ambiguous/recovery-required.

## R6 — normalized empty-delta guard

After exact mutation normalization, if no actual path change remains or resulting tree equals base tree, return `NO_WRITE_NEEDED` and create no commit.

Explicit delete of an already-absent path also normalizes away.

## R7 — resulting-tree completeness before first remote mutation

Before creating any remote tree/blob object, deterministically validate every required companion owner/index/routing/reference/recovery path for the planned resulting tree.

Late discovery invalidates/rebuilds the plan; it does not create a second product commit.

## R8 — generation-specific dirty clearing

Publication freezes exact semantic owner/path generation or equivalent fingerprint. Success clears only the frozen generation represented by the published tree; later local generations remain dirty.

## R9 — bounded semantic dependency footprint

Conflict classification includes accepted reads/dependencies, authorization/ownership/routing dependencies and recovery/reference dependencies, not only physical write paths.

## R10 — native-owner-only reconciliation

Automatic overlap reconciliation is allowed only where the native owner defines deterministic safe reconciliation. No generic YAML/JSON/text merge becomes semantic authority.

## R11 — transport outcome epistemics

Repository port distinguishes confirmed accepted, confirmed rejected and indeterminate authority-changing operations.

Only indeterminate results enter ambiguity verification.

## R12 — bounded automatic retry

Automatic stale/conflict retry is bounded. Repeated contention returns a typed synchronization/conflict result; it does not loop indefinitely.

Exact retry count/backoff remains implementation/configuration policy.

## R13 — authorization dependency revalidation

If HEAD movement changes relevant player binding, mode, creator/access policy or other authorization dependency, revalidate application authorization before retrying publication.

Repository credential success alone is not gameplay authority.

## R14 — authenticated acting-principal bridge

Python repository bridge must preserve trustworthy acting-principal/delegation evidence. A shared technical credential cannot silently become campaign/player authority.

If chosen bridge cannot preserve meaningful per-user Git commit authorship, legacy access rules that rely solely on `author.login` require explicit trusted machine-realization replacement rather than forged author metadata.

## R15 — host RepositoryPort prerequisite

Every deployment profile claiming campaign persistence must provide Python core an authenticated repository capability satisfying the canonical port contract.

Current built-in ChatGPT Data Analysis Python cannot itself make external API/web requests and therefore does not satisfy this capability alone.

No LLM Git fallback is permitted.

## R16 — narrow post-preflight phase

After final preflight, do no LLM work, broad research, semantic derivation or unrelated network operations before commit/ref attempt. Only already-frozen deterministic object finalization and immediate ref transition belong in that narrow race window.

## R17 — multi-domain compatibility after partial success

Successful native-domain publication remains real. If another required domain fails, revalidate the actual composed source set; overall edge remains incomplete until compatible closure holds. No rollback/distributed transaction.

## R18 — no generic persistent publication journal

No journal is introduced solely for post-success local crash recovery. Repository/native authorities + existing execution/recovery identities remain authoritative. Revisit only if Step 5.7 or implementation evidence demonstrates a real need.

---

# 3. Explicit deferred blockers/debt

These do not block Step-5.6 semantic canonicalization but MUST survive into later work.

## D1 — Python-to-repository host bridge feasibility

A supported authenticated bridge is mandatory before any runtime profile can claim actual campaign persistence. Plain built-in ChatGPT Data Analysis Python alone is insufficient under current platform constraints.

Carry to Step 6 deployment/host feasibility and integrated implementation planning.

## D2 — acting-principal / Git authorship realization

Selected bridge must preserve or replace current authenticated Git authorship assumptions without trusting forged metadata.

Carry into access-control/runtime realization.

## D3 — runtime prose is ahead/behind architecture in different places

Current `PERSISTENCE.md`, `STORAGE.md`, `SAVE_CONTRACT.md`, multiplayer/live files contain useful existing invariants but remain imperative prose oriented around current host/tool execution and contain stale policy assumptions elsewhere.

Do not partially rewrite them before 5.7/5.8 closes adjacent recovery/live semantics.

## D4 — executable test expansion

Future Python subsystem tests must cover lost ACK, ancestry/current-closure split, post-success crash, generation-specific clearing, authorization race, bounded contention, bridge unavailability and Python-only repository ownership.

---

# 4. No scope leakage

Canonical 5.6 SHALL NOT decide:

- checkpoint source-selection/hydration semantics — 5.7;
- live/campaign publish order, fencing and compaction authority transfer — 5.8;
- fictional chronology ordering — 5.9;
- Story/transcript publication cadence — 5.10/5.11;
- host delivery acknowledgement — 5.12;
- orphan-object/ref cleanup — 5.13;
- exact Python module/class implementation — later implementation planning.

---

# 5. Gate result

**READY FOR CANONICALIZATION.**

No unresolved Step-5.6 architecture blocker remains inside its declared scope.

Canonicalization must preserve the host/deployment prerequisite as an explicit unresolved implementation feasibility obligation rather than falsely claiming that plain ChatGPT sandbox Python already has authenticated GitHub networking.