# R2.7 WP-16 — Multiplayer / Access Control / Live State — Canonical Specification

Status: **CANONICAL WP-16 RESULT — STEPS 1-8 COMPLETE / MANDATORY FINAL SENIOR AUDIT PENDING**

Date: 2026-09-03

Canonical direction:

> **STABLE-PRINCIPAL AUTHORIZATION CHAIN / OWNER-TYPED IMMUTABLE LIVE CLAIMS / DOMAIN-SEPARATED CURRENTNESS / EXACT-SOURCE CAS / FORWARD NO-WINDOW AUTHORITY TRANSFER**

Canonicalization basis:

- repaired Step-1 Task Brief / open-world Source Manifest / whole-project critic;
- Senior repair `SR16-01` / `SR16-02`;
- Step-2 evidence extraction and Source-Manifest expansion;
- Step-3 Decision Brief;
- Step-4 collaborative review;
- Step-5 candidate specification;
- Step-6 whole-project adversarial review;
- Step-7 resolution gate.

This file is the single final WP-16 implementation-facing architecture owner. Earlier Step-5 candidate wording is design provenance and is superseded where it differs from this specification or the Step-7 finding resolutions.

---

# 1. Scope and central invariant

WP-16 realizes the physical/machine architecture for multiplayer application authorization, PLAYER/control resolution and selected LIVE writable authority while preserving Step-3 execution, Step-4 information ownership, Step-5.8 live semantics, R2.5 agency/collaboration and WP-11..WP-15 physical/currentness/recovery/chronology constraints.

It does not implement code/schemas/tests, start WP-17, select async collaboration semantics, introduce a server/leader/lease, create a global LIVE owner, define a distributed transaction, redefine chronology or begin implementation planning.

Central invariant:

> **A protected mutation is admissible only when one trustworthy current external principal resolves through current HDM application authority to the requested operation, and every mutated native owner/partition resolves to exactly one current writable source under current route/claim law.**

---

# 2. Supported principal and application authorization

## LAW WP16-1 — Supported-host principal evidence is explicit

The supported ChatGPT profile uses the connected GitHub Connector identity surface to resolve the current authenticated GitHub principal.

The principal evidence must expose a stable external GitHub user ID separately from mutable login/display metadata. A mutable login is never accepted as the stable `user_id` required by multiplayer PLAYER binding.

If trustworthy current stable principal identity cannot be resolved, a protected write fails closed. HDM does not guess from chat identity, cached login, commit author text, repository visibility or session state and does not try another Git transport.

## LAW WP16-2 — Stable external identity maps to one current PLAYER binding

For ordinary multiplayer authority:

```text
trusted current GitHub stable user ID
-> exactly one current active world.player / PLAYER binding by github_binding.user_id
-> stable campaign player_id
```

`PLAYER.player_id` is the campaign gameplay identity. `github_binding.login` is mutable convenience/audit metadata only.

A missing, inactive, ambiguous or multiply matching binding grants no ordinary gameplay authority.

Narrow creator-authorized onboarding, eligible open-contributor self-enrollment and permitted self-reactivation remain the only accepted pre-binding/reactivation exceptions under Access Control.

## LAW WP16-3 — Controlled-PC authority is separate

Current active PLAYER membership does not itself grant voluntary agency over a PC.

The operation must resolve the current controlled-PC relation. Joining/reactivation never silently seizes an existing PC, and a later explicit controller transfer wins over an older retained PLAYER association.

## LAW WP16-4 — Authorization is operation-specific

After principal, PLAYER and control resolution, apply the current owner-specific authorization for the requested mutation, including as applicable:

- creator-only campaign operations;
- active-member gameplay authority;
- controlled-PC voluntary agency;
- mechanical policy authority;
- target campaign/repository/ref routing;
- current native write authority/currentness.

Repository collaborator/Admin/write capability is infrastructure permission, not HDM gameplay authorization.

## LAW WP16-5 — Existing creator-login provenance remains a separate owner-specific rule

The accepted campaign-creator provenance rule remains governed by `ACCESS_CONTROL.md` / `BRANCH_MODEL.md`. WP-16 does not reinterpret historical creator login as the stable multiplayer GitHub `user_id`.

If a creator-only operation cannot establish its currently required creator provenance reliably, it fails closed under the owning rule. This limitation does not authorize a login-to-user-ID substitution or an upstream ownership rewrite inside WP-16.

---

# 3. Campaign selection and projection revalidation

## LAW WP16-6 — Card/session/index/cache data may nominate, never authorize

`CAMPAIGN_CARD`, menu state, session observations, indexes and local caches may help discover/select a candidate campaign or loaded object. They do not prove current creator identity, PLAYER membership, controlled-PC authority, current LIVE routing or write currentness.

## LAW WP16-7 — Post-selection revalidation is mandatory before mutable gameplay

After campaign selection/resume:

```text
candidate selection
-> pin current selected campaign ref
-> validate applicable creator provenance for owner-only operations
-> load current campaign mode/join policy from its owner
-> resolve current stable-ID PLAYER binding/membership
-> resolve current controlled-PC relation
-> resolve operation-specific authorization
-> resolve current campaign/LIVE write route
-> pin exact current native source basis
-> admit mutation
```

`MANIFEST` remains authoritative only for configuration fields it actually owns. A repeated card/session/cache projection of a MANIFEST or PLAYER fact does not replace the owner.

---

# 4. Three distinct currentness dimensions

## LAW WP16-8 — Campaign currentness is campaign-domain currentness

Campaign currentness is the exact selected campaign ref/current revision plus its owner-governed routing/configuration basis. It is not a universal currentness frontier for independently writable LIVE sources.

## LAW WP16-9 — LIVE currentness is selected-source currentness

A current LIVE route selects one exact LIVE epoch/source and its immutable claims. Authoritative LIVE mutation is fenced by that selected source's exact current revision under the native LIVE CAS contract.

Branch existence, branch name, scene membership, source-local integer revision or cached file bytes do not select authority.

## LAW WP16-10 — Local HOT currentness is local adoption only

Local HOT/SQLite state is current for an operation only while proven compatible with the selected native source basis. It cannot outrank campaign or LIVE authority by local freshness, generation or mtime.

A pre-CAS live result is prospective; a successful remote LIVE edge may be accepted even if local post-CAS adoption subsequently fails.

## LAW WP16-11 — No generic cross-domain freshness scalar

Campaign HEAD, LIVE HEAD, local HOT generation, session base SHA, checkpoint identity, Git timestamp or another scalar cannot be compared as “newer overall” to select truth.

---

# 5. LIVE claim grammar and authority geometry

## LAW WP16-12 — LIVE is a physical/currentness partition, not a semantic mega-owner

Physical co-location in `LIVE_STATE` does not transfer semantic ownership from Actor, Asset, Scene, Procedure, Resolution, Continuation, LoreFact, Knowledge, Disclosure, Event or another native owner.

A scene is not a universal LIVE owner. Physical scene membership and reference proximity do not imply write authority.

## LAW WP16-13 — Claim set is immutable for one epoch

A selected epoch E has immutable typed claim set `Q(E)`. Changing the claimed writable scope requires close/absorb/transfer and, if needed, a successor epoch; the old epoch is never mutated into a different authority set.

## LAW WP16-14 — Closed claim grammar

The baseline grammar is:

```text
LiveClaim :=
    EXACT_OWNER(native_family, native_identity)
  | EPOCH_LOCAL_CREATION(native_family)
  | OWNER_DEFINED_PARTITION(partition_type, partition_key)
```

No untyped path glob, scene-wide wildcard, arbitrary entity set, prose predicate or implicit graph closure is a claim.

## LAW WP16-15 — Exact-owner claims do not expand through references

`EXACT_OWNER` names exactly one pre-existing native semantic owner. It does not automatically include referenced owners, dependencies, children, same-scene participants, same-location records or every record touched by one action.

## LAW WP16-16 — Epoch-local creation is typed and closed

`EPOCH_LOCAL_CREATION(family)` permits lifecycle start only for a new native owner of that admitted family. It does not grant authority over existing records of that family.

The admitted creation-family set is a closed machine contract. Unknown/unadmitted families cannot become durable LIVE-born owners merely because a generic serializer can encode them.

## LAW WP16-17 — Owner-defined partitions require an existing owner contract

`OWNER_DEFINED_PARTITION` is legal only when the owning specification already defines deterministic bounded:

- partition identity;
- membership/containment;
- non-overlap;
- mutation authority;
- currentness/recovery;
- transfer/lifecycle behavior.

No generic sub-owner partition is activated in the WP-16 baseline merely for implementation convenience. Without such an owner contract, use exact-owner claims plus admitted epoch-local creation domains.

## LAW WP16-18 — Access/routing authority is campaign-only and cannot be LIVE-claimed

LIVE may not claim or become current authority for:

- `world.player` binding/membership/status/policy grants;
- controlled-PC assignment/transfer authority;
- campaign mode/join policy;
- creator provenance / creator-only authorization basis;
- campaign LIVE route/claim selection, absorption or successor selection;
- campaign/storage/engine write-routing authority;
- card/session/index/checkpoint/cache projections/helpers.

This prevents circular authorization where the source being authorized also owns the permission used to authorize itself.

## LAW WP16-19 — Selected claims do not overlap

Two selected ACTIVE/CLOSED-unabsorbed LIVE epochs cannot concurrently claim the same exact owner or overlapping owner-defined writable partition.

Overlap/ambiguity is an integrity/currentness conflict, not a last-writer-wins condition.

## LAW WP16-20 — WriteAuthorityLookup is bounded

For each target owner/partition X:

```text
WriteAuthorityLookup(X)
    -> CAMPAIGN
     | LIVE(epoch, source/ref, exact revision)
     | INTEGRITY_CONFLICT
```

The lookup uses current campaign routing plus bounded claim/owner metadata. Ordinary operation may not scan WORLD, all refs or all LIVE branches.

---

# 6. LIVE lifecycle and `CLOSED_UNABSORBED`

## LAW WP16-21 — ACTIVE is selected current truth plus ordinary writable authority

An ACTIVE selected LIVE source is current truth for its admitted claims and may accept ordinary writes only after current application authorization and exact-source validation.

## LAW WP16-22 — Close is terminal

`ACTIVE -> CLOSED` is monotonic for the epoch. CLOSED accepts no new ordinary gameplay mutation and never reopens.

## LAW WP16-23 — CLOSED_UNABSORBED is current truth with zero ordinary writers

If the campaign route still selects the CLOSED final source and absorption has not lawfully transferred its claims, that source remains current truth with zero ordinary writable authority.

Campaign base is not fallback current truth for the claimed owners. Shared mutation blocks/retries/repairs until lawful forward movement.

## LAW WP16-24 — Route-away requires the exact final CLOSED source

Campaign absorption/route movement must identify and validate the exact terminal source revision being absorbed/transferred. A status flag, scene pointer, cached blob or remembered head is insufficient.

## LAW WP16-25 — Absorption is forward publication, not merge/replay

Absorption publishes the accepted resulting native owners and routing state forward in the campaign domain. It does not replay every LIVE commit, rerun accepted mechanics or make Git branch merge semantics gameplay semantics.

## LAW WP16-26 — Cleanup is post-authority only

A predecessor LIVE ref/source may be removed only under Step-5.13 cleanup rules after current authority, required evidence and references have safely moved/discharged. Ref existence after absorption is non-authoritative residue; early deletion cannot be used to force authority movement.

---

# 7. Frozen LIVE mutation attempt and exact-source CAS

## LAW WP16-27 — LIVE mutation freezes one immutable ephemeral attempt

Before the first authority-changing LIVE remote mutation, deterministic core freezes an operation value equivalent to:

```text
FrozenLivePublicationAttempt {
    repository_identity
    campaign_ref + pinned relevant campaign authorization/routing basis
    stable_external_principal_id
    player_id + membership basis
    controlled_pc / operation authorization basis
    selected_live_epoch + immutable claim basis
    target_live_ref
    expected_exact_live_source_revision
    affected_native_owner identities/generations
    bounded semantic dependency/currentness footprint
    accepted execution/RNG/idempotency references as applicable
    normalized native LIVE delta
}
```

It is ephemeral operation state, not a journal, permission lease, lock, new authority owner or retry queue.

## LAW WP16-28 — Application authorization is revalidated independently of LIVE CAS

Before the first authority-changing LIVE mutation, every mutable campaign-domain authorization/routing dependency required by the operation must still satisfy its owning currentness rule.

If PLAYER status, control, policy authority, route selection or another relevant campaign-domain authorization fact moved, invalidate/rebuild or deny before LIVE mutation.

A successful exact-source CAS never retroactively legalizes stale application authorization.

## LAW WP16-29 — The selected native source revision is the authoritative LIVE fence

For the supported Git-backed realization, authoritative LIVE currentness is protected by the exact selected LIVE source/ref revision accepted by the authority-changing non-force transition.

Under the fixed current Git-data/ref realization this is the expected live-ref HEAD/source commit revision or a Connector operation with exactly equivalent expected-source CAS semantics.

A `LIVE_STATE` blob/content SHA may validate payload identity and support efficient refresh, but cannot by itself prove that the selected ref still names the expected current source revision.

The source-local integer `revision` is diagnostic/idempotency support only and does not establish authority.

## LAW WP16-30 — CAS outcomes preserve epistemic truth

Conceptual outcomes are at least:

```text
ACCEPTED
REJECTED / STALE
INDETERMINATE
```

On rejection, refresh only the affected selected source/dependencies and revalidate the operation. On ambiguity, resolve exact current source/ref and bounded lineage/closure evidence before deciding whether the edge accepted.

Never force push or infer success from a created object alone.

## LAW WP16-31 — Post-CAS local adoption cannot rollback accepted remote semantics

After confirmed compatible CAS, local HOT adopts the accepted source. Local adoption failure causes recovery/reload from current native authority; it does not undo, replay or reroll the accepted remote edge.

---

# 8. Source-native LIVE identity

## LAW WP16-32 — Durable identities first accepted in LIVE use `source_native_live`

Any independently addressable native record whose first durable/accepted identity is established inside LIVE and may escape the epoch uses a source-native identity basis:

```text
stable live epoch/source identity
+ native family/kind identity domain
+ accepted source-local creation coordinate
  or owner-defined collision-free equivalent
```

Exact printable encoding is implementation detail.

## LAW WP16-33 — Source-native identity needs no campaign allocator

The strategy must be collision-free across independent LIVE sources without campaign allocator access and must be fixed before/at the accepting native LIVE edge.

Campaign `runtime.id_allocator` is not a fallback for LIVE-born accepted identity.

## LAW WP16-34 — Accepted LIVE-born identity never rekeys on absorption

Retry, recovery, close, physical transfer and campaign absorption preserve the same semantic identity. Storage relocation does not create a replacement record identity.

ID ordering has no chronology, priority or winner semantics.

Derived child IDs continue to derive from their stable accepted parent where the native owner already defines that identity. Composite-key owners retain their semantic composite identity rather than gaining a second surrogate.

## LAW WP16-35 — Per-kind machine admission is mandatory

Every kind permitted to create an externally referenceable durable owner in LIVE must have an explicit machine identifier-policy disposition for `source_native_live` or an owner-defined equivalent.

Current campaign/sequential identifier-policy entries do not satisfy this requirement by themselves. A kind lacking a LIVE-born identity disposition cannot durably create such an owner in LIVE.

---

# 9. Revocation, deactivation, activation and controller changes

## LAW WP16-36 — Presence/absence never grants or revokes authority

No heartbeat, timeout, background polling, visible chat activity or user-presence guess is a correctness owner for membership/control.

## LAW WP16-37 — Revocation affecting ACTIVE LIVE closes the affected source first

When deactivation, controller removal/transfer, policy revocation or another authority withdrawal would invalidate a current ACTIVE LIVE writer for affected claims:

1. close/freeze affected source(s) through exact-source CAS;
2. establish exact final revision(s);
3. prevent stale writer publication;
4. preserve all already accepted native semantics before close;
5. publish the campaign-domain authority transition;
6. derive any successor only from the new current campaign authority basis.

## LAW WP16-38 — No-window campaign authority closure

When final LIVE absorption/route release and PLAYER membership/control/policy removal are same-domain facts whose separate publication could expose a state where old LIVE authority or old application authorization remains usable, publish them in one coherent campaign authority closure.

This closure may include:

- absorbed/surviving native owner values;
- predecessor final-source association;
- route/claim withdrawal;
- PLAYER deactivation/reactivation state as applicable;
- controlled-PC transfer/removal;
- policy/authorization changes;
- successor routing prerequisites;
- required derived routing/index companions.

## LAW WP16-39 — Additive authorization may avoid unrelated rollover

A PLAYER activation/reactivation or new participant need not close an unrelated ACTIVE LIVE source when immutable claims and existing writers' authorization semantics remain unchanged and no controlled-PC relation is transferred into/out of that source.

The newly authorized participant gains no mutable LIVE authority until current campaign membership/control/routing and applicable obligations are reacquired.

## LAW WP16-40 — Controller transfer that changes LIVE voluntary agency is a source transition

If controller transfer or equivalent authority substitution changes who may exercise voluntary PC authority against an ACTIVE LIVE claim, close/freeze affected source(s), perform the campaign authority transition, then open/adopt any successor from the new current basis.

The predecessor never reopens. An old controller's stale session fails current authorization even if it retains old source bytes/ref metadata.

## LAW WP16-41 — Rejoin/reactivation reacquires current obligations

Before mutable input after join/reactivation:

```text
current campaign/routing
-> current PLAYER binding
-> current controlled-PC relation
-> selected current LIVE source if any
-> current native/collaboration obligations
-> eligible role/recipient context
```

WP-17 owns durable asynchronous collaboration realization; WP-16 creates no timeout/fallback queue.

---

# 10. Multi-LIVE / cross-scope composition

## LAW WP16-42 — No distributed transaction or global LIVE owner

One semantic operation may depend on several current sources, but HDM does not create a transaction spanning LIVE refs or a global LIVE coordinator/rollback authority.

## LAW WP16-43 — Cross-scope prerequisites use bounded freeze/currentness

Where a cross-scope transition requires exclusive/fixed inputs:

```text
close/freeze affected LIVE A
close/freeze affected LIVE B
...
-> prove exact final required source revisions
-> perform the owning forward semantic/campaign transition
-> create optional successors from the new current basis
```

Partial freeze progress is technical state only, not partial fictional establishment.

## LAW WP16-44 — Accepted native edges never roll back because another source rejects

If one native durability/semantic edge accepts and another later rejects or remains indeterminate, the accepted edge remains real. Recompose current sources and block/retry/repair the dependent transition; do not compensate by replaying accepted mechanics or restoring old authority fictionally.

## LAW WP16-45 — Freeze/CAS/ref order is not chronology

Technical source order, Git commit order, CAS winner order, ref movement, integer revision, ID order and campaign absorption order do not establish fictional order.

When contested fictional order matters, use Step-5.9/WP-15 chronology and native rules/causal owners.

---

# 11. Execution, RNG and durability-edge granularity

## LAW WP16-46 — Close/source movement does not cancel accepted Step-3 execution

Accepted RuntimeCommand/Resolution/ExecutionSegment semantics, fixed RNG, idempotency identity, mandatory child/firing identity and already established native consequences survive transport conflict, close and recovery according to their owners.

## LAW WP16-47 — Retry never rerolls/replays an already accepted experiment

A stale/unaccepted prospective LIVE transition may be recomputed/rebased only at the owning safe boundary. Already accepted RNG/semantic edges retain identity and result; Git contention alone is never a reason to reroll or create replacement accepted identities.

## LAW WP16-48 — Native durability edge, not user message, defines atomic LIVE establishment

One high-level user action may produce multiple native semantic/durability edges. Physical packing may combine data only when those native semantics lawfully share one establishment boundary.

“One logical action = one LIVE write” is not architecture law.

---

# 12. Information ownership and player agency

## LAW WP16-49 — LIVE physical data creates no knowledge/disclosure mega-owner

Objective truth, `world.knowledge`, `runtime.disclosure`, accepted communication evidence and Story remain separate native owners.

Fields such as `live_facts`, `known_by_pc_ids`, `perceived_by_pc_ids` or observable-event summaries may be physical evidence/projection only unless the corresponding native owner itself is lawfully routed/claimed. Presence in LIVE does not create a second current authority.

## LAW WP16-50 — Disclosure follows its owning emission boundary

A shared mechanical/world consequence can establish before narration. Human disclosure advances only under the Step-5.12 emission owner. A LIVE publication and a disclosure publication may therefore be separate native edges.

## LAW WP16-51 — Human absence is not voluntary PC agency transfer

Absence/deactivation does not authorize another player/LLM to invent the absent player's voluntary speech, beliefs, emotions, intent or material PC choices and does not teleport/delete/kill the PC as membership maintenance.

The PC remains a world entity. Non-voluntary consequences may still occur only when existing mechanics/world causality require them without fabricating unresolved voluntary choice.

Another participant's report of an absent player's intended action is a hint, not player consent.

---

# 13. Recovery/currentness

## LAW WP16-52 — Recovery starts from campaign routing, then selected LIVE source

For a selected campaign:

```text
pin current campaign source
-> validate current routing/access basis
-> for each required claimed scope resolve selected LIVE epoch/source
-> pin exact current LIVE revision
-> hydrate current native owners
-> validate requested operation authorization/currentness
```

Campaign base never substitutes for selected ACTIVE or CLOSED_UNABSORBED truth.

## LAW WP16-53 — Missing/moving selected LIVE authority blocks or retries

A missing, incompatible, ambiguously selected or moving authoritative LIVE source yields bounded `RETRY`/`BLOCKED`/integrity handling under recovery rules. Session/cache/card/checkpoint/newest-looking branch is not fallback authority.

## LAW WP16-54 — Orphan/unselected LIVE source is non-authoritative

A prepared/live branch whose campaign route was never selected, or a leftover predecessor after confirmed absorption, gains no authority merely by existence. Cleanup remains owner-gated and conservative.

---

# 14. Performance and physical realization constraints

## LAW WP16-55 — Ordinary LIVE access/currentness stays bounded

Normal shared mutation uses bounded current route/claim metadata plus the selected source/ref and affected native owners. No ordinary operation requires:

- WORLD/campaign-wide scan;
- enumeration of all LIVE branches;
- full Git history;
- background polling/heartbeat;
- global lock/lease;
- distributed transaction;
- second LLM pass solely for synchronization.

## LAW WP16-56 — One-file packing remains an implementation option only

A physical `LIVE_STATE` file may package several native-owner payloads/evidence for efficiency only if it preserves:

- typed immutable claim grammar;
- one-authority-per-owner law;
- native semantic/durability edge granularity;
- source-native identity;
- information-owner separation;
- exact-source currentness;
- bounded validation/recovery.

Physical file packing cannot make scene membership the write-owner boundary.

---

# 15. Implementation/machine realization obligations

Later approved implementation planning must map this specification into concrete schemas/catalogs/runtime/test changes. At minimum it must realize and verify:

1. supported Connector authenticated principal -> stable external user ID separate from login;
2. stable user ID -> exactly one current active PLAYER binding;
3. controlled-PC and operation-specific authorization checks;
4. mandatory post-selection owner revalidation;
5. closed typed LIVE claim grammar (`EXACT_OWNER`, `EPOCH_LOCAL_CREATION`, admitted owner partition);
6. campaign/access/routing authority exclusion from LIVE claims;
7. bounded non-overlap/containment and `WriteAuthorityLookup`;
8. exact selected LIVE source/ref currentness fence distinct from blob/local integer revision;
9. immutable ephemeral FrozenLivePublicationAttempt and auth/currentness revalidation;
10. ACTIVE/CLOSED/CLOSED_UNABSORBED/absorbed/successor lifecycle;
11. no-window revocation/controller-transfer flow;
12. additive activation/reactivation no-rollover conditions;
13. `source_native_live` identity policy + per-kind LIVE-born admission;
14. no campaign allocator/rekey for accepted LIVE-born identity;
15. multi-LIVE freeze/forward-transition behavior without distributed rollback;
16. preservation of accepted execution/RNG/idempotency across retry/recovery;
17. chronology separation from Git/ref/CAS/freeze order;
18. information-owner/projection separation;
19. absence/deactivation agency negative cases;
20. recovery with ACTIVE, CLOSED_UNABSORBED, successor, missing/orphan and moved sources;
21. native durability-edge granularity rather than one-user-action/one-write;
22. bounded hot-path/read/write behavior under measured target workload.

---

# 16. Current machine/prose debt and downstream routing

Current stale surfaces are evidence of implementation work, not competing architecture:

- `GAME/CORE/LIVE_SCENE.md` — scene-centric ownership and one-action/one-write assumptions;
- `GAME/CORE/MULTIPLAYER.md` — stale close/compact/deactivate sequence;
- `GAME/SCHEMA/live_scene.schema.yaml` — no final typed claim grammar/source-native identity contract;
- `GAME/SCHEMA/scene.schema.yaml` — scene-wide live pointer semantics require narrowing to owner-typed routing;
- `DEV/CATALOG/identifier-policies.json` — campaign/sequential policies need explicit LIVE-born source-native dispositions;
- `DEV/TESTS/LIVE_SCENE_CASES.md` / `MULTIPLAYER_MEMBERSHIP_CASES.md` — stale scene/action/revocation expectations.

Downstream ownership:

- **WP-17:** durable async collaboration/offline contribution realization; remains not started;
- **WP-19/WP-20:** bootstrap/migration/schema/template materialization after architecture approval;
- **WP-22:** executable conformance and race/failure tests;
- **WP-24:** measured LIVE packing/size/fanout/latency/repartition decisions;
- **WP-26:** stale documentation/schema/test consistency reconciliation;
- **WP-27:** final implementation-planning readiness after remaining R2.7 domains.

WP-16 does not activate these domains.

---

# 17. Decision and risk record

**Decision:** preserve stable-principal application authorization as a chain separate from transport capability, preserve owner-typed immutable LIVE claims and domain-specific currentness, and realize authority movement through exact-source terminal close plus forward campaign transition with no stale authorization window.

**Risk:** a future implementation could recreate scene/global LIVE authority through convenient packing.
**Mitigation:** closed claim grammar, campaign/access authority exclusion, bounded exact-owner routing and owner-defined partition admission gate.

**Risk:** campaign-sequential/provisional IDs could escape from independent LIVE sources and later collide/rekey.
**Mitigation:** mandatory `source_native_live` per-kind policy for any durable LIVE-born owner.

**Risk:** exact LIVE CAS could succeed after PLAYER/control authorization became stale.
**Mitigation:** frozen LIVE attempt + independent campaign-domain authorization/currentness revalidation before authority-changing remote mutation.

**Risk:** membership/controller changes could reopen a stale writer window.
**Mitigation:** exact close first; same-domain no-window campaign authority closure; successor only from new current basis.

**Risk:** technical transition order could be mistaken for fictional chronology.
**Mitigation:** explicit non-equivalence; WP-15/native chronology remains owner.

---

# 18. Final WP-16 disposition

```text
STEP_6_BLOCKING:          2
STEP_6_SIGNIFICANT:       4
UNRESOLVED_BLOCKING:      0
UNRESOLVED_SIGNIFICANT:   0
HUMAN_DECISION_REQUIRED:  NO
UPSTREAM_REOPEN_REQUIRED: NO
WP17_STARTED:             NO
IMPLEMENTATION_PLANNING:  NO
NEXT_GATE:                MANDATORY SENIOR FINAL AUDIT
```
