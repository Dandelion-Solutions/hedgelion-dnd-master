# HDM Implementation Planning — LIVE / Temporal Completeness-Companion Handoff Amendment

Status: **CURRENT HIGHEST-PRECEDENCE MANDATORY AUTHOR REPAIR — PLANNING ONLY / NO PRODUCTION IMPLEMENTATION**
Date: 2026-09-14
Finding: **F36 — SIGNIFICANT — campaign/LIVE authority movement lacks an explicit atomic temporal-routing handoff**

## 1. Finding

The current package has two individually sound completeness-protected routing contracts:

- `STATE/RUNTIME/TEMPORAL_ROUTING.yaml` for campaign-source temporal enrollment, with `LIVE_STATE.temporal_routing` as the corresponding exact-source LIVE form;
- `STATE/RUNTIME/LIVE_ROUTING.yaml` for current selected LIVE route/claim completeness.

WP-15 requires derivative temporal enrollment to move coherently with owner/provider transfer and forbids an acknowledged healthy state in which an armed occurrence is reachable only from obsolete dependency state. The temporal-routing overlay also requires campaign routing never to claim LIVE-owned current truth.

Findings 29–31 seed exact native state and required derivative companions into the prepared LIVE candidate and make absorption materialize required derivative deltas forward. Finding 30 makes LIVE route selection/release update `LIVE_ROUTING.yaml` in the same campaign authority transaction.

However, no current executable route explicitly composes those two companion transitions when authority moves between campaign and LIVE. The package therefore permits a worker to perform route selection that:

```text
adds selected epoch to LIVE_ROUTING.yaml
but leaves the claimed armed owner in campaign TEMPORAL_ROUTING.yaml
```

while the selected LIVE candidate also contains its embedded temporal membership. Both companions are individually schema-valid but jointly claim completeness for different current source placements. The reverse absorption path can similarly remove `LIVE_ROUTING` without establishing the required campaign temporal membership in the same campaign closure.

This is a cross-companion atomicity/currentness defect. It does not change temporal semantics, LIVE claim semantics or publication ownership.

## 2. Source-placement invariant

For every independently-due armed native owner/occurrence, current completeness-protected temporal membership exists in exactly the current mutable source domain selected for that owner:

```text
WriteAuthorityLookup(owner) == CAMPAIGN
    -> required current temporal membership is in campaign TEMPORAL_ROUTING

WriteAuthorityLookup(owner) == LIVE(E)
    -> required current temporal membership is in exact selected E.LIVE_STATE.temporal_routing
```

A prepared/nonselected LIVE candidate may contain prospective seeded temporal routing, but that routing is non-authoritative until campaign route selection accepts.

Campaign `TEMPORAL_ROUTING` may not remain current enrollment for a claimed LIVE-owned occurrence. Conversely, after confirmed absorption/route release, the predecessor LIVE copy may remain historical/residual source bytes but is no longer current routing authority; campaign temporal membership must be established for every surviving armed occurrence before CAMPAIGN authority is exposed.

The same native owner must never be acknowledged as current temporal enrollment in both source domains at once.

## 3. Campaign -> LIVE opening handoff

### 3.1 Candidate preparation

Finding 29 opening seed is extended only in this exact respect:

```text
pin H
-> hydrate every claimed owner/partition at H
-> derive its exact temporal route entry at source_scope=LIVE when the owner is independently due/armed
-> construct candidate LIVE_STATE.native_state_entries
   + LIVE_STATE.temporal_routing
-> validate seed equivalence
-> prepare candidate ref
```

The prospective LIVE temporal entries are not current authority before selection.

Campaign temporal routing remains unchanged while the candidate is merely prepared.

### 3.2 Route-selection publication

When campaign publication selects the prepared epoch, the frozen campaign route-selection delta must include all of the following applicable changes in **one RD-06 campaign resulting-tree closure**:

```text
+ LIVE_ROUTING selected-route entry
+ scene/current nomination projections where required by their non-authoritative owners
- campaign TEMPORAL_ROUTING entries for claimed occurrences whose current source moves to LIVE
+ any campaign-side routing/index companion changes already required by current owners
```

Before acknowledgement, validate against the exact prepared LIVE candidate that every removed campaign temporal membership has the required equivalent current/prospective LIVE temporal membership under the same opening basis/owner occurrence.

Selection is rejected if:

- a claimed armed occurrence would lose temporal enrollment;
- a campaign temporal membership remains current for an owner becoming LIVE-owned;
- the candidate LIVE temporal entry is missing/incompatible/stale relative to the seeded owner occurrence;
- `LIVE_ROUTING` and the temporal handoff are based on different opening/claim bases.

A rejected/stale campaign publication changes none of these campaign companions. An indeterminate acknowledgement is reconciled by reading the exact resulting campaign authority state; the worker does not independently replay only one companion delta.

## 4. LIVE mutation while selected

Once selected, the existing temporal-routing overlay remains controlling:

- a LIVE owner mutation that arms/rearms/unarms/claims/terminalizes a temporal occurrence updates `LIVE_STATE.native_state_entries` and `LIVE_STATE.temporal_routing` in the same exact-source CAS when required;
- campaign `TEMPORAL_ROUTING` does not shadow those claimed owners;
- unrelated campaign-owned temporal owners remain in campaign routing.

No campaign publication is introduced for ordinary LIVE-local temporal lifecycle changes solely to mirror them.

## 5. LIVE -> campaign absorption handoff

Finding 31 frozen absorption is strengthened so its campaign delta contains the complete surviving temporal-source handoff derived from exact terminal `Lf`:

```text
validate exact CLOSED Lf
-> validate final native_state_entries + Lf.temporal_routing
-> materialize surviving native owners under normal campaign routes
-> derive/validate required campaign TEMPORAL_ROUTING entries for surviving armed occurrences
-> include all other required derivative companion/index deltas
-> remove selected route from LIVE_ROUTING
-> publish one campaign resulting-tree closure
```

The campaign publication is invalid if it would:

- expose CAMPAIGN authority for a surviving armed owner without its required campaign temporal membership;
- retain a current campaign temporal route for an occurrence whose owner remains selected LIVE;
- create a campaign temporal entry whose exact native owner is absent/incompatible in the resulting tree;
- remove `LIVE_ROUTING` while temporal/current owner materialization is incomplete.

Publication rejection/ambiguity leaves the exact CLOSED source as `CLOSED_UNABSORBED` current truth with zero ordinary writers. It does not partially adopt campaign temporal routing, reopen the source or rerun accepted execution.

## 6. No distributed transaction / no semantic merge

This repair uses the already accepted two-domain sequence:

```text
prepared/exact LIVE source state first
then one campaign publication that moves campaign-domain routing authority
```

There is no atomic transaction spanning a mutable LIVE ref and campaign ref.

Opening uses an already prepared immutable candidate basis; absorption uses exact terminal `Lf`. The campaign publication atomically changes only campaign-domain files/companions in its one resulting tree.

Technical order does not establish fictional chronology.

## 7. Recovery semantics

RD-07 current-source recovery must cross-check the companions after pinning current campaign authority:

1. load/validate campaign `LIVE_ROUTING.yaml`;
2. load/validate campaign `TEMPORAL_ROUTING.yaml`;
3. exact-resolve every selected LIVE source;
4. validate selected LIVE `temporal_routing` against exact hydrated native owners;
5. reject/block scoped integrity if one current native owner is simultaneously enrolled as campaign-current and selected-LIVE-current, or if neither domain contains required enrollment;
6. rebuild Agenda from the union of **disjoint current source-domain enrollments** only after those checks.

Recovery never resolves a split by choosing the newest file, scanning all refs or treating duplicate enrollment as harmless.

## 8. Tests / proof

Add cross-companion integration scenarios, conceptually under RD-09/RD-06/RD-07 proof surfaces:

```text
LiveTemporalRoutingHandoffTests
```

Required cases:

- prepared candidate may contain temporal routing while campaign membership remains current before selection;
- accepted route selection removes moved campaign membership and establishes selected `LIVE_ROUTING` in one campaign publication;
- selected LIVE owner cannot remain current in campaign temporal routing;
- selection rejects if candidate lacks required equivalent temporal entry;
- stale/rejected selection leaves campaign temporal membership and route table unchanged;
- lost acknowledgement reconciles the complete campaign resulting tree, not one companion independently;
- selected LIVE lifecycle changes only exact-source temporal routing for claimed owner;
- absorption establishes campaign temporal membership and removes `LIVE_ROUTING` in one campaign publication;
- rejected/indeterminate absorption leaves CLOSED_UNABSORBED source current and does not expose partial campaign enrollment;
- recovery detects duplicate cross-domain enrollment and missing-both-domain enrollment;
- no broad scan, mtime/newest-wins, branch-order or fictional chronology fallback exists.

Focused verification after implementation is authorized:

```bash
python3 -m unittest DEV.TESTS.test_rd08_temporal.TemporalRoutingCompletenessTests -v
python3 -m unittest DEV.TESTS.test_rd09_access_live.LiveTemporalRoutingHandoffTests -v
python3 -m unittest DEV.TESTS.test_rd06_save_publication -v
python3 -m unittest DEV.TESTS.test_rd07_recovery -v
python3 DEV/TOOLS/run_maintenance_audit.py
python3 -m unittest discover -s DEV/TESTS -p 'test_*.py'
```

Exact concrete class placement may follow the existing RD test modules, but one item-bound cross-companion witness is mandatory; broad temporal tests and broad LIVE tests passing separately do not discharge F36.

## 9. Execution / coverage / proof amendment

Add checkpoint join:

```text
RD08_TEMPORAL_ROUTING_LOCAL_SEMANTIC_READY
+ RD09_LIVE_OPENING_SEED_AND_ROUTE_LOCAL_READY
+ RD06_CAMPAIGN_PUBLICATION_MECHANISM_READY
    -> LIVE_TEMPORAL_ROUTE_SELECTION_HANDOFF_READY
```

and for absorption:

```text
RD09_EXACT_CLOSED_NATIVE_HANDOFF_READY
+ RD08_TEMPORAL_ROUTING_LOCAL_SEMANTIC_READY
+ RD06_CAMPAIGN_PUBLICATION_MECHANISM_READY
    -> LIVE_TEMPORAL_ABSORPTION_HANDOFF_READY
```

These are bounded integration joins, not whole-RD barriers.

Forward coverage:

```text
WP15-16..23 temporal completeness/lifecycle
+ WP16 selected LIVE currentness/route laws
-> RD-08 temporal entry semantics
-> RD-09 candidate/LIVE exact-source packing/currentness
-> RD-06 atomic campaign companion handoff
-> RD-07 disjoint current-source recovery
-> cross-companion proof
```

The post-graph proof witness set gains logical row `PG34`:

```text
PG34  campaign<->LIVE temporal completeness handoff is gap-free and non-duplicating
      -> LiveTemporalRoutingHandoffTests
      -> FAILURE_INJECTION + INTEGRATION_SCENARIO
```

R077 temporal package proof and applicable R080 LIVE proof are incomplete without this cross-companion witness.

## 10. Scaffold / blank state

Blank campaign continues to contain valid empty:

```text
STATE/RUNTIME/TEMPORAL_ROUTING.yaml
STATE/RUNTIME/LIVE_ROUTING.yaml
```

No LIVE source exists and no cross-companion handoff is required at bootstrap. Empty validity does not weaken missing/corrupt companion fail-closed behavior after gameplay state exists.

## 11. Disposition

```text
F36: REPAIRED_IN_PLANNING
CAMPAIGN_TO_LIVE_TEMPORAL_HANDOFF_ATOMIC_WITH_LIVE_ROUTE_SELECTION: REQUIRED
LIVE_TO_CAMPAIGN_TEMPORAL_HANDOFF_ATOMIC_WITH_LIVE_ROUTE_REMOVAL: REQUIRED
CROSS_DOMAIN_DUPLICATE_CURRENT_TEMPORAL_ENROLLMENT: INTEGRITY_CONFLICT
DISTRIBUTED_TRANSACTION_INTRODUCED: NO
NEW_RD: NO
NEW_SEMANTIC_OWNER: NO
ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```

This author-side repair remains independently unconfirmed. The broader typed graph audit continues and Senior handoff remains blocked.