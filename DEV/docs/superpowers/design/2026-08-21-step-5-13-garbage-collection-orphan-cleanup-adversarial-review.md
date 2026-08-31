# Step 5.13 — Garbage Collection / Orphan Cleanup — Adversarial Review

Status: **ADVERSARIAL REVIEW — BLOCKERS FOUND; ALL HAVE MECHANICAL RESOLUTIONS**

Date: 2026-08-21

Reviewed candidate:

- `2026-08-21-step-5-13-garbage-collection-orphan-cleanup-candidate-spec.md`

Candidate direction:

> **OWNER-GATED RETIREMENT / CLOSED BLOCKER CONTRACTS / COMPLETENESS-TYPED PROTECTION ROUTING / CURRENT-BASIS SAFE-RETIREMENT PROOF / REPLACEMENT-BEFORE-REMOVAL / OPTIONAL POST-AUTHORITY REF CLEANUP / HOST-MANAGED GIT OBJECT RECLAMATION**

The high-level architecture survives. Review found **12 required blockers/refinements**. None requires a new human product/risk decision.

---

# 1. Review method

The candidate was attacked across:

```text
cleanup-contract evolution
runtime/catalog adoption
negative-proof completeness
protection-index self-retirement
cross-source dependency creation
interaction/message provenance
idempotency lifetime
Story cursor migration
verified exact archive
checkpoint concurrency
live ref deletion acknowledgement
orphan branch classification
Git history/privacy semantics
legacy migration
large-scale cleanup boundedness
```

Classification:

- **BLOCKER** — candidate cannot canonicalize without normative resolution;
- **REQUIRED REFINEMENT** — direction valid but contract incomplete;
- **DEFERRED MACHINE** — semantics resolved; implementation remains later.

---

# 2. F1 — cleanup-contract evolution can race engine/catalog adoption

**Severity: BLOCKER**

## Attack

Engine generation G1 defines target T blockers:

```text
blockers = {A,B}
```

A newer engine G2 introduces owner C that may depend on T.

Campaign adopts G2, but old targets/protection routing still use G1 cleanup semantics. Cleanup then proves A/B absent and deletes T while a new C consumer is legal.

The problem is not runtime concurrency; it is **interpretation/version compatibility**.

## Analysis

Steps 5.2/5.7/Step 3 already require accepted runtime/catalog interpretation compatibility. Cleanup must be bound to the campaign's accepted cleanup-contract interpretation in the same way.

A consumer-admission change that expands blocker vocabulary cannot be treated as a harmless implementation-only code change.

## Required resolution R1

Add canonical law:

> **Cleanup-contract interpretation is part of campaign/runtime compatibility. A runtime/catalog adoption that changes blocker classes, reference-survival semantics or cleanup eligibility for existing target kinds must migrate/upgrade the affected cleanup contract/protection basis before automatic cleanup under the new semantics is enabled.**

Rules:

- one cleanup assessment pins the exact accepted cleanup-contract generation compatible with target and current campaign runtime;
- newer consumer C cannot durably rely on T until its protection semantics are admitted;
- legacy/incompatible target remains retain-only until migrated;
- open accepted execution continues under its own pinned interpretation and cannot be stranded by ambient newer cleanup rules.

**Disposition: mechanically resolved; no owner decision.**

---

# 3. F2 — `runtime.interaction -> raw message ref` may still require dereference after envelope deletion

**Severity: BLOCKER**

## Attack

Step 5.11 says Step-3 raw-message linkage is stable evidence linkage, and physical envelope removal belongs to 5.13.

Candidate permits deleting COMPACTED `runtime.message` after migrating remaining obligations.

But an old `runtime.interaction` may still contain:

```text
raw_message_ref = M17
```

If its schema implicitly means “load M17 to inspect the accepted request,” deleting M17 violates Step 3/5.11 even if the Interaction itself is settled.

## Analysis

This is exactly why reference-survival semantics must be explicit.

For an Interaction that still needs accepted semantic content for retry/audit/recovery, one of these must hold:

```text
message envelope remains resolvable
OR
Interaction/idempotency survivor independently retains required accepted meaning/fingerprint
OR
raw_message_ref is formally demoted to opaque provenance-only identity
```

A bare unchanged field with old implied dereference semantics is not enough.

## Required resolution R2

Before message-envelope removal, every surviving `runtime.interaction`/command/history reference must be classified and, if necessary, migrated.

Canonical rule:

> **Message-envelope deletion is forbidden while any accepted Interaction/execution contract still requires the message representation to reconstruct accepted meaning or validate idempotent retry. Opaque provenance-only linkage is legal only after sufficient semantic/idempotency evidence has moved to its owning survivor.**

Legacy raw-message refs default to resolvable until migration proves otherwise.

**Disposition: blocker resolved.**

---

# 4. F3 — protection routing can become immortal or self-authorize its own deletion

**Severity: BLOCKER**

## Attack

A correctness-complete reverse protection index P helps prove no consumers depend on targets.

Eventually P itself becomes obsolete after index generation P2 replaces it.

Two unsafe extremes:

1. P can never be deleted because deletion proof depends on P;
2. P says no one depends on P, so it deletes itself circularly.

## Analysis

Protection routing is a derivative generation with its own owner-local replacement contract.

Its deletion is authorized by the **routing/index owner generation transition**, not by running the target-retention query against itself.

Pattern:

```text
P1 serves blocker class C for generation G1
P2 becomes durable/current complete successor
routing generation selector/basis moves to P2
P1 no longer participates in any current SafeRetirementAssessment
then P1 may retire
```

## Required resolution R3

Add law:

> **Correctness-complete protection-routing generations retire only after a compatible successor/current routing basis is durably selected and every cleanup assessment that could rely on the old generation has ended/revalidated. They never authorize their own retirement from their own absence result.**

No durable reader lease is required; assessments are ephemeral and source/currentness movement causes retry.

**Disposition: blocker resolved without generic index lifecycle service.**

---

# 5. F4 — branch/ref deletion has its own ambiguous acknowledgement window

**Severity: BLOCKER / TRANSPORT**

## Attack

Eligible absorbed live ref E is non-authoritative.

RepositoryPort sends DeleteRef(E). Network response is lost.

Runtime does not know whether ref exists.

Blind retry may receive “not found,” or a concurrent valid process could theoretically create another ref at same textual name.

## Analysis

Ref deletion is post-authority cleanup, so ambiguity cannot threaten gameplay truth, but maintenance status must still be honest.

Stable epoch identity/name reuse is already undesirable.

## Required resolution R4

Ref-cleanup outcome uses the same epistemic discipline conceptually:

```text
CONFIRMED_ABSENT
CONFIRMED_PRESENT / deletion rejected
INDETERMINATE
```

After indeterminate outcome:

- exact-read the named ref when supported;
- absent => cleanup achieved;
- present and exact expected old source identity => may retry after current eligibility revalidation;
- present but points to a different/unexpected source => do not delete; classify integrity/maintenance conflict;
- never recreate the old ref merely to make deletion retryable.

Live epoch/ref identities used for authority generations are never reused.

No durable delete-job record is required.

**Disposition: blocker resolved.**

---

# 6. F5 — Git-history retention can violate user expectations about privacy even if semantic memory is correct

**Severity: REQUIRED REFINEMENT / DOCUMENTATION BOUNDARY**

## Attack

Candidate correctly says old Git history is not ordinary Master exact memory.

But a user may interpret “message deleted/compacted” as “the text is gone from storage.” In append-only Git that is false.

This is more than a technical detail when OOC/personal text exists.

## Analysis

Step 5.11 deliberately minimizes durable exact OOC retention, which is the primary defense: avoid publishing unnecessary sensitive exact text in the first place.

Once bytes are committed, ordinary cleanup cannot guarantee erasure.

Changing to history rewrite would be a material owner/security/storage decision and is outside 5.13.

## Required resolution R5

Canonical terminology/documentation must distinguish:

```text
no longer retained by active HDM semantic/history contracts
no longer present in current campaign tree
not guaranteed erased from Git repository history
```

Do not expose a player/admin command named “secure erase” unless a future explicit secure-expungement protocol actually provides that guarantee.

Machine realization should continue to minimize exact OOC persistence before publication.

**Disposition: clarification; no new product choice.**

---

# 7. F6 — Story source coverage may depend on dense enumeration continuity, not only one anchor

**Severity: BLOCKER**

## Attack

Candidate says preserve/migrate Story source enumeration anchor before message-envelope deletion.

Suppose source-domain cursor is a dense local ordinal and messages 1..100 are deleted individually while current retained state only knows cursor=100.

A future projection-contract migration may need to re-evaluate candidates in 40..70. The raw envelopes are gone and no enumeration structure maps those positions.

Does Step 5.10 promise such retroactive reprojection?

## Analysis

Step 5.10 contract generations solve this carefully:

- current compatible coverage means source candidates up to cursor have terminal disposition under that generation;
- changing semantic admission rules requires explicit migration/reprojection strategy;
- Step 5.10 does not promise arbitrary replay from deleted payload when prior retention law allowed deletion.

Therefore 5.13 must preserve **only the source/enumeration continuity promised by all still-supported projection-contract generations/migrations**, not hypothetical future reprojection capability.

But the cleanup contract must know which generations remain migration-supported before deleting enumeration records.

## Required resolution R6

Add law:

> **Source cleanup must preserve enough enumeration identity/anchors for every currently supported compatible Story coverage/migration path. It need not preserve deleted payload or arbitrary historical candidate replay for a future projection contract that was not protected before cleanup.**

A future contract expansion requiring old deleted content must accept unavailable history or require an explicit earlier retention/migration promise.

This mirrors Step 5.11 “never invent lost exact text.”

**Disposition: blocker resolved; no future-unbounded replay promise.**

---

# 8. F7 — compact idempotency anchors can grow forever

**Severity: REQUIRED REFINEMENT / PERFORMANCE RISK**

## Attack

Candidate avoids full command retention by keeping small duplicate-suppression anchors while retry remains possible.

In ordinary ChatGPT, stable host retry/revision identity feasibility is unresolved until Step 6. If no bounded retry horizon exists, anchors might accumulate forever—effectively another event log.

## Analysis

This is not a correctness defect; compact immutable accepted-interaction/result identity may be legitimate semantic history.

Step 3 already requires accepted interaction/command/history identities, and Step 5.11 product contract values semantic continuity.

Prematurely expiring anchors would be more dangerous than retaining them.

The unresolved issue is measured storage cost and exact minimum payload.

## Required resolution R7

Canonical 5.13 must:

- require minimum compact idempotency/result survivor only where retry contract actually needs it;
- not mandate a time-based expiration;
- permit long-lived small anchors;
- carry Step-6 feasibility/measurement debt to determine whether host identity allows a bounded retry horizon or further compaction.

Do not create a human decision until measured cost or platform behavior makes a real trade-off necessary.

**Disposition: non-blocking after explicit debt.**

---

# 9. F8 — verified-exact Transcript certification could accidentally become a new universal tombstone

**Severity: REQUIRED REFINEMENT**

## Attack

For every deleted message represented in Story, candidate may create a certification survivor containing source ID/digest.

If applied indiscriminately, this just replaces message envelopes with millions of tiny tombstones and undermines cleanup.

## Analysis

Certification survivor is needed only while a retained Transcript record claims `verified_exact` and its existing Story representation cannot itself carry the minimum certification data under the Story owner contract.

Best design:

- co-locate exact-certification basis with retained Transcript projection state where appropriate;
- no standalone per-message anchor if no verified-exact record survives;
- no certification anchor for ordinary `MAY_OMIT`/semantic-only history.

## Required resolution R8

Canonical wording should prefer **natural-owner/co-located survivor evidence** over a generic certification-tombstone class.

Standalone compact anchor is last resort for a concrete contract, not baseline representation.

**Disposition: YAGNI refinement.**

---

# 10. F9 — cleanup of selected checkpoint can race a bounded support read

**Severity: REQUIRED REFINEMENT**

## Attack

Support command resolves current `last_checkpoint_id=K`, then cleanup clears pointer/deletes K before support fetches path K from branch-relative current state.

Support command fails even though it started from a valid pointer.

## Analysis

The correct solution is not a durable reader lease.

Maintenance/support operation should pin the campaign revision that supplied the pointer and read K from that exact pinned revision. Git history remains reachable in the append-only baseline.

Cleanup may proceed independently after its own currentness checks.

## Required resolution R9

Any bounded operation that relies on a cleanup-eligible current record must either:

- exact-pin the source revision and read from that basis;
- or participate in an owner-specific protection relation if the operation promises current-record availability across revisions.

Ordinary read operations do not create durable GC roots merely because they are in flight.

**Disposition: refinement; reinforces pinned-read model.**

---

# 11. F10 — `UNCLASSIFIED_NONCURRENT_REF` can accumulate forever and branch namespace may collide

**Severity: REQUIRED REFINEMENT / OPERATIONAL**

## Attack

Connector cannot delete refs today. Failed openings may leave many branches. After context loss some become unclassified and therefore retained forever.

If epoch branch names are deterministic from scene/base only, a later opening could encounter an old leftover with the same name.

## Analysis

Step 5.8 already requires epoch-qualified stable identity and current route selection; branch existence alone never grants authority.

Implementation should generate epoch identity sufficiently collision-resistant/nonreused across distinct opening generations, not depend only on reusable scene/base naming if that creates ambiguity.

For old unclassified refs:

- maintenance may inspect bounded source metadata and current route/absorption records;
- unresolved leftovers are harmless except repository clutter;
- a future admin/tooling audit can classify/delete when capability exists.

## Required resolution R10

Carry machine debt:

- live branch naming/epoch identity must avoid authority-generation reuse;
- stale leftover name collision must never cause implicit adoption;
- unclassified refs may remain indefinitely without correctness effect;
- measured accumulation may justify a stronger bounded orphan registry **only if real evidence shows need**.

No preemptive orphan registry now.

**Disposition: no blocker after debt.**

---

# 12. F11 — cleanup of Story old generation may destroy correction provenance still referenced by current Story

**Severity: BLOCKER**

## Attack

Current Story record N2 supersedes N1. Old projection-contract/index generation G1 is considered obsolete and bulk-deleted.

But N2 contains an editorial/correction reference to N1 or a current availability/provenance explanation depends on G1 structure.

Bulk generation retirement produces dangling Story refs.

## Analysis

Generation supersession is only candidate discovery. Current Story reference closure remains authoritative for Story structure.

Bulk cleanup must exclude cross-generation survivors or migrate their refs before removing the generation.

## Required resolution R11

Add law:

> **Generation/epoch bulk retirement is legal only for the subset proven closed under all surviving cross-generation references and migration/provenance requirements. A generation label does not override current Story/reference closure.**

If sparse survivors remain, retain/migrate them individually; do not require whole-generation all-or-nothing deletion.

**Disposition: blocker resolved.**

---

# 13. F12 — whole current-tree record deletion can break future bounded integrity diagnosis even when ordinary operation is safe

**Severity: REQUIRED REFINEMENT**

## Attack

A compact message/receipt/checkpoint body is no longer needed for current gameplay and is deleted.

Later a corruption is discovered in a surviving SemanticEvent. The deleted record would have been useful repair evidence.

Should 5.13 retain everything “just in case” for future diagnosis?

## Analysis

No. That collapses into Alternative F and defeats explicit retention policy.

Step 5.7/INTEGRITY already treats checkpoints/history as optional bounded repair evidence, not guaranteed universal forensic archive. Step 5.9 likewise rejects arbitrary historical temporal analytics.

Git history may still incidentally contain deleted current-tree data, but ordinary correctness cannot depend on it.

The architecture must distinguish:

```text
required repair evidence promised by an owner contract
vs
potentially useful evidence
```

Only the former blocks deletion.

## Required resolution R12

Canonical law:

> **Potential future diagnostic usefulness alone is not a universal retention blocker. Only explicitly admitted audit/repair/provenance contracts protect evidence. Cleanup may reduce future forensic richness while preserving all current promises.**

Support tools must report unavailable evidence rather than fabricate it.

**Disposition: consistent with inherited product semantics.**

---

# 14. Additional attack matrix

## A1 — stale candidate + live forward dependency + missing protection index

If protection routing claims completeness but forward owner exists without membership:

- targeted integrity defect;
- deletion prohibited.

**PASS with candidate LAW 5.13-19 + R1/R3.**

## A2 — cleanup proof built under G1, engine adoption G2 wins first

Cleanup contract/current interpretation changes => proof stale/retry.

**PASS after R1.**

## A3 — message envelope delete while unresolved Interaction still needs exact input

Blocked by Interaction/message cleanup contract.

**PASS after R2.**

## A4 — message envelope delete after Interaction content promoted to stable semantic plan/fingerprint

Opaque provenance allowed; survivor validates.

**PASS.**

## A5 — Story verified exact, envelope removed with no digest survivor

Forbidden or exactness revoked.

**PASS.**

## A6 — old Git blob exact text remains reachable

Ordinary runtime treats as semantically non-retained; no verbatim resurrection.

**PASS.**

## A7 — security incident demands true erasure

Ordinary 5.13 cannot satisfy; explicit exceptional owner/security process required.

**PASS as scope boundary.**

## A8 — DeleteRef lost response, ref absent

Targeted ref read => cleanup confirmed.

**PASS after R4.**

## A9 — DeleteRef lost response, name now points elsewhere

Do not delete; conflict/integrity maintenance outcome.

**PASS after R4/R10.**

## A10 — cleanup interrupted halfway through independent candidates

Current state contains subset; next activation rediscovers remainder.

**PASS.**

## A11 — cleanup interrupted inside one campaign replace+delete transaction before ref selection

No current authority change; prepared objects nonauthority.

**PASS.**

## A12 — current campaign ref selection succeeds but local ACK lost

Step 5.6 resolves actual current tree; no double semantic effect.

**PASS.**

## A13 — chronology derived index deleted while source relations needed

Index successor/rebuild contract only; source retention independently protected.

**PASS.**

## A14 — chronology evidence body deleted because no current deadline uses it, but a retained causal provenance owner does

Protected consumer blocks via Step 5.9.

**PASS.**

## A15 — old checkpoint useful for diagnostics but no explicit retention contract

May be removed; future diagnostics report unavailable.

**PASS after R12.**

## A16 — current sparse disclosure row appears old

Not ordinary candidate.

**PASS.**

## A17 — terminal world actor appears unused

5.13 has no generic world deletion policy; retain unless owner-specific contract exists.

**PASS.**

---

# 15. Required candidate-to-canonical tightenings

Canonical consolidation must add/strengthen at least:

1. **R1 Cleanup interpretation/adoption barrier** — cleanup contract generation participates in compatible runtime/catalog adoption/migration.
2. **R2 Interaction/message linkage discharge** — raw message ref cannot become opaque until accepted meaning/idempotency is independently safe.
3. **R3 Protection-routing generation lifecycle** — old correctness-complete routing retires only after compatible successor selection; no self-authorization.
4. **R4 Ref-delete ambiguity protocol** — targeted exact ref verification; unexpected name reuse blocks delete.
5. **R5 Semantic deletion vs storage erasure documentation** — no misleading secure-delete promise.
6. **R6 Story supported migration continuity** — retain enumeration only for currently promised compatible migration/reprojection paths, not arbitrary future replay.
7. **R7 Compact idempotency anchor measurement/Step-6 carry-forward** — no premature TTL.
8. **R8 Natural-owner exact-certification survivor** — avoid generic per-message tombstones.
9. **R9 Pinned readers do not create durable GC roots** — current-record support reads pin exact source revision.
10. **R10 Nonreused live epoch/ref identity + unclassified leftover behavior**.
11. **R11 Bulk generation retirement respects sparse cross-generation survivors/references**.
12. **R12 Potential diagnostic usefulness is not universal retention authority**.

---

# 16. Architecture verdict

**PASS WITH REQUIRED RESOLUTION.**

The candidate's owner-gated hybrid remains superior to:

- universal mark/sweep;
- generic reference counts;
- retain-everything;
- owner-local-only cleanup lacking bounded negative-proof support.

No adversarial finding requires:

- a new gameplay/product retention promise;
- weaker recovery;
- weaker Selective Exact semantics;
- history rewrite/force push;
- mandatory background cleanup;
- new canonical GC owner.

All blockers can be resolved mechanically in the resolution gate/canonical specification.

---

# 17. No human decision required

The owner delegated mechanical Step-5.13 architecture and all surviving choices are derivable from existing canonical laws.

A human decision would become necessary only if the project later chooses to:

- promise secure erasure of previously committed Git content;
- expire idempotency/provenance earlier to reduce storage;
- weaken historical/recovery evidence guarantees;
- introduce generic world-history deletion;
- permit history rewrite/force update;
- mandate cleanup on a user-visible latency path.

None is required to close Step 5.13.
