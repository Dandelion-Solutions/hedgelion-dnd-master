# Implementation Planning — PLAYER Access Transition Executable Closure Amendment

Status: **MANDATORY AUTHOR REPAIR — PLANNING ONLY / NO PRODUCTION IMPLEMENTATION**
Date: 2026-09-14
Finding: **AUTHOR GRAPH FINDING 37 — SIGNIFICANT**

## Finding

The current package contains the accepted semantics for PLAYER membership/control changes and contains several downstream pieces that consume a hypothetical campaign access change, but it does not yet define the worker-facing executable producer of that change.

The gap is visible across the current package:

- WP-16 defines active/inactive PLAYER membership, controlled-PC separation, campaign-only access/routing authority, close-before-revocation and no-window campaign authority closure;
- shipped `GAME/CORE/MULTIPLAYER.md` defines self-enrollment, leave/removal/reactivation and controller-change behavior;
- the principal-routing repair requires stable external binding changes to update `PRINCIPAL_PLAYER_ROUTING.yaml` in the same campaign closure;
- the WP-16 executable-closure repair adds `classify_additive_authorization_change(...)`, but that function classifies an already-proposed `campaign_change`; it does not construct or validate the PLAYER transition itself;
- base RD-09 `access_control.py` plans principal resolution and authorization checks, but no mutation assembler for PLAYER membership/control/binding state.

Therefore a worker still has to invent how to build a PLAYER authority transition, which bytes/fields it may replace, how it preserves independently-owned PLAYER fields, when the principal-routing companion participates, and how the change is frozen/revalidated before RD-06 publication. That is a worker-must-invent seam and a proof-without-mechanism defect for the WP-16 revocation/additive-transition witnesses.

This is an implementation-planning defect. The canonical semantics are already accepted; no architecture reopen or Product Owner decision is required.

---

# 1. Required RD-09 transition producer

RD-09 must add one explicit campaign-domain access-transition producer in `GAME/TOOLS/access_control.py`.

Conceptual operation set:

```text
PlayerAccessTransitionKind :=
    CREATE_BINDING
  | REBIND_STABLE_PRINCIPAL
  | ACTIVATE_BINDING
  | DEACTIVATE_BINDING
  | TRANSFER_CONTROL
```

This list covers the current v1 PLAYER lifecycle/control mutations already owned by accepted access-control semantics. It does not create a generic authorization database or invent new policy grants.

Conceptual frozen planning interface:

```text
freeze_player_access_transition(
    request,
    pinned_campaign_basis,
    current_player_state,
    current_principal_player_route,
    current_selected_live_routes,
    current_collaboration_route_refs,
) -> FrozenPlayerAccessTransition | DENIED | BLOCKED_INTEGRITY
```

The result is an ephemeral immutable transition plan. It is not a new durable record family, lock, transaction log or authority owner.

The frozen plan must carry enough exact basis to revalidate before publication:

```text
FrozenPlayerAccessTransition {
    kind
    pinned_campaign_revision
    target_player_id or create_identity_basis
    exact_before_player_value when one exists
    typed_player_field_delta
    stable_principal_binding_before/after
    controlled_pc_relation_before/after
    membership_status_before/after
    principal_route_delta when applicable
    affected_live_routes / required LIVE transition disposition
    collaboration_reconciliation_required
    authorized campaign path set
}
```

Exact field names may follow the final native PLAYER structure. The semantic requirements above are mandatory.

---

# 2. Fresh-base / field-preservation law

No access-control path may serialize a stale whole PLAYER record assembled from an earlier read.

Every transition must:

1. pin one current campaign basis;
2. direct-load the exact current PLAYER owner where one exists;
3. validate the operation against current principal/creator/membership/control policy;
4. construct a typed semantic delta only for fields owned by the requested access transition;
5. preserve every unrelated current PLAYER field from the exact current base, including RD-12 `collaboration_route_refs` and any other admitted owner fields;
6. if the campaign basis changes before publication, discard/refreeze or deterministically revalidate/recompose from the new current PLAYER value;
7. never use blind text merge, stale full-record replacement or last-writer-wins semantics.

This rule composes with F35. F35 guarantees that the final strict schema admits all required fields; F37 guarantees that runtime mutation of one concern does not erase another concern's current PLAYER state.

---

# 3. Stable-principal routing join

For `CREATE_BINDING` or `REBIND_STABLE_PRINCIPAL`, the resulting campaign closure must include the exact `PRINCIPAL_PLAYER_ROUTING.yaml` delta required by Finding 9.

```text
PLAYER stable binding transition
+ PRINCIPAL_PLAYER_ROUTING delta
  MUTATES_WITH
one RD-06 campaign resulting-tree publication
```

The route remains non-authoritative. Authorization after publication still reloads exact current PLAYER state.

Activation/deactivation with unchanged stable principal binding does not rewrite the route solely because status changed; current status is re-read from PLAYER as already required by Finding 9.

A route delta whose resulting PLAYER owner is absent/mismatched, or a changed stable binding without its required route delta, is an integrity failure and may not publish.

---

# 4. LIVE transition join

The F7 classifier remains the owner of whether an access change may avoid LIVE rollover:

```text
FrozenPlayerAccessTransition
  -> classify_additive_authorization_change(...)
     -> NO_LIVE_ROLLOVER | LIVE_TRANSITION_REQUIRED
```

If `LIVE_TRANSITION_REQUIRED`:

1. freeze/close every affected selected LIVE source by its exact-source CAS using the accepted single- or multi-LIVE forward transition;
2. prove each required terminal exact source revision;
3. only then publish the campaign-domain PLAYER/control transition and required campaign routing/companion deltas;
4. derive/adopt any successor LIVE source only from the new current campaign authority basis.

If `NO_LIVE_ROLLOVER`, the campaign transition may publish only after the classifier's current-basis predicates remain true at publication revalidation.

No operation may mutate immutable LIVE claims in place, reopen a predecessor, or rely on branch existence/presence as authorization.

---

# 5. Collaboration join boundary

A PLAYER transition that can materially change an outstanding voluntary-agency requirement — membership status, controlled-PC relation or applicable authorization basis — sets:

```text
collaboration_reconciliation_required = true
```

Such a transition is not publishable until RD-12 supplies the bounded reconciliation result required by WP-17 Law 27. The exact producer of that reconciliation is defined by the later-precedence F38 amendment; F37 establishes the mandatory access-transition side of the join.

Stable-principal rebinding with no change to membership/control/authorization still revalidates any current collaboration authority binding when applicable; inability to prove non-impact fails closed rather than silently publishing.

---

# 6. RD-06 publication integration

RD-06 remains the campaign publication mechanism owner. It does not acquire access-control semantics.

After all required preconditions/joins are satisfied, publication freezes one resulting campaign tree containing all campaign-domain deltas required by the transition, including as applicable:

- exact PLAYER owner mutation/creation;
- `PRINCIPAL_PLAYER_ROUTING.yaml` delta;
- collaboration obligation generation/resulting PLAYER-route deltas supplied by RD-12;
- LIVE route/release/absorption companions required by the accepted LIVE transition;
- other already-mandatory campaign companions whose owner transition is affected.

The resulting commit is single-parent from the pinned current campaign revision and is published through the accepted non-force compare-and-swap boundary.

A stale-head rejection refreezes/revalidates from current owner state. It never reapplies a stale PLAYER serialization.

---

# 7. RD-07 recovery / retry

Recovery of an indeterminate access transition uses current campaign owner state and current completeness companions; there is no new durable transition journal.

The retry path must distinguish:

- transition already fully reflected in current resulting state -> idempotent success/reconciliation;
- prior attempt not accepted -> refreeze from current basis;
- split/inconsistent PLAYER / principal-route / collaboration-companion state -> integrity/repair handling, not optimistic completion;
- LIVE predecessor already CLOSED while campaign transition is not yet accepted -> preserve truthful CLOSED_UNABSORBED state and continue forward; never reopen.

---

# 8. Required tests / proof repair

Add a focused RD-09 group conceptually:

```text
PlayerAccessTransitionTests
```

Required cases:

1. open-contributor self-enrollment creates only the authorized PLAYER binding plus required principal-route delta and preserves unrelated campaign state;
2. self-deactivation changes only permitted membership fields and preserves stable identity/control history/unrelated PLAYER fields;
3. creator deactivation obeys owner-only authority and current-basis validation;
4. self-reactivation reuses the same PLAYER identity and does not silently reclaim a transferred PC;
5. creator reactivation after creator removal is distinct from self-reactivation;
6. stable-principal rebind publishes PLAYER + principal-route delta together; split publication is impossible;
7. controller transfer uses exact current before-state and cannot be based on stale PLAYER bytes;
8. access transition preserves current `collaboration_route_refs` unless the supplied RD-12 reconciliation intentionally changes them;
9. stale campaign HEAD forces refreeze/revalidation; stale whole-record replacement is rejected;
10. LIVE-impacting revocation closes/finalizes affected source(s) before campaign authority withdrawal;
11. safe additive activation leaves unrelated LIVE unchanged only when the F7 classifier proves all predicates;
12. an access change requiring collaboration reconciliation cannot publish without the RD-12 reconciliation result;
13. no broad PLAYER scan, cache/session authority, presence authority or last-writer-wins fallback is introduced.

Update the WP-16 proof mapping for duties 11 and 12 so the witness route includes `PlayerAccessTransitionTests` plus the existing LIVE lifecycle/classifier and RD-06 publication proof. LIVE lifecycle tests alone are insufficient to prove the campaign mutation producer.

---

# 9. Execution graph amendment

Add checkpoints:

```text
RD09_PLAYER_ACCESS_TRANSITION_LOCAL_READY
RD09_PLAYER_ACCESS_LIVE_CLASSIFICATION_READY
RD09_PLAYER_ACCESS_PRINCIPAL_ROUTE_JOIN_READY
```

Required edges:

```text
RD09_PLAYER_ACCESS_TRANSITION_LOCAL_READY
  -> RD09_PLAYER_ACCESS_LIVE_CLASSIFICATION_READY

F9 principal-route producer ready
+ RD09_PLAYER_ACCESS_TRANSITION_LOCAL_READY
  JOIN_BEFORE_INTEGRATION
RD09_PLAYER_ACCESS_PRINCIPAL_ROUTE_JOIN_READY
```

For access transitions that can affect collaboration requirements, final campaign publication additionally waits for the F38 RD-12 reconciliation checkpoint.

For transitions requiring LIVE close/forward movement, final campaign publication waits for the accepted exact terminal LIVE source checkpoint(s) supplied by the existing F7/F27–F31 path.

These are checkpoint-level joins, not whole-RD serialization edges.

---

# 10. Non-goals

This repair does not add:

- a new authorization database;
- a generic ACL DSL;
- background membership polling;
- a distributed transaction or persistent saga coordinator;
- a new semantic PLAYER owner;
- a second principal-routing authority;
- a new LIVE claim mutation mechanism;
- whole-record last-writer-wins merge semantics.

---

## Disposition

```text
AUTHOR_GRAPH_FINDING_37: REPAIRED_IN_PLANNING
SEVERITY: SIGNIFICANT
ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
INDEPENDENT_CONFIRMATION: PENDING
```
