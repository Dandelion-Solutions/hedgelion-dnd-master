# Implementation Planning — Campaign Access-Policy Transition Addendum

Status: **MANDATORY AUTHOR REPAIR — PLANNING ONLY / NO PRODUCTION IMPLEMENTATION**
Date: 2026-09-15
Finding: **AUTHOR FINDING 59 — SIGNIFICANT**

## 1. Proven planning defect and controlling owners

ACCESS_CONTROL campaign ownership and House-Rules HR-8 already admit creator-only campaign mode/join-policy changes and grant/revoke of the existing PLAYER.policy_authority.mechanical_override_policy field. MULTIPLAYER specifies that join-policy changes do not revoke existing bindings. WP-16 Laws 4, 7, 18 and 37–41 require current operation authority and no-window LIVE transitions; WP-17 Law 27 requires reverse reconciliation when applicable authority changes materially.

RD-09 Task 2 supplies authorization validators; Task 7 and F7 supply LIVE classification/forward movement. F37 supplies five PLAYER lifecycle/control/binding mutations, but none assembles a campaign mode, join-policy or mechanical-override grant change. F38 is invoked by that PLAYER mutation producer. RD-13's current-mode admission and RD-16's preserved policy fields are consumers/structure, not the omitted mutation producer. The 16-RD/37-overlay package therefore leaves the exact mutation, complete affected set and joined publication to worker invention.

A concrete mode change can affect several PLAYERs and the same obligation generation through several route holders. Independent per-PLAYER reconciliation against different provisional after-states cannot establish one coherent successor. A grant-only write must also preserve unrelated current PLAYER fields; join-policy changes must not be misclassified as membership revocation.

This overlay extends F37/F38 for these already-owned operations. It adds no authorization class, stable creator contract, persistent transition journal, generic ACL service or gameplay policy. Creator evidence remains subject to the current owner and its unresolved architecture gate: unresolved creator authority denies the request. No login-to-stable-ID substitution or creator placement decision is authorized here.

## 2. Exact operation and native-field scope

RD-09 extends the existing GAME/TOOLS/access_control.py realization with:

~~~text
AccessPolicyTransitionKind :=
    SET_CAMPAIGN_MODE
  | SET_JOIN_POLICY
  | SET_MECHANICAL_OVERRIDE_GRANT

freeze_access_policy_transition(
    request,
    pinned_campaign_basis,
    current_creator_and_principal_evidence,
    exact_current_manifest,
    current_principal_player_routing,
    exact_current_player_loader,
    current_selected_live_routing,
    budget
) -> FrozenAccessPolicyTransition | DENIED | BLOCKED_INTEGRITY | INCOMPLETE
~~~

The frozen result is ephemeral. It records the requested operation, exact before-values and pinned campaign revision, typed native field delta, current creator/operation authorization evidence, complete affected PLAYER and LIVE nomination basis, one resulting after-authority view, required collaboration reconciliation and authorized campaign paths. It cannot accept an arbitrary caller-supplied authorization boolean or preassembled unproven affected set.

| Operation | Permitted native delta | Required non-effects and admission |
|---|---|---|
| SET_CAMPAIGN_MODE | MANIFEST.mode; initialize players.join_policy to invite_only when enabling multiplayer without a chosen policy where the owner requires initialization | Only current creator authority. Do not change PLAYER identities, status, bindings, control, policy grants or accepted execution merely because mode changes. Derive actual authority impact under current mode/control/claims. |
| SET_JOIN_POLICY | MANIFEST.players.join_policy, invite_only or open_contributors | Only current creator authority. Existing active bindings remain active; creator-removed bindings do not gain a self-enrollment bypass. This field governs enrollment, not retroactive membership or PC control. |
| SET_MECHANICAL_OVERRIDE_GRANT | Exact target PLAYER.policy_authority.mechanical_override_policy, true or false | Only current creator authority may grant/revoke another PLAYER's existing narrow grant. Missing/null is false for a non-creator; no stored interpretive grant is introduced. Current activity and operation-specific authority still apply to later adoption. |

Use exact current owner values and typed deltas, preserving every unrelated MANIFEST/PLAYER field, including F35 collaboration_route_refs, other policy data, preferences and provenance. Do not serialize stale full records. No PLAYER creation, principal rebind or PC transfer is implicit in these operations; an explicitly requested such operation uses its F37 producer and all corresponding joins.

Grant/revoke is a HARD access-control persistence boundary. It is prospective: it cannot invalidate previously accepted policy revisions, Resolution generations, RNG results or established consequences. A prepared policy-adoption write must revalidate current grant/activity/creator authority and cannot self-grant permission in its own resulting tree. The policy sidecar remains adoption evidence, not grant authority.

## 3. Complete bounded impact derivation

Derive impact from exact current before-state plus the single intended after-authority view.

- A grant-only transition direct-loads its exact target PLAYER and that PLAYER's complete collaboration_route_refs. The F9 stable-principal companion is unchanged when stable binding is unchanged; validate it where used, rather than rewriting it for a policy/status change.
- A mode transition may affect multiple current bindings. For this explicit campaign management operation, enumerate the complete pinned F9 principal-routing companion's candidate PLAYER IDs, deduplicate, direct-route/load exact current PLAYERs and validate owner binding/status/control. Retained inactive bindings remain nominations, never ordinary authority. This is current companion traversal for the selected management scope, not a generic PLAYER-family/history scan or an ordinary per-turn synchronization rule.
- F9 completeness must cover every currently bound PLAYER whose applicable authority can change. Missing, partial, stale or mismatched nomination evidence blocks or enters the existing explicit derivative-repair boundary. A route holder not discoverable under the proven companion invariant is not silently omitted. No new MANIFEST player registry or global collaboration index is created.
- For each PLAYER with a material before/after agency-authorization change, inspect the exact current collaboration_route_refs and direct-load the nominated current obligation generations. Deduplicate by (obligation_id,generation) before reconciliation. A PLAYER with unchanged authority need not cause unrelated generation mutation.
- Derive the complete affected selected-LIVE set from current F30 routing plus current native claims/control and the F7 classifier. Unknown impact cannot choose NO_LIVE_ROLLOVER. A grant or join-policy change that provably leaves existing LIVE writers/claims/control unchanged must not become a blanket all-LIVE rollover merely because its name contains policy.
- Apply finite page/read/retry budgets with explicit complete/incomplete results. Partial traversal cannot publish the access change. No broad ref, historical runtime or all-obligation scan is an ordinary fallback.

For a mode transition, the management cost is bounded by P current principal-route candidates, C distinct nominated obligation generations, L affected selected LIVE sources and their required native dependencies/bytes. Grant-only work normally uses one target and its nominated obligations; a join-policy-only change with proved unchanged existing authority needs no all-PLAYER reconciliation. Exact provider action count, serial depth and latency require later supported-target evidence. No additional LLM generation, polling, background reconciler or global barrier is prescribed.

## 4. One after-authority view for collaboration

RD-12 extends GAME/TOOLS/collaboration.py with a bounded batch adapter around F38's existing native generation reconciliation:

~~~text
reconcile_collaboration_for_access_policy_transition(
    frozen_access_policy_transition,
    exact_current_affected_players,
    deduplicated_current_obligation_generations,
    current_dependency_opportunity_basis
) -> AccessPolicyCollaborationReconciliation | BLOCKED_INTEGRITY | INCOMPLETE
~~~

AccessPolicyCollaborationReconciliation is an ephemeral aggregate of the pinned campaign revision, exact after-authority basis, inspected PLAYER refs, unique obligation-generation transitions and all affected PLAYER route-ref deltas. It does not reuse F38's single-player_id result as if that field identified a whole campaign transition.

The batch uses one pinned campaign basis and the complete intended after-authority view for every affected PLAYER. It evaluates each current obligation generation once; repeated discovery through required contributors and held-input holders must not create competing successors or duplicate route deltas.

F38 remains controlling: unchanged opportunity/requirement -> UNCHANGED; lost opportunity -> OBSOLETE with no successor; same dependency lineage with materially changed requirement -> old generation OBSOLETE plus a successor from current authority; a semantically new dependency is not an invented successor. All required and held-input route holders are derived from the resulting owner state.

Do not rewrite the old generation's authority identity, copy accepted old input into a successor, synthesize consent/action/pass/readiness, replay mechanics or infer that a PC disappeared. Mode/policy change alone does not settle an accepted Command, Procedure or promised unresolved input; F58 operational membership survives unless its native owner independently proves an eligibility change. Temporal eligibility and accepted firing identity remain with their native owners.

## 5. LIVE prerequisites and one campaign acceptance edge

The final mutation reuses F37/F7/F30/F31/F36/F38/F58 and RD-06:

1. Revalidate current creator/operation authority, exact MANIFEST/PLAYER bases, complete affected routes, claims and collaboration opportunity.
2. When LIVE_TRANSITION_REQUIRED, close/freeze every affected selected LIVE source by its native exact-source CAS, prove the exact terminal revisions, and retain every accepted native semantic/identity. An already accepted close stays real after another source rejects or is indeterminate.
3. After terminal proofs, re-evaluate dependency/opportunity from the exact final source values and the single intended after-authority view; do not retain pre-close collaboration decisions over newly accepted native state. Freeze one campaign resulting tree containing the typed MANIFEST/PLAYER policy delta, every required obligation obsolete/successor and affected PLAYER route-ref delta, exact LIVE absorption/route release and required temporal/operational companions. Binding-preserving policy changes do not invent a principal-routing mutation. Preserve other already-required campaign companions.
4. Publish through RD-06's single-parent non-force current-base campaign boundary. Campaign authority must not change before all required terminal source proofs and reconciliations exist.
5. Derive any successor LIVE source from the newly accepted current campaign authority. Never reopen predecessors, rekey accepted identities, replay RNG or report distributed rollback.

No acknowledged tree may expose new mode/policy authority with stale required collaboration authority, split route-holder generations, missing transferred temporal/operational roots or stale writable LIVE authorization.

A stale campaign base requires fresh impact derivation and complete recomposition, including simultaneous affected PLAYERs. An indeterminate result is reconciled from the exact current native resulting state through RD-07/RD-06: already fully accepted, not accepted, or inconsistent/split state. A successful remote acceptance with failed local adoption remains accepted; no blind repeat. Persistent churn or incomplete evidence ends in the owner-bounded unavailable/blocked result. No new durable queue or transition record is introduced.

## 6. Derived planning and recipient boundary

RD-13's existing overlay1/overlay2 admission is the required consumer join, not a new campaign-wide horizon rewrite. Accepted mode disable makes retained multiplayer horizons INACTIVE_MODE; bytes may remain. Re-enable or changed PLAYER/control/eligibility does not select old bytes without current native/recipient/shared-basis validation. Shared ABSENT versus BOUND remains owner-defined; no forced shared dependency or private horizon transfer is added.

Join/rejoin still reacquires current PLAYER/control/routes/obligations before mutable input or recipient-safe catch-up. Neither access management nor a route reference grants another participant's accepted-input text, private planning, knowledge or disclosure. Preserve RD-12 JoinRejoinCatchUpTests and F50's current principal-route product cutover.

## 7. Exact task-owned proof

Each new class is introduced in its own RED-to-GREEN task after its local prerequisites. Later integration negatives are not pre-created as a failing earlier-task suite.

| Exact module/class | Primary channel | Mandatory joined evidence |
|---|---|---|
| DEV/TESTS/test_rd09_access_live.py::CampaignAccessPolicyTransitionTests | FOCUSED_BEHAVIOR | All three operation kinds and exact field scope; creator unresolved/non-creator denial; no self-grant-plus-adopt; null grant false; prospective revocation; fresh MANIFEST/PLAYER preservation including collaboration refs; stable principal route not needlessly rewritten; join-policy non-revocation/removal-bypass negatives; complete affected-set/incomplete-budget and F7 classification. |
| DEV/TESTS/test_rd12_collaboration.py::AccessPolicyCollaborationReconciliationTests | INTEGRATION_SCENARIO | Actual RD-09 producer + RD-12 adapter; multiple affected PLAYERs nominate one generation -> one reconciliation/successor under the common after-view; held-input holders included; obligation/PLAYER route closure; no late-input carry, agency synthesis or opportunistic wait for a new input. |
| DEV/TESTS/test_rd09_access_live.py::AccessPolicyPublicationIntegrationTests | INTEGRATION_SCENARIO | Actual policy producer/reconciliation + RD-06 publication + LIVE terminal/absorption + RD-07 recovery; mode withdrawal with multiple selected sources, partial/unknown close and campaign results; stale complete impact set; F36 temporal and F58 operational companions; unchanged accepted IDs/RNG; native acceptance remains truthful after local adoption failure. |
| DEV/TESTS/test_rd09_access_live.py::AccessPolicyConsumerIntegrationTests | INTEGRATION_SCENARIO | Actual accepted policy result + RD-13 admission and RD-12 join/frontier/catch-up: disable/re-enable, changed eligibility/control, no stale cached horizon or private-input transfer, no automatic reactivation of obsolete generations. |

Required commands, only during authorized implementation/proof execution:

~~~bash
python3 -m unittest DEV.TESTS.test_rd09_access_live.CampaignAccessPolicyTransitionTests -v
python3 -m unittest DEV.TESTS.test_rd12_collaboration.AccessPolicyCollaborationReconciliationTests -v
python3 -m unittest DEV.TESTS.test_rd09_access_live.AccessPolicyPublicationIntegrationTests -v
python3 -m unittest DEV.TESTS.test_rd09_access_live.AccessPolicyConsumerIntegrationTests -v
~~~

The publication integration must inject an omitted policy/PLAYER/collaboration/LIVE companion, missing required terminal source and stale affected-set basis; each must prevent false success. It must also prove safe join-policy/grant-only changes do not revoke existing memberships or roll unrelated LIVE, accepted prior policy/execution remains valid after revocation, and the separate consumer integration proves disabled/re-enabled planning never bypasses actual admission. Mocked success booleans or only the existing static HouseRulesPolicyAuthorityContractTests do not establish this joined behavior.

PG36 is the exact integration row. It extends the supporting routes for R080 items 3, 4, 11 and 12 and R083 theme 16; item12 keeps its original additive membership duty while the shared classifier's policy/non-revocation boundary receives additional integration coverage. Existing Wp16LiveAccessProofTests and Wp17CollaborationProofTests remain item-bound. PG35 and all earlier PG identities remain separate. Creator-unresolved denial is testable; no test/finding disposition here closes the unresolved creator architecture decision or authorizes production.

## 8. Checkpoints, files and version impact

| Prerequisites | Checkpoint | Relation |
|---|---|---|
| RD09_PLAYER_ACCESS_TRANSITION_LOCAL_READY + current F9/F30 nomination contracts | RD09_ACCESS_POLICY_TRANSITION_LOCAL_READY | Local producer/field/impact RED-to-GREEN. Uses exact contract fixtures; does not wait for full RD12/RD16. |
| RD12_PLAYER_AUTHORITY_RECONCILIATION_LOCAL_READY + RD09_ACCESS_POLICY_TRANSITION_LOCAL_READY | RD12_ACCESS_POLICY_RECONCILIATION_READY | Actual common-after-view batch adapter and joined generation proof. |
| RD09_ACCESS_POLICY_TRANSITION_LOCAL_READY + RD12_ACCESS_POLICY_RECONCILIATION_READY + existing RD06 campaign publication/recovery substrate + implicated F7/F30/F31/F36 LIVE/temporal joins + RD09_OPERATIONAL_ROOT_HANDOFF_READY | RD09_ACCESS_POLICY_PUBLICATION_JOIN_READY | JOIN_BEFORE_INTEGRATION for actual acceptance/partial-result/companion proof. No whole-RD barrier. |
| RD09_ACCESS_POLICY_PUBLICATION_JOIN_READY + existing RD13 published-generation admission and RD12 recipient-safe catch-up targets | RD09_ACCESS_POLICY_CONSUMER_JOIN_READY | JOIN_BEFORE_INTEGRATION for the separate actual-admission/catch-up consumer class; no premature later-task RED suite. |
| All four task-owned target/proof results above | ACCESS_POLICY_TRANSITION_PROOF_READY | PROOF_AFTER_TARGET, terminal PG36 sink. No reverse semantic prerequisite. |

Runtime input completeness/terminal source proofs are per-attempt preconditions; the table names implementation readiness, not a new runtime scheduler. Contract readiness does not depend on final generated runtime output. Integration proof follows its actual targets.

Exact future edits extend existing planned GAME/TOOLS/access_control.py, GAME/TOOLS/collaboration.py and their named RD-09/RD-12 test modules. RD-06, RD-07 and RD-13 remain consumed owners; add only the smallest adapter in those already-owned modules if required to expose the declared join. GAME/CORE/MULTIPLAYER.md's existing mode/join/access rules and ACCESS_CONTROL/House-Rules grant law are preserved in its already-mandatory RD-09/F46 final integration; no new independent final CORE writer is introduced. No new durable schema, route file, registry, allocator, Story artifact or MANIFEST creator field is added.

F35/RD16 remain final strict PLAYER integration owners; F48's final campaign_manifest v5 and the retained PLAYER local-version cutover remain unchanged. The three existing policy fields are already admitted. This planning publication has Version Impact NONE. A newly discovered structural/semantic incompatibility must return to its native owner; it is not permission to invent an extra version/generation or migration here.

Disposition: F59 is repaired at the planning level. Independent confirmation remains pending. Production implementation, release/migration execution and zero-open author closure are not authorized.
