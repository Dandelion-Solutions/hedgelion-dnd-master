# R2.7 WP-13 — Durability / SAVE / Publication — Step 3 Decision Brief

Status: **STEP 3 COMPLETE — DECISION SYNTHESIS / NO HUMAN-OWNED DECISION**

Date: 2026-09-02

Evidence basis:

- repaired WP-13 Step-1 package + `SR13-01`;
- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-step-2-evidence-extraction.md`;
- base Source Manifest + Step-2 expansion.

---

## 1. Decision statement

WP-13 requires a machine-realization architecture that satisfies already-accepted durability/publication semantics without introducing a new gameplay owner, global durability frontier, distributed transaction, persistent publication journal, transport fallback or broad completeness scan.

The evidence leaves no product-level choice about those constraints. The remaining decision is architectural composition among machine shapes that can or cannot satisfy them.

---

## 2. Stable axes

The realization must keep these axes independent:

1. **semantic establishment** — owned by native owner/execution/live contract;
2. **current durability obligation** — `MAY_DEFER` or named `MUST_BE_DURABLE_BEFORE(edge)`;
3. **durability-policy scope** — native/authority/visibility partition;
4. **owner generation / dirty membership** — local operational evidence from WP-12;
5. **required durable source closure** — correctness relation over native sources;
6. **pending write set** — only not-yet-durable material;
7. **native durability domain** — campaign ref, selected live source, storage-owner metadata, or another already-admitted domain;
8. **publication source/currentness basis** — exact domain-native revisions;
9. **transport outcome** — accepted/rejected/indeterminate/no-write/prepublication failure;
10. **overall promise status** — explicit SAVE/HARD-edge result over all required domains.

No scalar may collapse these axes into one campaign-global frontier.

---

## 3. Options considered

### Option A — Scope-evaluated native-domain composition with immutable ephemeral attempts

Shape:

```text
named owner edge / explicit SAVE / risk-control request
    -> evaluate exact policy scope + frozen owner generations
    -> derive required durable source closure
    -> classify already-durable versus pending native-domain work
    -> execute each required native durability domain under its existing protocol
    -> aggregate domain outcomes for the promised boundary
```

Campaign-domain publication uses one immutable ephemeral frozen attempt and the fixed R2.6 Python/core -> GitHub Connector -> non-force-ref path.

Pros:

- directly preserves Step-5.5 scope policy and RRC;
- naturally composes live/campaign/storage domains without distributed transaction;
- maps WP-12 G/G+1 semantics cleanly;
- preserves existing named edge owners;
- supports clean/no-write completion;
- confines ambiguity/currentness to native domain protocol;
- does not require a persistent journal or generic semantic owner.

Cons:

- requires explicit typed operation/result values and careful currentness/closure accounting;
- implementation must distinguish overall SAVE result from each native-domain result;
- stale current machine prose/tests need coordinated repair.

### Option B — Persistent centralized durability scheduler / save journal

Shape:

```text
all dirty state -> central persistent durability queue/frontier/journal -> worker publishes
```

Pros:

- operationally simple to visualize;
- one place for retry status.

Cons / rejection:

- creates a new global owner/queue/frontier forbidden by Step 5.2/5.3/5.5/5.6/WP-12;
- risks duplicating native currentness/authority;
- encourages campaign-global timing and cross-domain ordering;
- persistent journal is explicitly rejected absent concrete unresolved recovery evidence.

**Disposition: REJECTED by accepted architecture.**

### Option C — Campaign-only `SAVE_ALL_DIRTY` transaction as the universal SAVE realization

Shape:

```text
explicit SAVE -> gather all dirty campaign paths -> one campaign commit -> saved
```

Pros:

- close to current `SAVE_CONTRACT.md` and tests;
- simple singleplayer path.

Cons / rejection:

- cannot satisfy Step-5.5 multi-native-domain SAVE;
- can falsely treat campaign commit as live/shared authority;
- cannot represent partial native-domain success;
- conflates campaign transaction atomicity with overall SAVE promise;
- encourages broad “all state” scans/materialization.

**Disposition: REJECTED as universal architecture; retained only as the campaign-domain subcase of Option A.**

### Option D — Independent bespoke durability flows with no shared operation contract

Shape:

```text
onboarding save path
readiness save path
handoff save path
multiplayer save path
explicit save path
maintenance save path
...
```

Pros:

- each owner can be locally optimized.

Cons / rejection:

- repeats currentness/ambiguity/G-specific adoption logic;
- makes it difficult to prove one consistent SAVE promise;
- increases risk that one edge silently uses weaker publication semantics;
- does not exploit already-shared Step-5.5/5.6 protocol while still needing native owner-specific root/edge semantics.

**Disposition: REJECTED as primary architecture. Owner-specific edge/root policy remains, but it feeds a shared machine protocol under Option A.**

---

## 4. Recommendation

**Select Option A: scope-evaluated native-domain composition with immutable ephemeral attempts.**

This is not a new product choice. It is the narrowest machine shape that realizes the already-approved architecture.

---

## 5. Recommended conceptual machine split

Exact Python class names remain implementation detail. Equivalent typed values/operations must preserve the following separations.

### 5.1 `DurabilityEvaluation` — ephemeral

Conceptually carries:

```text
reason / named edge
selected durability-policy scope(s)
frozen implicated owner generations / dirty roots
policy-owned accumulated dirty roots
required recovery/reference/interpretation dependencies
required native durable source closure
already-durable components
pending native-domain work
quiescence/freeze scope when required
```

It is evaluation/operation state only; not a persistent owner or queue.

### 5.2 Scope-relative exposure support — local operational metadata

For deferrable risk-control policy, implementation must be able to determine the oldest still-relevant unpublished established state within the applicable policy partition.

WP-13 does **not** require one timestamp per historical delta. A correct aggregate representation is allowed when it tracks the actual oldest still-relevant unpublished basis and resets/recomputes only when that relevant state becomes durable/superseded.

No campaign-global `durable_frontier_time` exists.

### 5.3 `FrozenCampaignPublicationAttempt` — immutable ephemeral

Conceptually carries at least:

```text
repository identity
target campaign ref
acting principal + authorization basis
pinned authoritative HEAD + base tree
frozen owner generations/fingerprints
campaign-domain durability roots
required dependency/read/currentness footprint
exact WP-11 UPSERT/DELETE path delta
required index/projection companions
publication reason / named edge
prepared tree/commit identities as produced
```

The attempt freezes before the first remote Git-object mutation.

No SQLite transaction spans it and it is not persisted as a generic publication journal.

### 5.4 `NativePublicationOutcome` — typed operation result

At minimum distinguishes:

```text
NO_WRITE_NEEDED
CONFIRMED_ACCEPTED
CONFIRMED_REJECTED
INDETERMINATE
FAILED_PREPUBLICATION
REVALIDATION_REQUIRED
CAPABILITY_FAILURE
```

Exact subcodes are implementation detail, but no result may erase the epistemic distinction between confirmed rejection and unknown/indeterminate remote outcome.

`CAPABILITY_FAILURE` on the fixed R2.6 Connector path does not authorize an alternate transport.

### 5.5 `DurabilityPromiseResult` / SAVE composition — ephemeral

Conceptually maps every required native durability domain to its current confirmed status and computes whether the promised boundary is satisfied.

It is not a distributed transaction coordinator and does not roll back already accepted native publications.

---

## 6. Campaign-domain publication protocol

The accepted ordinary existing-campaign envelope is:

```text
1. select/freeze campaign-domain roots and exact owner generations
2. freeze application authorization/currentness/dependency basis
3. derive exact WP-11 direct paths + required index/projection companions
4. prove bounded resulting-tree completeness/invariants locally
5. normalize byte-identical UPSERT / absent DELETE
6. if empty -> NO_WRITE_NEEDED
7. obtain exact base tree for pinned H
8. deterministic Python/core asks GitHub Connector to create base-derived tree
9. preflight target ref
10. if ref moved -> classify bounded semantic footprint
11. if still H -> create one single-parent commit C(parent=H)
12. immediately request authoritative `update_ref(force=false)`
13. classify ACCEPTED / REJECTED / INDETERMINATE
14. adopt only confirmed compatible exact generations
```

Only deterministic already-frozen finalization occurs in the post-preflight race window.

No runtime alternate transport participates.

---

## 7. Currentness and retry decision

### 7.1 Proven disjoint movement

If bounded compare shows movement disjoint from:

- planned write paths;
- native dirty/root owners;
- accepted read/dependency footprint;
- authorization/routing dependencies;
- required recovery/reference dependencies;

then the accepted semantic result remains valid.

The runtime adopts the newer campaign authority, rebuilds only source/path/transport basis, preserves accepted IDs/execution/RNG and makes a new single-parent publication attempt.

### 7.2 Relevant overlap

If overlap is relevant:

- use a native-owner deterministic safe merge/reconciliation only when that owner defines one;
- otherwise return typed owner-specific revalidation/re-resolution;
- never use generic YAML/JSON/text merge as semantic authority;
- never reroll/reallocate solely because Git moved.

### 7.3 Bounded retry

Automatic transport/currentness revalidation is bounded. Sustained contention returns a typed unresolved conflict/synchronization result.

---

## 8. Indeterminate publication decision

After indeterminate final ref transition:

```text
NO saved acknowledgement
NO G dirty clear
NO HARD-edge release
NO gameplay replay
NO blind second update_ref
```

Perform bounded exact authoritative verification:

1. read current target ref `D`;
2. if `D == C`, prove selected closure and accept;
3. if bounded Connector compare/ancestry proves `C` is in `D` lineage, treat C only as durable lineage evidence, inspect D-vs-C intersection with required closure/dependency footprint, and accept only if current D still satisfies the promise;
4. if bounded evidence proves C absent, repin/revalidate from current D;
5. if bounded proof is unavailable, remain `INDETERMINATE` / recovery-required.

Never force stale C back into authority.

---

## 9. Generation-specific adoption decision

On confirmed compatible campaign publication:

```text
for each frozen owner generation G:
    mark G durable under confirmed source basis
    if current local generation == G:
        clear its dirty membership
    else:
        preserve newer G+1 dirty
```

Derived indexes/helpers may update/rebuild according to their owner contracts but never become authority.

A crash after remote success but before local adoption is recovered from actual authoritative remote/native state; no gameplay replay or persistent generic journal is required.

---

## 10. Explicit SAVE composition decision

```text
accept explicit SAVE intent
-> freeze selected save scope strongly enough to give acknowledgement one meaning
-> derive RRC-compatible required native durable source closure
-> partition pending work by native durability domain
-> skip already-durable components
-> execute required domains under their own protocols
-> preserve every confirmed accepted native publication
-> revalidate coherent resulting source composition
-> acknowledge saved only when the entire promised closure is confirmed durable
```

If one domain accepts and another rejects/fails/indeterminate:

- accepted domain remains accepted;
- overall SAVE remains incomplete;
- no distributed rollback or force rewrite occurs;
- dependent continuation is gated only where an unresolved correctness-critical edge requires it;
- ordinary local/private continuation after a failed explicit save remains governed by Step 5.5.

---

## 11. Named HARD edge decision

The shared machine never decides **why** an edge is HARD.

The owning module supplies:

```text
edge identity/reason
policy scope
policy roots / accumulation scope
success postcondition
```

WP-13 machinery evaluates/satisfies the durability closure.

Current named consumers include at least:

- `PROVISIONAL_IDENTITY`;
- READY_PC / PLAY_READY;
- controlled recovery-safe handoff;
- membership deactivation/reactivation and policy grant/revoke where owner marks HARD;
- explicit SAVE / pause-stop composition;
- current live shared write-before-reveal/CAS edges;
- maintenance/adoption boundaries that require clean durable state before runtime switch.

No central persistent trigger table is required.

---

## 12. Fixed transport and capability failure

R2.6 fixes the supported gameplay transport:

```text
Python/core -> GitHub Connector -> non-force authoritative ref transition
```

WP-13 preserves that choice.

A missing required Connector operation/capability returns a typed supported-profile capability/infrastructure failure. Runtime does not probe/fallback through CLI/native Git/private HTTP/tokens/custom MCP/backend/Actions/transparent push.

No new transport research is needed. A future bounded feasibility spike is permitted only if implementation evidence demonstrates a concrete uncertainty **inside** this selected path that current accepted evidence cannot resolve.

---

## 13. Boundaries intentionally not selected here

- exact SQL DDL/table/API representation;
- exact policy names or risk-control numeric thresholds;
- exact automatic retry count/backoff;
- exact user-facing wording for every failure code;
- final checkpoint machine/schema (WP-14);
- final live file/ref/identity machine (WP-16);
- bootstrap/migration orchestration (WP-19/WP-20);
- test implementation (WP-22 / implementation TDD);
- performance partitioning (WP-24);
- stale Storage-v2 prose repair (WP-26).

---

## 14. Required downstream verification obligations

Later implementation/testing must prove at least:

1. no global one-hour/frontier architecture remains;
2. scope-relative exposure basis follows actual still-relevant unpublished state;
3. named HARD semantics stay with owner modules;
4. explicit SAVE composes native domains and never falsely acknowledges partial/ambiguous durability;
5. campaign normalized empty delta creates no write;
6. exact WP-11 record + required-index closure is one campaign publication;
7. frozen attempt includes auth/currentness/dependency/read basis;
8. preflight movement uses bounded semantic footprint;
9. disjoint movement preserves accepted IDs/RNG/semantics;
10. overlap cannot use generic text merge as authority;
11. final ref transition is non-force;
12. confirmed reject differs from indeterminate;
13. indeterminate result uses bounded ref/lineage/current-closure verification and never blind retry;
14. confirmed G publication cannot clear G+1;
15. crash after remote success/local adoption loss recovers from remote authority without replay;
16. checkpoint is not required/save proof;
17. live exact-source CAS remains authoritative for live-claimed mutation;
18. fixed Connector capability failure does not trigger alternate transport;
19. storage-owner metadata transaction remains independent from campaign SAVE;
20. engine/rules maintenance publication consumes the same campaign publication contract without granting unauthorized MANIFEST writes.

---

## 15. Decision disposition

```text
RECOMMENDED_OPTION:         A — scope-evaluated native-domain composition
HUMAN_DECISION_REQUIRED:    NO
UPSTREAM_REOPEN_REQUIRED:   NO
MATERIAL_RISK_ACCEPTANCE:   NONE NEW
STEP_4_MAY_PROCEED:         YES
```

The recommendation is mechanically derived from accepted architecture and therefore proceeds through normal auto-continue review.