# R2.7 WP-16 — Multiplayer / Access Control / Live State — Step-5 Candidate Specification

Status: **STEP 5 CANDIDATE — READY FOR MANDATORY WHOLE-PROJECT STEP-6 ADVERSARIAL REVIEW**

Date: 2026-09-03

Selected direction:

> **STABLE-PRINCIPAL AUTHORIZATION CHAIN / OWNER-TYPED IMMUTABLE LIVE CLAIMS / DOMAIN-SEPARATED CURRENTNESS / EXACT-SOURCE CAS / FORWARD NO-WINDOW AUTHORITY TRANSFER**

This candidate realizes closed upstream multiplayer/access/live semantics against the supported host and current machine surfaces. It does not start implementation or WP-17.

---

# 1. Scope and central invariant

For every multiplayer-protected mutation, HDM must be able to decide both:

```text
WHO is currently authorized for this operation?
WHERE is the current native writable authority for each target owner/partition?
```

without deriving either answer from mutable login, repository permission, scene membership, storage position, session/cache state, CAS success or transport order.

Central invariant:

> **A protected mutation is admissible only when one trustworthy current external principal resolves through current HDM application authority to the operation, and every mutated native owner/partition resolves to exactly one current writable source under current route/claim law.**

---

# 2. Supported-host principal chain

## LAW WP16-1 — supported principal evidence is explicit

For the supported ChatGPT profile, authenticated GitHub identity evidence comes from the connected GitHub Connector capability selected by R2.6.

A principal-sensitive operation requires trustworthy current evidence equivalent to:

```text
AuthenticatedExternalPrincipal {
    provider = github
    stable_user_id
    mutable_login?       # audit/display label only
    current capability/repository evidence as needed by the operation
}
```

This is conceptual; no new persistent record is mandated.

## LAW WP16-2 — stable external ID, not login, binds PLAYER

Multiplayer PLAYER binding resolves by stable external GitHub user ID.

```text
authenticated_principal.stable_user_id
    -> exactly one current PLAYER.github_binding.user_id
```

Mutable login SHALL NOT substitute for stable user ID, even when currently equal to a cached/historical label.

`PLAYER.player_id` remains the canonical campaign gameplay-principal identity after binding.

## LAW WP16-3 — missing trustworthy stable principal fails closed

If an operation requires authenticated application authority and the supported Connector cannot provide trustworthy current stable principal evidence, the operation returns typed capability/authorization unavailability and does not mutate.

No fallback to:

- mutable login;
- chat self-identification;
- cached session/card identity;
- repository collaborator/Admin permission;
- native Git/CLI/direct private HTTP/custom token transport.

## LAW WP16-4 — infrastructure permission never expands application authority

GitHub repository capability may be required to execute a transport operation, but it cannot independently create campaign membership, PC control, creator authority, policy authority or target write authority.

---

# 3. PLAYER membership and controlled-PC realization

## LAW WP16-5 — current PLAYER binding is an application-authority prerequisite

For ordinary multiplayer gameplay, stable external user ID resolves to exactly one current active PLAYER in the selected campaign.

No matching active PLAYER => no ordinary gameplay write authority, except narrowly admitted onboarding/reactivation operations under existing access-control law.

Multiple conflicting current bindings => integrity/authorization conflict; do not guess.

## LAW WP16-6 — controlled-PC relation is separately validated

When an operation exercises voluntary PC agency or mutates state under PC-control authority, the current PLAYER must currently control the applicable PC according to canonical control relation.

Joining, repository access, shared-scene participation, inactive-player return or absence of another controller do not assign control.

## LAW WP16-7 — authorization is operation-specific

After principal/member/control resolution, HDM applies the actual operation's current authorization contract, including as applicable:

- target repository/ref scope;
- campaign creator-only operation;
- PLAYER membership state;
- controlled-PC relation;
- House-Rule/mechanical policy grants;
- native owner permissions;
- lifecycle/currentness restrictions;
- join/reactivation narrow exceptions.

One successful operation does not create a reusable authorization lease for another operation.

---

# 4. Projection and cache non-authority

## LAW WP16-8 — menu/session/index/cache state is not authorization

The following may route or optimize current work only in their declared role:

- CAMPAIGN_CARD creator/participant login hints and join/menu classifications;
- MANIFEST player lists/mode/join-policy fields outside their exact configuration ownership;
- session `player_id`, `pc_id`, observed HEADs and timestamps;
- PLAYER_INDEX and other derived indexes;
- CURRENT projections;
- cached campaign/LIVE HEADs;
- cached parsed LIVE/HOT state.

They SHALL NOT independently grant membership, PC control, claim ownership, write authority or current truth.

A protected mutation revalidates the required mutable authorization dependencies at the currentness boundary prescribed by the owner/publication protocol.

## LAW WP16-9 — creator-login provenance stays separate from PLAYER stable identity

Where current accepted campaign-owner/storage/engine rules use Git provenance or owner login for a distinct owner-specific check, that login comparison remains in that narrow contract. It SHALL NOT be reinterpreted as `PLAYER.github_binding.user_id` or as a universal stable external identity rule.

If such owner-specific provenance cannot be reliably established, existing fail-closed behavior applies; WP-16 does not invent a substitute identity source.

---

# 5. Currentness domains

## LAW WP16-10 — campaign currentness is domain-native

Campaign-domain currentness is the exact authoritative campaign ref/revision selected under campaign publication law for campaign-owned scope.

## LAW WP16-11 — LIVE currentness is domain-native

For a native owner/partition currently claimed by selected LIVE epoch E, LIVE currentness is the exact current selected source revision of E.

Branch existence, branch naming, cached head, local revision integer or scene pointer remembered by the session cannot establish currentness without current valid routing.

## LAW WP16-12 — local HOT currentness is distinct

Process-local HOT/SQLite state is an adopted working realization over native owners. It may contain accepted unpublished campaign state or locally adopted LIVE state according to owner law, but it never becomes the remote LIVE/campaign publication authority merely by being locally newest.

## LAW WP16-13 — no generic cross-domain newer-than relation

Campaign revision, LIVE source revision and local HOT revision/adoption position are not generically comparable.

Only explicit owner relations such as `based_on`, `selected_by`, `absorbed_from`, `adopted_from` or equivalent may relate them for a concrete consumer.

---

# 6. Typed immutable LIVE claims

## LAW WP16-14 — LIVE is a physical/currentness partition, not semantic mega-owner

Physical co-location in one live source does not move semantic authority from native world/runtime owners into `world.scene`, `LIVE_STATE`, the live branch or a new LIVE record class.

Native ownership remains visible/machine-decidable for every mutable fact.

## LAW WP16-15 — claim identity is typed

A LIVE claim identifies exactly one:

```text
native owner reference
OR
native-owner-defined typed writable partition reference
```

only where deterministic membership, containment, non-overlap, mutation admission and recovery routing are defined.

## LAW WP16-16 — claim set is immutable for one epoch

The selected claim set Q(E) cannot expand/shrink while E remains the same epoch.

Changing claim ownership requires forward lifecycle movement through close/freeze, campaign transfer/absorption and optional successor epoch.

## LAW WP16-17 — selected claims cannot overlap

Current selected LIVE routes may not claim overlapping mutable owner/partition authority.

Overlap is integrity conflict, not last-writer-wins.

## LAW WP16-18 — no implicit claim graph closure

Physical presence, scene participation, participant/PC list membership, reference reachability, touched paths/entities, knowledge relation or shared file placement does not automatically claim another owner.

## LAW WP16-19 — bounded write-authority lookup

For every class admitted to LIVE mutation, deterministic bounded routing supports an operation equivalent to:

```text
WriteAuthorityLookup(native_owner_or_partition)
    -> CAMPAIGN(exact/current route basis)
     | LIVE(epoch, exact/current route basis)
     | INTEGRITY_CONFLICT
```

No ordinary gameplay all-live/world scan is authorized.

---

# 7. ACTIVE and CLOSED_UNABSORBED

## LAW WP16-20 — ACTIVE

When current routing selects ACTIVE E for claim X:

```text
current truth(X) = E
ordinary write(X) = allowed only through authorized exact-source LIVE transition
```

Campaign base for X is dependency/reference state, not concurrent writable truth.

## LAW WP16-21 — CLOSED_UNABSORBED

When current routing still selects CLOSED E for X:

```text
current truth(X) = E at exact final source
ordinary write(X) = NONE
campaign fallback = FORBIDDEN
```

Recovery/absorption/repair may read the closed source. Ordinary gameplay cannot reopen it.

## LAW WP16-22 — route-away requires exact final CLOSED source

Normal authority transfer/release from selected E requires proof of E's exact final CLOSED source under the Step-5.8 transfer contract.

An ACTIVE source is not routed away in healthy normal operation.

---

# 8. Exact-source LIVE CAS and publication

## LAW WP16-23 — exact source revision is the LIVE mutation fence

Each authoritative LIVE transition is conditioned on the exact current selected source revision accepted by the attempt.

A source-local integer `revision`, blob ordinal or timestamp may be diagnostic but cannot replace the exact source revision fence.

## LAW WP16-24 — pre-CAS LIVE state is prospective

A prepared LIVE delta, fixed prospective owner overlay or locally staged result is non-current until the authorized exact-source transition is accepted.

It must not be narrated as established shared fact when write-before-reveal owner law requires prior establishment.

## LAW WP16-25 — CAS success requires prior application authorization

A transition may attempt authoritative publication only after current enough evidence establishes:

- authenticated stable principal;
- PLAYER/control/policy authorization as applicable;
- current LIVE route/claim membership;
- exact expected source basis;
- native transition validity.

Technical ability to update the source or successful CAS is not a substitute for those checks.

## LAW WP16-26 — post-CAS local adoption cannot undo accepted state

Once exact-source LIVE publication is confirmed accepted, later local HOT/SQLite/session adoption failure cannot roll it back, replay mechanics or reroll. The runtime refreshes/adopts from current native source or enters bounded recovery/integrity handling.

## LAW WP16-27 — publication ambiguity is resolved from source currentness/lineage

Dispatch alone does not prove acceptance. `ACCEPTED | REJECTED | INDETERMINATE` transport outcomes are resolved using bounded exact source/current lineage evidence under existing publication law; never by guessing or replaying accepted mechanics.

---

# 9. Live-born identity

## LAW WP16-28 — externally referenced accepted LIVE identities are source-native and collision-safe

An accepted record created in an independently writable LIVE source that must survive durable external reference SHALL have stable identity allocatable without synchronous campaign-global sequential reservation.

The accepted Step-5.8 conceptual strategy remains epoch/source-qualified identity plus an accepted source-local creation coordinate/equivalent collision-free owner data.

Accepted identity survives absorption.

## LAW WP16-29 — provisional identity is explicitly owner-constrained

A rekeyable/provisional identity is legal only where the native owner contract proves it does not escape into durable external references requiring stable identity before promotion.

Generic live `provisional_id` is not a universal creation policy.

## LAW WP16-30 — identity order has no semantic precedence

LIVE local ordinals, IDs and allocation order do not establish fictional chronology, conflict winner or application authority.

---

# 10. Revocation / deactivation without stale writer window

## LAW WP16-31 — deactivation never depends on background presence detection

There is no TTL/heartbeat/online-presence correctness dependency. Revocation becomes effective through authoritative state transitions and is discovered at the next required currentness/publication boundary by stale sessions.

## LAW WP16-32 — active LIVE revocation closes source first

If removing/deactivating a PLAYER affects a currently selected LIVE source in which their authorized operations may mutate claimed state, affected LIVE source(s) are first exact-source closed/frozen.

A close that wins rejects later stale ordinary LIVE writes. An already accepted write that won before close remains accepted canon.

## LAW WP16-33 — same-domain absorption and authorization removal form one campaign authority closure

When final LIVE absorption/route release and PLAYER deactivation/membership removal are represented in the same campaign authority domain and splitting them could reopen an authorization/write window, one coherent campaign transition SHALL establish together as applicable:

```text
final absorbed/survivor native state
+ PLAYER status/authorization removal
+ controlled/authorization relation updates explicitly part of the operation
+ live route release/replacement
+ completeness-critical derivative claim/authorization routing updates
```

No acknowledged healthy campaign state may restore ordinary campaign mutation for the affected scope while still authorizing the removed PLAYER through stale prior membership.

## LAW WP16-34 — successor opens only from post-revocation current campaign state

If remaining authorized players still require LIVE concurrency, any successor epoch is opened/adopted only after the campaign transition establishing the new authorization/routing state is current.

The removed player is not included merely because an old session/participant list says they were present.

## LAW WP16-35 — stale session cannot publish through old authorization

A stale session may retain cached conversation/HOT state, but before a protected write succeeds it must pass the current authorization/currentness predicates of the selected native source. If PLAYER is now inactive or route/claim changed, publication is denied/reselected.

---

# 11. Multi-LIVE / cross-scope composition

## LAW WP16-36 — no distributed LIVE transaction

A semantic transition affecting several independently writable LIVE sources does not require a distributed transaction or global rollback.

## LAW WP16-37 — prerequisite freezes are technical state only

The runtime may sequentially exact-source close/freeze each required current LIVE source and durably observe a partial set of frozen sources if interrupted.

That partial freeze establishes no fraction of the intended fictional transfer/global consequence.

## LAW WP16-38 — cross-scope result establishes at owning forward boundary

After all required final source states are known and ownership prerequisites satisfied, the existing owner-defined campaign-domain transition establishes the cross-scope semantic result and route changes.

Failure resumes forward. Closed sources never reopen merely to emulate rollback.

---

# 12. Accepted execution / RNG / idempotency continuity

## LAW WP16-39 — close/source movement does not cancel accepted execution

Closing, freezing, absorption, revocation, CAS contention or local adoption loss does not revoke already accepted RuntimeCommand/Resolution/Procedure/Continuation/fixed RNG/receipt/temporal evidence.

Prospective unpublished work may lose a race and remain unaccepted.

## LAW WP16-40 — retry does not replay/reroll accepted semantics

A stale source rejection or authority movement causes current-source refresh/revalidation. Already accepted execution identity and generated accepted RNG remain fixed under Step-3 rules.

If an unaccepted prospective action's assumptions changed, its consequence may be recomputed from current state without converting the retry into a new accepted player action or arbitrary reroll.

---

# 13. Technical order versus fictional chronology

## LAW WP16-41 — Git/ref/CAS/freeze order is not fictional chronology

The order of:

- campaign commits;
- LIVE source revisions;
- CAS winners/rejections;
- source freezes;
- campaign absorption;
- local HOT adoption;
- IDs/index traversal;
- host/session/message events;

has only the semantic meaning granted by those technical/currentness owners.

It does not automatically establish fictional before/after, simultaneity or elapsed time.

## LAW WP16-42 — contested fiction uses its native rules/chronology owner

If two prospective actions are fictionally simultaneous/contested and storage acceptance order alone would change the intended fictional result, adjudicate through the appropriate mechanic/chronology/order owner. Do not let Git/CAS choose fiction merely because it serialized transport.

Accepted current-state consequences remain respected; this law is not permission to overwrite a prior already-established semantic transition.

---

# 14. Knowledge / disclosure / observable LIVE evidence

## LAW WP16-43 — LIVE storage does not become PC-knowledge authority

Objective live-owned world facts remain with native world owners. Durable fictional subject knowledge remains `world.knowledge` authority.

A LIVE observable event/per-PC visibility projection may be bounded evidence/routing used to establish or retrieve that knowledge but cannot survive as an independent competing durable knowledge truth.

## LAW WP16-44 — PLAYER exposure remains separate

Human exposure remains `runtime.disclosure` under the existing delivery/disclosure owner. Same scene, file readability, participant membership or PC knowledge does not by itself establish human PLAYER delivery.

## LAW WP16-45 — observable evidence follows native acceptance/idempotency

A compact observable event needed by another session must tie to a stable accepted semantic occurrence/owner transition. Source retry/absorption may not duplicate the fictional occurrence merely to refresh another session's projection.

---

# 15. Absence and voluntary PC agency

## LAW WP16-46 — absence is not voluntary action

Player disconnect, lack of current host activity, stale session, timeout, removal or deactivation does not authorize another player/DM/runtime component to choose that PC's voluntary action, belief, speech, consent or delegation.

## LAW WP16-47 — technical membership change does not move the PC fictionally

PLAYER membership/control maintenance does not teleport, kill, erase or otherwise create an in-world action for the PC.

Non-voluntary world consequences may still occur when existing rules/world owners establish them. Whether a procedure can continue without current input belongs to its native procedure/rules and, where applicable, downstream WP-17 collaboration semantics.

---

# 16. CAMPAIGN_CARD / MANIFEST / session / index roles

## LAW WP16-48 — CAMPAIGN_CARD remains menu projection

`creator_github_login`, participant login lists, join-policy display and derived lock/join classifications are presentation/access hints only. After campaign selection, authoritative provenance/PLAYER/policy/current route evidence is revalidated as required.

## LAW WP16-49 — MANIFEST remains declared configuration owner only

MANIFEST may own campaign mode/join-policy/configuration fields where current schema says so. It does not become creator identity, external principal binding, controlled-PC or LIVE-claim authority merely because it lists players/settings.

## LAW WP16-50 — session remains coordination/observation

Session records may retain selected PLAYER/PC/scene and observed source revisions for resume/diagnostics. They do not authorize writes, prove liveness or supersede current native routing.

## LAW WP16-51 — indexes/caches are bounded derivatives

PLAYER indexes, scene routing caches, claim lookup projections and current working caches may be correctness-critical for bounded discovery only under their declared completeness/currentness contract. Their payload never replaces native semantic authority.

---

# 17. Integrity / recovery / cleanup

## LAW WP16-52 — missing selected LIVE source is not campaign fallback

If current route points to a LIVE source that cannot be resolved/validated, affected scope becomes bounded integrity/recovery suspect. Do not silently read/mutate campaign base as current truth.

## LAW WP16-53 — recovery resolves current route before mutable owner hydration

Cold/context-loss recovery re-establishes current campaign authority/routing, then exact selected LIVE source(s), then native owners/execution dependencies. Session/card/cache state may accelerate discovery but cannot decide authority.

## LAW WP16-54 — live ref deletion is post-authority cleanup

A LIVE ref/source may retire only after native routing/absorption/retention contracts prove it non-authoritative and all protected consumers have sufficient survivors. Ref deletion never moves authority.

---

# 18. Performance and boundedness

## LAW WP16-55 — ordinary authorization/currentness is bounded

Normal multiplayer operation must not require:

- scanning all PLAYER records when a bounded stable-ID index/route exists;
- scanning all LIVE branches;
- scanning all scene/world entities to infer claims;
- broad Git history retrieval;
- global claim graph traversal;
- heartbeat/lease polling;
- distributed transaction coordination.

## LAW WP16-56 — LIVE mutation granularity is native durability edge, not user message

One user Interaction may produce zero, one or several authoritative LIVE transitions when Step-3/native owner semantics define separate durability/choice/reaction edges.

Do not force all internal accepted execution into one write merely to satisfy a “one user action = one LIVE write” optimization.

Ordinary performance should still batch data belonging to one native transition into the smallest practical complete LIVE source transition.

---

# 19. Downstream boundaries

WP-16 deliberately does not:

- implement schemas/runtime/tests;
- define async collaboration obligation lifecycle/order — WP-17;
- define Dramaturg behavior — WP-18;
- execute bootstrap/migration changes — WP-19/WP-20;
- implement conformance tests — WP-22;
- select performance optimizations without measurement — WP-24;
- perform broad stale CORE/schema cleanup — WP-26;
- start implementation planning.

Later domains must consume this result without treating those downstream obligations as current activation.

---

# 20. Machine-realization obligations

Later implementation planning must include, at minimum:

1. supported Connector adapter/current-principal result exposing stable GitHub user ID distinct from login;
2. stable-ID -> active PLAYER lookup and ambiguity/fail-closed handling;
3. current controlled-PC and operation-specific authorization checks;
4. explicit typed immutable claim representation/routing or equivalent machine contract;
5. bounded claim containment/non-overlap validation;
6. current `WriteAuthorityLookup` for each admitted LIVE-mutable native owner/partition;
7. exact-source LIVE currentness/fencing independent of local `revision`;
8. source-native collision-safe identities for live-born externally referenced accepted records;
9. owner-constrained provisional identity rules;
10. revocation closure combining absorption/route release with deactivation where split state could reopen authority;
11. CLOSED_UNABSORBED recovery and zero-writer enforcement;
12. multi-LIVE forward freeze/transfer recovery;
13. current knowledge/disclosure normalization/projection rules;
14. per-native-durability-edge LIVE publication;
15. stale-card/session/index/cache rejection/revalidation cases;
16. accepted execution/RNG/idempotency source-movement tests;
17. no-technical-order-as-fiction tests;
18. absence/no-voluntary-agency tests;
19. boundedness/performance instrumentation.

No exact schema/API names beyond current accepted owners are selected here unless required by a current owner contract.

---

# 21. Candidate status

```text
STEP_5_CANDIDATE_COMPLETE: YES
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
STEP_6_READY: YES
```

This candidate has not yet passed the mandatory independent whole-project Step-6 adversarial review and is not canonical until Steps 6–8 complete.