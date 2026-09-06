# HDM Publication Currentness — Supported Ref Monotonicity Repair Amendment

Status: **CANONICAL REPAIR CANDIDATE — MANDATORY SENIOR REPAIR REVIEW PENDING**

Date: 2026-09-06

Scope: bounded whole-project audit repair for publication/currentness realization only.

This amendment reconciles the accepted publication/currentness architecture with the ref-transition capability actually available in the supported ChatGPT Work / GitHub Connector profile. It does not reopen gameplay semantics, authority ownership, creator-login policy, durability product policy, migration compatibility policy, LIVE ownership, or the versioning taxonomy.

Controlling upstream/current owners remain:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-6-campaign-publication-crash-consistency-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-08-20-step-5-8-multiplayer-live-epoch-ownership-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-09-02-r2-7-WP-13-durability-save-publication-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-17-async-collaboration-agency-safe-progression-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-canonical-spec.md`;
- `DEV/docs/superpowers/specs/2026-09-05-r2-7-WP-20-engine-update-schema-evolution-migration-canonical-spec.md`.

Where one of those sources uses the shorthand `exact-source CAS` or wording that assumes an expected-old-ref argument in the Connector, this amendment supplies the supported Git-backed realization. All unrelated laws remain unchanged.

---

## 1. Capability finding

The current connected ref-move capability exposes the target repository/ref, the new commit SHA and a `force` flag. With `force=false`, the update is non-force/fast-forward-only. It does **not** expose a separate expected-old/current-ref SHA argument.

Therefore:

```text
preflight ref == H
```

is an early-stale check, not an atomic compare-and-swap by itself.

The current branch/ref creation capability is create-if-absent: creating a ref that already exists is a rejected creation, not an overwrite path.

This capability shape is sufficient for the already-accepted Step-5.6 stale-write invariant when the supported authority refs obey the monotonicity contract below. It is not evidence for an API primitive that the host does not expose.

---

## 2. Supported-ref monotonicity contract

### PCR-1 — Existing authoritative refs are append-only under normal HDM publication

For campaign refs and Git-backed LIVE refs admitted by the supported automatic HDM publication path, normal authority-changing movement is only:

```text
current ref A
-> descendant commit B
-> ref A -> B with force=false
```

No normal HDM publication path performs ref rewind, history replacement, force update, deletion/recreation to recover stale work, or branch-name substitution to bypass conflict.

This restates Step-5.6 LAW 5.6-14/21 as an explicit supported-host realization constraint.

### PCR-2 — Single parent plus non-force fast-forward is the exact-source fence

For a prepared existing-ref publication based on pinned authoritative source `H`:

```text
parent(C) = H
AND
update target ref -> C with force=false
```

is the admitted Git-backed exact-source fence.

If another accepted writer advances the ref from `H` to `A` before the final transition, stale sibling `C(parent=H)` is not a descendant of `A`; the non-force transition `A -> C` is rejected. A further accepted descendant `D` does not make the stale sibling valid.

The runtime SHALL NOT describe this realization as though the Connector accepted an `expected_old_sha=H` argument. `exact-source CAS` remains the logical concurrency law; parentage plus non-force fast-forward is the supported Git realization.

### PCR-3 — Ref creation is create-if-absent, not stale update

Initial campaign/LIVE ref creation is a distinct operation:

```text
prove/expect target ref absent under owning creation protocol
-> create prepared initialization/opening commit
-> create target ref at that commit
```

If the target ref already exists at creation time, creation rejects/fails closed. The runtime does not reinterpret an existing ref as permission to overwrite or continue initialization on top of an unknown source.

Initial campaign commit parentage to the pinned storage/default basis remains WP-19-owned provenance; after creation, ordinary publication uses PCR-1/PCR-2.

### PCR-4 — Non-monotonic history is outside the supported automatic publication model

Observed evidence of any of the following invalidates ordinary exact-source proof for the affected ref:

- force rewrite;
- ref rewind to an ancestor/older lineage;
- history replacement/divergence not produced by admitted non-force progression;
- deletion/recreation of an authority ref;
- another non-monotonic movement that can make previously stale prepared work appear fast-forward-valid again.

Disposition:

```text
NON_MONOTONIC_HISTORY
-> invalidate all prepared attempts whose source proof crossed the discontinuity
-> pin/read current authority again
-> perform bounded owner/currentness/integrity recovery
-> do not auto-publish the old prepared commit
-> do not force a preferred lineage back into place
```

If the host profile cannot preserve the non-force/create-if-absent guarantees required above, publication capability for that profile is unavailable and the operation fails closed.

---

## 3. Publication epistemics remain richer than ref equality

### PCR-5 — Confirmed accepted response remains current operation evidence

A confirmed accepted non-force ref response selecting intended commit `C` proves that publication succeeded at that response point. No gratuitous reread is required merely to re-prove the acknowledgement.

This evidence is not a lease against later lawful movement.

### PCR-6 — Indeterminate result uses lineage plus current closure

After an indeterminate final ref outcome, read exact current authoritative head `D` and use bounded lineage/current-closure evidence:

```text
D == C
    -> prove required current closure at C

C proven reachable ancestor of D
    -> C is durable lineage evidence
    -> inspect only D-vs-C changes intersecting required closure/dependency/authorization footprint
    -> treat the durability/publication promise as satisfied only if current D supplies compatible current required closure

C proven absent from D lineage
    -> C does not prove current closure
    -> repin/revalidate from D

bounded lineage/current-closure evidence unavailable
    -> remain INDETERMINATE / recovery-required
```

A later lawful descendant does not retroactively turn an actually accepted publication into a rejected publication. Conversely, ancestry alone does not prove that the current required closure still has the needed meaning.

Exact `ref == intended_commit` is therefore neither the only success evidence nor a substitute for current-closure proof after later movement.

### PCR-7 — Rejected stale transition remains old/current authority

A server-confirmed non-fast-forward rejection of stale `C(parent=H)` does not establish `C`. The currently selected ref lineage remains authority. Rebuild/reconcile only from current owner evidence; never force or blind-retry.

---

## 4. LIVE reconciliation

Step-5.8 and WP-16 continue to require logical exact-source fencing for every LIVE transition.

For the current Git-backed Connector realization:

```text
pin selected LIVE ref/source L
-> build one complete successor commit/source with parent/basis L
-> non-force fast-forward selected LIVE ref to successor
```

is the admitted realization of that fence under PCR-1/PCR-2.

WP-16 wording that allows “a Connector operation with exactly equivalent expected-source CAS semantics” does not imply the currently available ref-update action has an expected-source parameter. A future host primitive may satisfy the same logical law directly, but the current supported profile relies on monotonic ref history plus parentage/non-force selection.

LIVE ambiguity continues to require exact current source/ref plus bounded lineage/current closure before an accepted edge may be inferred. A successful technical ref transition never substitutes for current application authorization.

---

## 5. Consumer reconciliation

### WP-17

`runtime.collaboration_obligation` and completeness-protected PLAYER routing companions remain campaign-owned and publish through the campaign durability closure. No WP-17-specific ref primitive is introduced. Campaign movement/currentness consumes PCR-1..PCR-7 through WP-13.

### WP-19

Initial campaign publication remains one complete from-scratch tree + initialization commit + create-if-absent campaign ref. Existing campaign publications after creation consume PCR-1/PCR-2 through the normal campaign publication contract.

A duplicate/racing initial ref creation is a creation conflict/failure, not authority to overwrite an existing campaign ref.

### WP-20

Prepared migration remains based on pinned `H` and publishes through the normal campaign transaction. A stale prepared migration cannot overwrite an intervening accepted fast-forward because its commit remains parented to old `H`.

Ambiguous migration publication consumes PCR-6 / WP13-L33 semantics. A current lawful descendant containing intended migration commit is not automatically classified as “rejected/stale”; current closure must be checked. A current lineage that excludes the intended commit does not prove migration publication.

No migration-specific CAS, rollback ref, force path or publication owner is added.

---

## 6. Machine/acceptance matrix

Every ref movement admitted by the supported model has an explicit disposition:

| ID | Initial state | Operation/evidence | Expected disposition |
|---|---|---|---|
| `PCR-A1` | target ref absent | create initialization/opening ref at prepared commit | ACCEPTED only if create-if-absent succeeds |
| `PCR-A2` | target ref exists | competing create of same ref name | REJECTED / creation conflict; no overwrite |
| `PCR-A3` | ref at `H` | publish `C(parent=H)` with `force=false` | ACCEPTED fast-forward |
| `PCR-A4` | `H -> A` already accepted | stale sibling `C(parent=H)` attempts `A -> C` with `force=false` | REJECTED non-fast-forward |
| `PCR-A5` | `H -> A -> D` already accepted | same stale sibling attempts `D -> C` | REJECTED non-fast-forward |
| `PCR-A6` | intended `C` response indeterminate; current `D` is descendant of `C` | bounded lineage + required-current-closure proof | lineage success evidence only; promise succeeds iff current closure compatible |
| `PCR-A7` | current head excludes `C` or history discontinuity/rewind is observed | ambiguity/currentness recovery | no success inference; repin or fail closed/integrity recovery |

Executable acceptance coverage lives in `DEV/TESTS/test_publication_ref_fence_contract.py`.

---

## 7. Authority and product-policy non-change

This repair does not change:

- creator-only versus storage-owner authority;
- PLAYER/control authorization;
- creator-login continuity policy;
- SAVE/HARD semantics;
- LIVE claim/lifecycle ownership;
- migration compatibility/evidence/path law;
- chronology;
- ruleset/package identity;
- any version namespace.

Creator-login rename continuity remains **NOT SUPPORTED** under `DEV/docs/superpowers/specs/2026-09-06-hdm-creator-login-continuity-owner-decision.md`.

```text
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
UPSTREAM_WHOLESALE_REOPEN_REQUIRED: NO
VERSIONING_TAXONOMY_REOPENED: NO
```
