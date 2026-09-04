# R2.7 WP-18 — Story / Continuity / Dramaturg Planning — Canonical Specification

Status: **CANONICAL WP-18 RESULT — STEPS 1-8 COMPLETE / MANDATORY FINAL SENIOR AUDIT PENDING**

Date: 2026-09-04

Canonical direction:

> **LAYER-LOCAL STORY PROJECTIONS / DERIVED CONTINUITY / EPHEMERAL SINGLE-PLAYER PREP / SCOPED MULTIPLAYER DRAMATURG HORIZONS / NATIVE-OWNER-FIRST INVALIDATION**

Canonicalization basis:

- recovered WP-18 Step-1 Architecture Task Brief / open-world Source Manifest / whole-project Task-Brief critic;
- Senior Step-1 recovery `SR18-01..SR18-04` and explicit Senior GO for Steps 2-8;
- Step-2 research / architecture draft and open-world Source-Manifest expansion;
- Step-3 Decision Brief;
- Step-4 collaborative architecture review;
- Step-5 candidate specification;
- Step-6 independent whole-project dependency reconstruction and adversarial review (`F18-01..F18-08`);
- Step-7 finding-resolution / propagation gate;
- Step-8 canonicalization self-review.

This file is the single final implementation-facing WP-18 architecture owner, subject to mandatory final Senior audit. Earlier research, Decision Brief, review and candidate artifacts remain design provenance. Where they differ from Step-7 repairs incorporated here, this canonical specification governs.

This specification does not implement runtime/schema/template/catalog/test changes, does not start WP-19 and does not authorize implementation planning.

---

# 1. Responsibility and authority split

## LAW WP18-1 — Story is durable retrospective projection, not canon

Story is a durable, source-bound, noncanonical retrospective projection family.

Story owns only:

- layer-local presentation/history units;
- layer-local Story ID allocation;
- compatible source-domain coverage;
- required layer-local projection/index/editorial metadata.

Story does **not** own:

- objective/current truth;
- Actor cognition or intentional state;
- fictional knowledge;
- human disclosure;
- gameplay execution;
- accepted mechanics/RNG;
- fictional chronology;
- recovery/currentness of native state;
- prospective Dramaturg planning.

## LAW WP18-2 — Continuity has no generic semantic owner

Continuity is a bounded retrieval/projection concern over current native owners and admitted history/projections. Story may orient retrieval, but material reliance escalates to the applicable current/exact owner.

No generic continuity record, campaign-wide memory graph or second continuity authority is admitted.

## LAW WP18-3 — Source Actor owns current intentional continuity

R2.2 source Actor remains owner of current sparse non-epistemic intentional continuity, including applicable goals, current objective, next intention, material commitments and reconsideration cues.

Story and Dramaturg planning may reference or project that state but cannot duplicate or override its current authority.

## LAW WP18-4 — Dramaturg planning is prospective noncanonical preparation

Dramaturg planning owns only provisional planning coherence for its admitted scope.

It does not own future fact, accepted fiction, Actor intent, player/PC agency, current world state, chronology, execution, knowledge/disclosure, recovery canon or campaign-wide currentness.

---

# 2. Fundamental planning/projection laws

## LAW WP18-5 — PREPARATION HAS NO ENTITLEMENT TO OCCUR

No prepared scene, event, reveal, Actor reaction, convergence, clue location, threat beat or outcome becomes mandatory merely because Dramaturg preparation retained it.

## LAW WP18-6 — CANON INVALIDATES PREPARATION

Current accepted owners outrank preparation. An accepted player decision, source-Actor change, mechanics result, world/process transition, knowledge/disclosure change, LIVE/current-state movement or other native owner update invalidates incompatible preparation.

Invalidation yields omission, discard, selective rebase or replacement preparation. The engine must never repair canon to restore a plan.

## LAW WP18-7 — Persistence never promotes authority

Story/planning does not become canonical/current merely because it is durable, newer, shared, cached, indexed, repeated, copied, committed later or physically visible in the active ChatGPT context.

## LAW WP18-8 — Technical order is not fictional chronology

Story sequence/ID, planning generation, file order, Git/ref movement, CAS order, publication order and message order do not by themselves establish fictional time or causality.

WP-15/native chronology owners remain authoritative where relative fictional order matters.

## LAW WP18-9 — Native recovery wins

Recovery reconstructs current/accepted state from native current/durable owners. Story/planning may assist orientation but never reconstruct accepted fiction, Actor state, PC intent, mechanics or RNG in place of missing native evidence.

## LAW WP18-10 — Physical context visibility does not create role eligibility

Story or Dramaturg material physically present in one ChatGPT context is not automatically eligible for Narrator, Actor, Chronicler, Dramaturg or player-facing use. R2.3/R2.4/WP-08/WP-09 role, subject, purpose and recipient eligibility still govern.

---

# 3. Story physical and lifecycle contract

## 3.1 Layer-local topology

Use the accepted exceptional Story topology:

```text
<story_root>/<layer>/PROJECTION_STATE.yaml
<story_root>/<layer>/<floor(sequence/1000)>/<story_id>.yaml
```

`<story_root>` is campaign-root-relative static routing metadata under accepted storage topology. It cannot own coverage, currentness, generation or chronology.

Accepted baseline Story layers remain:

```text
TRANSCRIPT
EVENTS
MECHANICS
NARRATIVE
```

No global Story record, global Story currentness owner, universal Story frontier or campaign-wide mandatory Story index is admitted.

## 3.2 Layer projection state

Each layer projection-state owner conceptually carries:

```text
layer
story_id_allocator_high_water
coverage_by_source_domain[]
required_layer_local_index/editorial_metadata
```

Coverage compatibility is source-domain-typed and semantic-contract-aware. Story currentness is layer/source-domain-relative, never global.

## 3.3 Story unit contract

A Story unit contains only layer-specific retrospective presentation/history payload plus the source/projection basis required by that layer contract.

It may reference native owner/evidence identities for traceability and later escalation. Cross-layer references are presentation/retrieval aids only; they create neither cross-layer authority nor distributed atomicity.

## 3.4 Candidate disposition and coverage

Every enumerated candidate requiring disposition is classified under its source contract as:

```text
MUST_MATERIALIZE
MAY_OMIT
```

Coverage advances only after a legal terminal disposition and successful required publication.

`MAY_OMIT` creates no durable skip record unless a later accepted source contract proves one necessary.

## 3.5 Chronicler service state

There is no durable Chronicler queue, lease, heartbeat, worker-state or backlog record.

Backlog is derived from compatible source enumeration and layer coverage.

Turn-local service decision remains:

```text
NO_BACKLOG
SERVICE(window)
DEFER(reason)
```

Chronicler-generated drafts do not own Story IDs, coverage, publication or current truth.

## 3.6 Story publication/concurrency

Story uses validated ordinary non-force campaign publication consistent with WP-13.

- Story cannot block accepted gameplay publication;
- contention yields to current gameplay/native owners;
- no cross-layer distributed transaction is required;
- relevant source basis is revalidated under its source contract;
- same-ref optimistic/CAS publication serializes only the affected Story owner;
- successful Story publication does not establish fictional chronology.

## 3.7 Story retrieval / disclosure / same-envelope containment

Story retrieval remains bounded through R2.3/WP-09 and is admitted to a logical role only after current role/subject/purpose eligibility.

Story presence does not grant fictional knowledge or human disclosure.

Newly generated Story is not eligible as same-envelope gameplay/Narrator evidence merely because the host still physically exposes it; future use requires ordinary current role binding and eligibility.

---

# 4. Continuity contract

Baseline result:

```text
CONTINUITY: DERIVED ONLY
GENERIC_CONTINUITY_RECORD: NO
GLOBAL_MEMORY_GRAPH: NO
```

Conceptual retrieval route:

```text
current decision dependency
-> compact current routes / Story-history orientation where useful
-> bounded relevant source candidates
-> currentness + eligibility verification
-> exact/current native owner load when material
```

Story omission, Story lag or index omission is never general proof of absence.

---

# 5. Single-player Dramaturg contract

## LAW WP18-11 — Single-player planning is ephemeral only at baseline

```text
SINGLEPLAYER_DRAMATURG: EPHEMERAL ONLY
DURABLE_SINGLEPLAYER_PLANNING_OWNER: NO
```

Single-player Dramaturg uses current bounded context and typed `PreparationDraft` handoff. If lost or stale, it is recomputed from current owners.

A durable single-player owner may be proposed only if later accepted evidence proves an independently durable consumer whose correctness/quality cannot be met by bounded recomputation/current context.

Convenience, previously spent prompt cost or desire to retain an unused scene is insufficient.

---

# 6. Multiplayer retained Dramaturg owners

## LAW WP18-12 — Exactly two retained planning families are admitted

When multiplayer is active, exactly two bounded retained-horizon families are admitted:

```text
shared multiplayer horizon
player-local horizon keyed by stable PLAYER identity
```

They remain noncanonical preparation/projection owners outside `world.*` and `runtime.*` gameplay authority.

## 6.1 Fixed physical routes

WP-18 baseline routes are fixed campaign-root-relative paths:

```text
DRAMATURG/SHARED.yaml
DRAMATURG/PLAYERS/<player_id>.yaml
```

No planning registry, planning index, global plot graph, scheduler, campaign-wide planning list, horizon frontier or MANIFEST/root selector is required by WP-18 baseline architecture.

A future configurable selector, if ever justified by implementation-scaffold/migration constraints, is static routing only and cannot own planning currentness.

## 6.2 Stable local route identity

Player-local planning is keyed by stable campaign `player_id`, never GitHub login, display name, chat ID or PC ID.

Current eligibility is separate from stable route identity. PLAYER deactivation makes that retained local horizon unusable while inactive.

Control transfer never transfers another PLAYER's private planning to a successor controller.

## 6.3 Retained horizon conceptual shape

A retained horizon minimally supports conceptually:

```text
scope_identity
generation
planning_contract_identity_or_version?  # only where needed
source_basis[]
assumptions[]
entries[]
invalidation_or_revalidation_hints?
shared_basis                            # player-local horizon only
```

Exact schema field names remain downstream implementation work.

For a player-local horizon:

```text
shared_basis.kind = ABSENT | BOUND
```

- `ABSENT` means the local horizon did not consume retained shared planning.
- `BOUND` means it consumed a retained shared generation.

If `BOUND`, the local horizon MUST retain:

```text
exact shared_generation
bounded shared-basis identity sufficient to resolve that exact retained shared generation
```

A generic optional `shared_generation_hint` is insufficient.

Shared dependency is planning-local coordination only; it creates neither fictional chronology nor campaign-global freshness.

## 6.4 Planning entries

Entries are embedded typed values, not independently addressable campaign records.

Accepted classes remain:

```text
SOURCE_ANCHORED_CONSTRAINT
PROVISIONAL_DRAMATURGIC_DIRECTION
```

An implementation-local deterministic entry key may support comparison/update inside one horizon but creates no independent identity, backlink, GC ownership or global route.

## 6.5 Native-owner-typed source basis

Every declared material planning source dependency is typed by its native owner:

```text
owner_domain
owner_type
bounded_identity_or_partition
expected_owner_currentness_evidence?   # only where that native owner defines it
```

No universal source revision scalar/vector exists.

Currentness/revalidation delegates to the referenced native owner/domain.

`SOURCE_ANCHORED_CONSTRAINT` MUST carry enough declared native source basis to revalidate its claim.

`PROVISIONAL_DRAMATURGIC_DIRECTION` carries only assumptions/anchors actually consumed. Unrelated undeclared sources do not become dependencies.

A copied mutable native fact never becomes authority merely because the planning horizon retained it.

---

# 7. Planning currentness, authorization and publication

## LAW WP18-13 — Planning currentness is owner-local and published-generation based

The following remain distinct domains:

```text
planning generation
campaign/current native owner basis
LIVE epoch/current source
HOT local current state
PLAYER/control authorization
Actor source state
fictional chronology
Story coverage
```

No scalar/frontier unifies them.

Newly generated or edited planning remains an **EPHEMERAL candidate** until successful publication of the retained-horizon record.

Only a successfully published generation is eligible to serve as retained cross-context coordination basis.

Publication failure, defer or conflict does not select the unpublished candidate.

If still compatible, the previously published generation remains the retained basis; otherwise retained planning is absent, stale or incompatible.

Planning-publication failure never changes native gameplay/canon and creates no generic gameplay HARD durability edge or second campaign frontier.

## 7.1 Shared-horizon mutation preconditions

Before accepting a material shared-horizon mutation, runtime establishes at least:

1. current campaign identity and active multiplayer mode;
2. current authenticated principal -> active PLAYER binding where applicable;
3. current Dramaturg/operation eligibility for the shared scope;
4. exact current published shared planning generation/base;
5. compatibility of material declared native source basis;
6. absence of a native-owner contradiction that already invalidates the proposal.

## 7.2 Player-local load/use/write eligibility

Before material load/use/write of a player-local retained horizon:

- the stable PLAYER route identity is resolved;
- current active PLAYER membership is required;
- current Dramaturg role/recipient eligibility is required;
- where an entry materially depends on a controlled PC/entity, current control/subject compatibility is required through WP-16 owners;
- any `BOUND` shared basis is revalidated against the exact referenced published shared generation and current source compatibility.

Planning never owns membership, authentication, role eligibility or control.

## 7.3 Publication and CAS

Retained planning is campaign-owned noncanonical data and publishes through the ordinary campaign-tree optimistic/non-force path.

Planning publication:

- cannot turn planning into canon;
- cannot create chronology from commit/CAS order;
- cannot require a campaign+LIVE distributed transaction;
- cannot override a newer native owner because the planning write won transport CAS.

## 7.4 Conflict / rebase

On current-base movement or publication conflict:

```text
read current affected horizon + declared native dependencies
-> verify current authorization / eligibility
-> verify exact published planning base
-> revalidate native source basis and any bound shared basis
-> classify compatibility
-> keep compatible entries
-> rebase/rewrite only where semantically safe
-> discard incompatible provisional content
-> publish successor generation if still useful
```

Blind text merge and last-writer-wins are forbidden.

A conflict never authorizes restoration of older planned fiction.

---

# 8. Planning lifecycle and invalidation

## 8.1 Derived usability states

Planning usability is derived, not owned by a self-sufficient stored validity flag:

```text
ABSENT
CURRENT_COMPATIBLE
STALE_OR_INCOMPATIBLE
INACTIVE_MODE
CORRUPT_OR_UNUSABLE
```

Stored metadata may assist validation, but `active=true` or `valid=true` cannot outrank current mode, membership/control, role eligibility, shared dependency or native source evidence.

## 8.2 Successor generation

A successfully published material retained-horizon update produces a successor generation for that same bounded horizon.

Generation is monotonic owner-local metadata only. It is not global time, Story coverage, fictional chronology or gameplay order.

## 8.3 Selective invalidation

When bounded current-source movement invalidates only part of a horizon, compatible entries may survive only after explicit revalidation. Incompatible entries are omitted, rebased where safe, discarded or replaced.

The engine must not regenerate a campaign-wide plot merely because one source moved, nor preserve incompatible material merely to save prior preparation work.

## 8.4 Multiplayer disable / re-enable

When current campaign mode is not multiplayer, **both retained multiplayer planning families are semantically inactive**:

```text
DRAMATURG/SHARED.yaml
DRAMATURG/PLAYERS/<player_id>.yaml
```

Physical bytes may remain. Single-player operation does not adopt those bytes as a durable single-player planning owner.

On multiplayer re-enable, bounded retained horizons may be discovered and independently revalidated against:

- current multiplayer mode;
- current PLAYER membership;
- current role/recipient eligibility;
- current control/subject compatibility where relevant;
- current native source bases;
- any exact bound shared generation for player-local horizons.

Only compatible material may be reused. Incompatible material is discarded/rebuilt.

---

# 9. Privacy, disclosure and agency boundaries

## LAW WP18-14 — Planning presence grants no disclosure

Campaign membership or physical repository/context visibility does not grant semantic access to another PLAYER's local planning.

Local planning enters shared planning or another logical role only through an independently eligible/authorized projection or typed handoff.

## LAW WP18-15 — Narrator cannot consume raw planning by physical visibility

Narrator cannot consume raw Dramaturg horizon content merely because the same physical ChatGPT context contains it. Current WP-08/R2.4 role binding and eligible typed handoff remain required.

## LAW WP18-16 — Planning cannot invent PC agency

No planning entry may establish a voluntary PC action, speech, belief, emotion, allegiance, goal, consent or interpretation.

Convergence/pressure preparation may describe world opportunities/constraints only.

## LAW WP18-17 — Planning cannot replace Actor intent

Planning may record expected or conditional reactions based on current Actor state, but the real current NPC/Actor goals/objectives/intentions/commitments/reconsideration remain source-Actor state under R2.2.

---

# 10. Recovery and failure

## 10.1 Story loss/staleness/corruption

If Story is absent, stale or corrupt:

- native gameplay state remains recoverable from native owners;
- Story may be regenerated/caught up from compatible source contracts where source continuity permits;
- gameplay rollback is never authorized merely to restore Story.

## 10.2 Planning loss/staleness/corruption

If retained planning is absent, stale, inactive or corrupt:

```text
establish current campaign/mode/PLAYER/eligibility/native sources
-> establish exact published retained basis if any
-> discard unusable planning
-> reprepare bounded horizon if useful
```

No accepted action, Actor decision, mechanics result, RNG result or fictional fact is reconstructed from planning.

## 10.3 Publication/adoption failure

If noncanonical Story/planning publication is accepted remotely but local adoption/cache update fails, remote publication evidence controls that projection/planning owner's durable result.

Recovery does not replay gameplay and does not treat local cache as stronger.

If retained planning publication itself did not succeed, the unpublished candidate is not a durable/current retained generation.

---

# 11. Cleanup / retention

Story source retention/compaction follows accepted Step-5.10/5.11/5.13 obligations.

Planning references are not default GC retention blockers for native sources.

Old/inactive planning bytes may be cleaned under downstream scaffold/cleanup rules when they are not needed for current bounded retained-horizon operation. Physical residue does not remain semantically active.

No planning tombstone/history registry is required for correctness.

---

# 12. Bounded discovery and resource behavior

Ordinary runtime must preserve:

- no global campaign Story/planning scan;
- Story routing through known layer projection-state and bounded source-domain windows;
- direct player-local route from known stable PLAYER identity;
- direct shared route from active multiplayer mode;
- bounded native-owner source revalidation;
- no background planning invalidation scan;
- no planning graph traversal;
- no preload of all Story/planning into every logical role/context.

If measured scale later exceeds accepted resource budgets, WP-24 may trigger reviewed partitioning/index work. Scale is not assumed today.

---

# 13. Machine-realization obligations after approval

Later explicitly authorized implementation must align at least:

1. Story unit/projection-state schemas with accepted Step-5.10/WP-11 topology;
2. retained multiplayer Dramaturg horizon schema/value contract;
3. fixed campaign routes `DRAMATURG/SHARED.yaml` and `DRAMATURG/PLAYERS/<player_id>.yaml`;
4. stable PLAYER local route plus current membership/control/role eligibility validation;
5. local-horizon `shared_basis = ABSENT | BOUND`, with exact shared generation/bounded identity when `BOUND`;
6. native-owner-typed `source_basis[]` with no universal revision vector;
7. published-generation currentness and failed-publication semantics;
8. exact-base CAS/rebase/no-LWW behavior;
9. multiplayer disable/re-enable invalidation and revalidation;
10. catalog/admission-ledger provenance so `planning_entry_classes` traces current planning semantics through R2.5 and this final WP-18 owner, rather than implying Story/continuity ownership;
11. current CORE/instruction mapping without a parallel role-instruction subsystem;
12. executable regression/contract coverage for the acceptance cases below;
13. R2.6 post-implementation host-containment/evaluation obligations.

Current `planning_entry_classes` vocabulary remains semantically unchanged. WP-18 adds no new catalog semantic identifier solely for architectural convenience.

These are downstream realization obligations, not implementation authorization.

---

# 14. Required acceptance / adversarial cases

A conforming implementation must preserve at least these outcomes:

1. Delete all Story while native canon remains healthy -> gameplay/recovery remains valid.
2. Story contradicts current Actor/world owner -> native owner wins.
3. Story layer A caught up and layer B behind -> no global Story currentness inference.
4. Chronicler deferred repeatedly -> no durable scheduler/queue appears.
5. `PreparationDraft` serialized incidentally -> still not a durable owner.
6. Single-player context lost -> reprepare; no durable single-player plan required.
7. Shared planning predicts NPC betrayal; Actor state changes incompatibly -> plan invalidates/rebases.
8. Shared planning predicts PC consent -> illegal PC-agency assertion.
9. Shared-horizon CAS succeeds after native source moved incompatibly -> transport success cannot make stale planning semantically current.
10. An edited candidate fails publication -> it does not become the retained generation.
11. Player-local horizon consumed shared generation G and shared advances to G+1 -> local horizon must revalidate its mandatory `BOUND` basis before material use.
12. PLAYER becomes inactive -> its local retained horizon is unusable while inactive.
13. Control transfers -> prior controller's private local planning does not transfer.
14. Multiplayer disabled -> both shared and player-local retained families are semantically inactive.
15. Multiplayer re-enabled with old files -> current mode/membership/eligibility/control/source/shared-basis revalidation occurs before reuse.
16. Local planning contains private material -> no automatic shared/Narrator/player disclosure eligibility.
17. Planning generation is newer than LIVE/native state -> no LIVE/currentness override.
18. Story/planning file/ID/Git/CAS order differs from fiction -> no chronology inference.
19. Planning source disappears through lawful cleanup -> planning invalidates; canon is not reconstructed from it.
20. Story/planning cache survives native-state loss -> it cannot reconstruct accepted canon.
21. Newly generated Story remains physically visible in context -> no same-envelope Narrator/gameplay feedback.
22. A source-anchored constraint references a native owner without sufficient typed basis -> unusable until repaired/recomputed; no guessed universal revision.

---

# 15. Deferred / dormant / rejected baseline items

## Durable single-player planning

`DORMANT` until an accepted consumer proves bounded recomputation/current context insufficient and an independently durable lifecycle necessary.

## Planning partition/index

`DORMANT` until measured size/contention/retrieval budgets fail and a simpler bounded document cannot satisfy them.

## Durable Chronicler scheduler/queue

`REJECTED BASELINE`; revisit only if production evidence demonstrates queue-free pull catch-up cannot meet explicit anti-starvation requirements and a new owner is justified.

## Planning-based native-source retention blocker

`REJECTED BASELINE`; revisit only if a concrete future planning feature requires a source-retention promise that cannot be achieved by invalidation/rebase.

## Global Story search/index

`DERIVED/DORMANT`; add only for a measured bounded consumer, never as currentness authority.

## Configurable Dramaturg root selector

`DORMANT`; baseline fixed routes are sufficient. Revisit only if downstream scaffold/migration evidence proves a static selector useful. Such a selector can never own planning currentness.

---

# 16. Final canonical disposition

```text
CANONICAL_DIRECTION:              LAYER-LOCAL STORY PROJECTIONS / DERIVED CONTINUITY / EPHEMERAL SINGLE-PLAYER PREP / SCOPED MULTIPLAYER DRAMATURG HORIZONS / NATIVE-OWNER-FIRST INVALIDATION
STEP_6_BLOCKING:                  1
STEP_6_SIGNIFICANT:               7
UNRESOLVED_BLOCKING:              0
UNRESOLVED_SIGNIFICANT:           0
HUMAN_DECISION_REQUIRED:          NO
ARCHITECTURE_REOPENED:            NO
UPSTREAM_REOPEN_REQUIRED:         NO
IMPLEMENTATION_AUTHORIZED:        NO
WP_19_AUTHORIZED:                 NO
IMPLEMENTATION_PLANNING_AUTHORIZED: NO
NEXT_GATE:                        MANDATORY FINAL SENIOR AUDIT
```
