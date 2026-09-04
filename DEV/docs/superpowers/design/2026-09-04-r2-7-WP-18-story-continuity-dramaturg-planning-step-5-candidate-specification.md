# R2.7 WP-18 — Story / Continuity / Dramaturg Planning — Step-5 Candidate Specification

Status: **STEP 5 COMPLETE — CANDIDATE SPECIFICATION READY FOR INDEPENDENT STEP-6 REVIEW**

Date: 2026-09-04

Decision direction:

> **LAYER-LOCAL STORY PROJECTIONS / DERIVED CONTINUITY / EPHEMERAL SINGLE-PLAYER PREP / SCOPED MULTIPLAYER DRAMATURG HORIZONS / NATIVE-OWNER-FIRST INVALIDATION**

This is a candidate architecture specification. It becomes canonical only after independent Step-6 review, Step-7 resolution/propagation and Step-8 canonicalization. It authorizes no implementation.

---

# 1. Responsibility map

## 1.1 Story

Story is a durable, source-bound, noncanonical retrospective projection family.

It owns only:

- layer-local presentation/history units;
- layer-local Story ID allocation;
- compatible source-domain coverage;
- required layer-local projection/editorial metadata.

It does **not** own:

- objective/current truth;
- Actor cognition;
- fictional knowledge;
- human disclosure;
- gameplay execution;
- accepted mechanics/RNG;
- fictional chronology;
- recovery/currentness of native state;
- prospective Dramaturg planning.

## 1.2 Continuity

There is no generic continuity semantic owner.

Continuity is a bounded retrieval/projection concern over current owners and admitted history/projections. Story may orient retrieval; material reliance escalates to the applicable current/exact owner.

## 1.3 Actor intentional state

R2.2 source Actor remains the owner of current sparse non-epistemic intentional continuity, including applicable goals/objectives/intentions/commitments/reconsideration cues.

Dramaturg planning and Story cannot duplicate or override that owner.

## 1.4 Dramaturg planning

Dramaturg planning is prospective noncanonical preparation.

It owns only provisional planning coherence for its admitted scope. It does not own future fact, Actor intent, player agency, current world state, chronology, execution, knowledge/disclosure or recovery canon.

---

# 2. Fundamental laws

## WP18-01 — PREPARATION HAS NO ENTITLEMENT TO OCCUR

No prepared scene, event, reveal, Actor reaction, convergence, clue location, threat beat or outcome becomes mandatory merely because Dramaturg preparation retained it.

## WP18-02 — CANON INVALIDATES PREPARATION

Current accepted owners outrank preparation. An accepted player decision, source-Actor decision/state change, mechanics outcome, world/process transition, knowledge/disclosure change, LIVE/current-state movement or other native owner update invalidates any incompatible preparation.

Invalidation results in omission, discard, selective rebase or replacement preparation. The engine must never repair canon to restore a plan.

## WP18-03 — PROJECTION/PERSISTENCE DOES NOT PROMOTE AUTHORITY

Story/planning does not become canonical/current merely because it is durable, newer, shared, cached, indexed, repeated, copied, committed later or physically visible in the active context.

## WP18-04 — TECHNICAL ORDER IS NOT FICTIONAL CHRONOLOGY

Story sequence/ID, planning generation, file order, Git commit order, CAS order and message order do not by themselves establish fictional time or causality.

## WP18-05 — NATIVE RECOVERY WINS

Recovery reconstructs current/accepted state from native current/durable owners. Story/planning may assist orientation but never reconstruct accepted fiction, Actor state, PC intent, mechanics or RNG in place of missing native evidence.

---

# 3. Story physical contract

## 3.1 Root and routing

Use the accepted exceptional Story topology:

```text
<story_root>/<layer>/PROJECTION_STATE.yaml
<story_root>/<layer>/<floor(sequence/1000)>/<story_id>.yaml
```

where `<story_root>` resolves campaign-root-relative through the accepted static storage-routing model. Baseline implementation may use `STORY` as the default/root value according to downstream scaffold/schema rules.

`story_root` is routing metadata only. It cannot store coverage/currentness/generation.

## 3.2 Layer identities

Accepted baseline layers remain:

```text
TRANSCRIPT
EVENTS
MECHANICS
NARRATIVE
```

No global Story record/index/currentness owner is admitted.

## 3.3 Projection-state semantics

Each layer projection-state record owns conceptually:

```text
layer
story_id_allocator_high_water
coverage_by_source_domain[]
required_layer_local_index/editorial_metadata
```

Coverage entry compatibility is typed by source-domain contract and semantic contract generation. Projection-state currentness is layer/source-domain-relative.

## 3.4 Story units

A Story unit contains only the layer-specific presentation/history payload and source/projection basis required by its layer contract. It may contain references to native owner/evidence IDs sufficient for traceability and later escalation.

Cross-layer references are presentation/retrieval aids and do not create cross-layer authority or mandatory atomicity.

## 3.5 Candidate disposition

Every enumerated candidate requiring disposition is classified by its source contract as:

```text
MUST_MATERIALIZE
MAY_OMIT
```

Coverage may advance only after the candidate receives a legal terminal disposition and any required Story publication succeeds.

`MAY_OMIT` needs no durable skip record unless a later approved source contract proves one necessary.

## 3.6 Chronicler service

There is no durable Chronicler queue, lease, heartbeat, worker state or backlog record.

Backlog is derived from compatible source enumeration and layer coverage.

Turn-local service decision remains:

```text
NO_BACKLOG
SERVICE(window)
DEFER(reason)
```

Chronicler-generated draft content does not own Story IDs, coverage or publication.

## 3.7 Story concurrency/publication

Story publication uses validated ordinary non-force campaign publication consistent with WP-13.

- Story does not block accepted gameplay publication;
- conflict/contention yields to current gameplay;
- no cross-layer distributed transaction is required;
- source basis is revalidated as required by the relevant Story contract;
- same-ref CAS/optimistic publication serializes the affected Story owner only.

## 3.8 Story retrieval/eligibility

Story retrieval remains bounded by R2.3/WP-09. A Story unit is admitted to a logical role only after role/subject/purpose eligibility.

Story presence never grants fictional knowledge or human disclosure.

---

# 4. Continuity contract

## 4.1 No new record family

Baseline outcome:

```text
CONTINUITY: DERIVED ONLY
GENERIC_CONTINUITY_RECORD: NO
GLOBAL_MEMORY_GRAPH: NO
```

## 4.2 Retrieval path

Conceptually:

```text
current decision dependency
-> compact current routes / Story-history orientation where useful
-> bounded relevant source candidates
-> currentness + eligibility verification
-> exact/current native owner load when material
```

Story omission or index omission is never general proof of absence.

---

# 5. Single-player Dramaturg contract

## 5.1 Baseline durability

```text
SINGLEPLAYER_DRAMATURG: EPHEMERAL ONLY
DURABLE_SINGLEPLAYER_PLANNING_OWNER: NO
```

The single-player Dramaturg uses the current bounded context and `PreparationDraft` typed handoff. If it is lost/stale, prepare again from current owners.

## 5.2 Durability reopen trigger

A durable single-player owner may be proposed only if later evidence establishes an accepted consumer whose correctness/quality requirements cannot be met by bounded recomputation/current context and whose independent lifecycle justifies persistence.

Convenience, prompt cost already spent, or desire to remember an unused scene is insufficient.

---

# 6. Multiplayer retained Dramaturg contract

## 6.1 Admitted retained owners

Exactly two bounded retained-horizon families are admitted at baseline:

```text
shared multiplayer horizon
player-local horizon keyed by stable PLAYER identity
```

They remain noncanonical projection/preparation owners outside `world.*` and `runtime.*` current authority.

## 6.2 Physical route

Baseline deterministic route:

```text
<dramaturg_root>/SHARED.yaml
<dramaturg_root>/PLAYERS/<player_id>.yaml
```

A downstream static manifest/root selector may route `<dramaturg_root>`. The route itself cannot establish planning generation/currentness.

No planning registry, generic index or campaign-wide list is needed because both routes are derivable from known campaign/mode/PLAYER identity.

## 6.3 Stable local owner key

Player-local planning is keyed by stable campaign `player_id`, never GitHub login, display name, chat ID or PC ID.

PCs controlled by that PLAYER may be referenced in source basis. Controller changes do not silently transfer private planning ownership to another PLAYER.

## 6.4 Horizon shape

A retained horizon minimally supports conceptually:

```text
scope identity
generation
planning contract identity/version where needed
source_basis[]
assumptions[]
entries[]
invalidation/revalidation hints
shared_generation_hint?     # local horizon only
```

Implementation may choose exact field names only after schema work is authorized. No extra field is admitted solely because it is easy to serialize.

## 6.5 Planning entries

Entries are embedded typed values, not independently addressable campaign records.

Accepted classes:

```text
SOURCE_ANCHORED_CONSTRAINT
PROVISIONAL_DRAMATURGIC_DIRECTION
```

An implementation-local deterministic entry key may support comparison/update inside one document but does not create independent identity, backlinks, GC ownership or global routing.

## 6.6 Source-anchored constraints

A source-anchored constraint stores sufficient native source identity/basis to revalidate its claim. It must not copy a mutable native fact and then treat the copy as authority.

If current source evidence has moved incompatibly, the planning entry is stale even if planning generation is the newest planning generation.

## 6.7 Provisional directions

A provisional direction is always disposable and conditional. Retaining or repeating it across generations does not promote it to truth, Actor intent, knowledge, chronology or an execution obligation.

---

# 7. Planning currentness, authorization and CAS

## 7.1 Distinct currentness domains

The following remain distinct:

```text
planning generation
campaign branch/current native owner basis
LIVE epoch/current source
HOT local current state
PLAYER/control authorization
Actor source state
fictional chronology
```

No single scalar/frontier unifies them.

## 7.2 Shared planning mutation preconditions

Before accepting a material shared-horizon mutation, the runtime establishes at least:

1. current campaign identity and multiplayer mode;
2. current authenticated principal -> active PLAYER binding as applicable;
3. operation eligibility for the shared planning scope;
4. exact current shared planning generation/base;
5. compatibility of material current native source basis;
6. absence of a native-owner contradiction that already invalidates the retained proposal.

## 7.3 Publication

Retained planning is campaign-owned noncanonical data and publishes through the ordinary campaign-tree optimistic/non-force path.

Planning publication:

- cannot turn planning into canon;
- cannot create fictional chronology from commit order;
- cannot require a campaign+LIVE distributed transaction;
- cannot override a newer native owner because the planning write won transport CAS.

## 7.4 Conflict

On conflict/current-base movement:

```text
read current affected horizon/native dependencies
-> verify authorization/currentness
-> classify compatibility
-> keep compatible entries
-> rebase/rewrite only where semantically safe
-> discard incompatible provisional content
-> publish successor generation if still useful
```

Blind text merge/LWW is forbidden.

A conflict never authorizes restoration of the older planned fiction.

---

# 8. Planning lifecycle and invalidation

## 8.1 Derived usability states

Baseline planning usability is derived, not owned by a self-sufficient stored validity flag:

```text
ABSENT
CURRENT_COMPATIBLE
STALE_OR_INCOMPATIBLE
INACTIVE_MODE
CORRUPT_OR_UNUSABLE
```

Stored metadata may support validation, but `active=true` / `valid=true` cannot outrank current mode/source evidence.

## 8.2 Successor generation

An accepted material retained-horizon update produces a successor generation for that same bounded horizon. Generation is monotonic owner-local metadata only.

It is not global time, Story coverage or gameplay order.

## 8.3 Selective invalidation

When a bounded current-source change invalidates only some planning entries, compatible entries may survive after explicit revalidation. Invalid entries are omitted/rebased/replaced.

Do not regenerate the whole campaign plan merely because one source changed, and do not preserve incompatible content merely to save previous preparation effort.

## 8.4 Mode transition

When multiplayer becomes disabled:

- shared retained planning is semantically inactive immediately under current mode;
- physical bytes may remain until ordinary cleanup/scaffold policy handles them;
- no player/runtime may treat them as current preparation authority.

On re-enable:

- discover bounded retained horizons;
- revalidate scope/source basis/current PLAYER mappings;
- reuse compatible entries only;
- discard/rebuild incompatible content before use.

---

# 9. Privacy / eligibility

## 9.1 Local planning privacy

Membership in the campaign or physical repository visibility does not grant semantic access to another PLAYER's local planning.

Local horizon content enters shared planning or another logical role only through an independently eligible/authorized projection/handoff.

## 9.2 Narrator containment

Narrator cannot consume raw Dramaturg horizon content merely because it exists in the same physical context. Current WP-08/R2.4 role binding and eligible typed handoff remain required.

## 9.3 Story containment

Newly produced Story is not eligible as same-envelope gameplay/Narrator evidence. It may become future bounded context only after ordinary current role binding/eligibility.

---

# 10. Actor / agency boundary

## 10.1 Actor state

Current NPC/Actor goals/objectives/intentions/commitments/reconsideration remain source-Actor state under R2.2.

Planning may record expected/conditional reactions based on that state but cannot own the real current intention.

## 10.2 PC agency

No planning entry may establish a voluntary PC action, speech, belief, emotion, allegiance, goal, consent or interpretation.

Convergence/pressure prep may describe world opportunities/constraints only.

---

# 11. Recovery / failure

## 11.1 Story loss

If Story is absent/stale/corrupt:

- native gameplay state remains recoverable from native owners;
- Story may be regenerated/caught up from compatible source contracts where source continuity permits;
- no gameplay rollback is authorized merely to restore Story.

## 11.2 Planning loss

If retained planning is absent/stale/corrupt:

```text
establish current campaign/mode/PLAYER/native sources
-> discard unusable planning
-> reprepare bounded horizon if useful
```

No accepted action, Actor decision, mechanics result or fictional fact is reconstructed from planning.

## 11.3 Partial publication/adoption

If a noncanonical Story/planning publication is accepted remotely but local adoption/cache update fails, remote publication evidence controls that projection owner's durable result. Recovery must not replay gameplay or treat local cache as stronger.

If publication itself did not succeed, no durable projection update is claimed.

---

# 12. Cleanup / retention

## 12.1 Story

Story source retention/compaction follows existing Step-5.10/5.11/5.13 source-contract obligations.

## 12.2 Planning

Planning references are not default GC retention blockers for native sources.

Old/inactive planning bytes may be cleaned under downstream scaffold/cleanup rules when not needed for current bounded retained horizon operation. Physical residue does not remain semantically active.

No planning tombstone/history registry is required for correctness.

---

# 13. Bounded discovery / resource behavior

- no global campaign Story/planning scan on ordinary play;
- Story uses known layer projection state + bounded source-domain windows;
- local planning direct-routes from known PLAYER;
- shared planning direct-routes from multiplayer mode;
- source revalidation follows bounded registered owner routes;
- no background planning invalidation scan;
- no planning graph traversal;
- no preload of all Story/planning into every role/context.

If measured scale later exceeds accepted resource budgets, WP-24 may trigger a reviewed partitioning/index change. Scale is not assumed today.

---

# 14. Machine realization obligations after architecture approval

Later implementation must align at least:

1. Story unit/projection-state schemas with Step-5.10/WP-11;
2. retained Dramaturg horizon schema/value contract;
3. static campaign routing/root selectors as required by accepted topology;
4. catalog/admission-ledger provenance to current R2.5/WP-18 semantics;
5. current CORE/instruction mapping without parallel role instruction subsystem;
6. validation for stable PLAYER route, generation/source basis and typed entries;
7. executable tests for:
   - Story nonauthority and retirement of chapter architecture;
   - Actor/Story/planning separation;
   - single-player no-durable planning baseline;
   - local/shared planning privacy;
   - mode disable/re-enable;
   - exact-base CAS/rebase/no LWW;
   - source invalidation/canon-wins;
   - loss/corruption recovery;
   - no mechanics/RNG replay;
   - no technical-order chronology;
   - no same-envelope Story feedback;
   - R2.6 post-implementation host containment/evaluation obligations.

These obligations are not implementation authorization.

---

# 15. Dormant / conditional / revisit items

### Durable single-player planning

`DORMANT` until an accepted consumer proves bounded recomputation/current-context insufficient.

### Planning partition/index

`DORMANT` until measured size/contention/retrieval budgets fail and a simpler bounded document cannot satisfy them.

### Durable Chronicler scheduler/queue

`REJECTED BASELINE`; revisit only if production evidence demonstrates queue-free pull catch-up cannot meet explicit anti-starvation requirements and a new owner is justified.

### Planning-based source retention blocker

`REJECTED BASELINE`; revisit only if a concrete future planning feature requires a source-retention promise that cannot be achieved by invalidation/rebase.

### Global Story search/index

`DERIVED/DORMANT`; add only for a measured bounded consumer, never as currentness authority.

---

# 16. Candidate acceptance tests

A valid implementation of this candidate must preserve these counterexamples:

1. Delete all Story while native canon remains healthy -> gameplay/recovery remains valid.
2. Story contradicts current Actor/world owner -> native owner wins.
3. Story layer A caught up and layer B behind -> no global Story currentness inference.
4. Chronicler deferred repeatedly -> no durable scheduler appears.
5. `PreparationDraft` serialized -> still not durable owner.
6. Single-player context lost -> reprepare; no durable planning required.
7. Shared planning says NPC will betray; Actor changed -> planning invalidates/rebases.
8. Shared planning says PC will agree -> illegal PC-agency assertion.
9. Shared horizon CAS succeeds after native source moved incompatibly -> transport success alone cannot make stale preparation semantically current.
10. PLAYER/control changes -> local/shared planning eligibility is revalidated.
11. Multiplayer disabled -> shared bytes inactive.
12. Re-enable with stale files -> revalidate/discard/rebuild before use.
13. Local planning contains private material -> no automatic shared/Narrator eligibility.
14. Planning generation newer than LIVE -> no LIVE/currentness override.
15. Story/planning file/ID/Git order differs from fiction -> no chronology inference.
16. Planning source disappears through lawful cleanup -> plan invalidates; no canon reconstruction.
17. Story/planning cache survives native-state loss -> cannot reconstruct accepted canon from projection/prep.
18. Newly generated Story physically remains in context -> no same-envelope feedback.

---

# 17. Candidate disposition

```text
CANDIDATE_DIRECTION:          ALTERNATIVE C WITH STEP-4 REFINEMENTS
HUMAN_DECISION_REQUIRED:      NO
UPSTREAM_REOPEN_REQUIRED:     NO
IMPLEMENTATION_AUTHORIZED:    NO
STEP_6_REQUIRED:              YES — INDEPENDENT WHOLE-PROJECT RECONSTRUCTION
```
