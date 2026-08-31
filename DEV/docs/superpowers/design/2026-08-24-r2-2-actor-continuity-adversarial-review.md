# R2.2 Adversarial Review — Actor Continuity, Cognition and Lazy Discovery Handoff

Status: **ADVERSARIAL REVIEW**

Date: 2026-08-24

Candidate specification:

- `DEV/docs/superpowers/design/2026-08-24-r2-2-actor-continuity-candidate-spec.md`

Owner decision:

- `DEV/docs/superpowers/design/2026-08-24-r2-2-actor-continuity-owner-decision.md`

This review tests the owner-approved A architecture and the added lazy-loading/downstream-discovery constraint. It does not redesign R2.3 retrieval policy.

---

# 1. Review verdict

The source-Actor-owned sparse-continuity architecture remains sound.

No new owner-level product/architecture choice is required.

However, six clarifications are required before canonicalization. Three are Actor-state correctness clarifications and three protect lazy discovery from becoming hidden authority or a false-negative source.

---

# 2. Actor-state findings

## AR-1 — Relationship facets must not duplicate objective social facts

### Attack

`felt_obligation`, hostility or trust can be confused with objective contract/debt/allegiance facts.

If downstream code treats a subjective facet as objective state, R2.2 would recreate the truth/cognition contamination Step 4 rejected.

### Required clarification

Relationship facets are **subjective source-Actor cognition only**.

A relationship view may reference objective/evidentiary sources, but cannot establish:

- legal/actual debt;
- contract existence;
- faction membership;
- ownership;
- target intent;
- mutual consent;
- reciprocal relationship state.

Canonicalization must make this distinction explicit at the relationship definition, not only in a general ownership paragraph.

Disposition: **AGENT CLARIFICATION / NO OWNER DECISION**.

---

## AR-2 — “Foundation change by long-term development” needs an anti-drift threshold

### Attack

A sequence of individually plausible small assessments could gradually rewrite stable values/temperament without any one update looking like a foundation change.

### Required clarification

Ordinary Actor cognition deltas SHALL NOT mutate foundation by accumulation.

Foundation change requires an explicitly classified foundation-transition operation/cause, with stronger provenance/review/validation than ordinary evolving-cognition mutation.

The exact machine operation is downstream, but the semantic boundary must be explicit now.

Disposition: **AGENT CLARIFICATION / NO OWNER DECISION**.

---

## AR-3 — Persisted transient state needs invalidation ownership, not just prose expiry hints

### Attack

If persisted transient state merely contains prose such as “until calm,” it can survive indefinitely because no deterministic/runtime boundary knows when it becomes invalid.

### Required clarification

Persisted transient state must use an **inspectable invalidation condition/ref** tied to existing fictional state/time/event owners where possible.

R2.2 does not introduce a scheduler, but it must make stale transient state detectably invalid when a relevant owner changes or an applicable fictional-time/event boundary is evaluated.

Disposition: **AGENT CLARIFICATION / NO OWNER DECISION**.

---

# 3. Lazy-discovery findings

## AR-4 — Derived index omission cannot prove entity absence

### Attack

A stale or incomplete `NPC_INDEX`, scene manifest or relevance cache can omit an Actor. If omission is treated as “this Actor is not here/relevant,” lazy loading turns an optimization defect into false world state.

### Required clarification

A derived discovery surface is **positive-candidate evidence**, not general closed-world authority.

Absence from a derived index/manifest SHALL NOT prove absence from the scene/location/world unless that exact index contract provides a current exhaustive guarantee for the queried scope.

When correctness depends on presence/absence, Context Runtime must verify through the applicable current owner/routed live source or another source with an explicit exhaustive contract.

Disposition: **MANDATORY R2.3 HANDOFF**.

---

## AR-5 — Campaign-base location/index data may be stale during a live epoch

### Attack

`world.actor.location_id` or campaign-level indexes can describe the base campaign state while a selected live epoch currently owns mutable Actor/scene state through overlays.

A lazy candidate scan that ignores routing can miss moved/created/touched entities or load stale Actor state.

### Required clarification

Discovery/currentness must respect the same source-routing law as ordinary state reads.

If a live source currently owns the relevant scope, candidate discovery and any material verification must account for its:

- scene overlay;
- entity overlays;
- created entities;
- touched/current owner evidence;
- exact current live revision as applicable.

Campaign indexes remain hints unless their own currentness is established against routed authority.

Disposition: **MANDATORY R2.3/R2.5 INTEGRATION CONSTRAINT**.

---

## AR-6 — Location-only discovery is insufficient and secret-bearing metadata can leak

### Attack A — relevance

An Actor can be materially relevant without being physically co-located:

- remote faction/antagonist process;
- known contact referenced by the player;
- owner of an object/document;
- Actor implicated by current thread/evidence;
- causal participant in an imminent consequence.

A pure `actors_at_location` manifest would miss these consumers.

### Attack B — secrecy

A low-cost discovery index containing descriptive labels such as “secret cult leader” can leak material information before full role eligibility is evaluated.

### Required clarification

R2.3 discovery must combine **typed relevance channels**, with co-location only one channel.

Candidate metadata exposed before full source load must be bounded and eligibility-safe. Opaque IDs/type/path and non-secret selector metadata may be usable before deeper retrieval; secret-bearing descriptions require the same role/subject/player eligibility discipline as full content.

The first discovery tier is not permission to preload hidden names, motivations, relationship summaries or Story spoilers.

Disposition: **MANDATORY R2.3 HANDOFF**.

---

# 4. Other attacks and outcomes

## 4.1 Every assessment mutates state

Blocked by `NO_CHANGE` law and bounded delta semantics.

No new finding.

## 4.2 Actor continuity duplicates `world.knowledge`

Candidate explicitly reserves proposition stance to `world.knowledge`.

No new finding.

## 4.3 Separate physical relationship files accidentally become semantic owners

Candidate explicitly states physical normalization does not transfer source-Actor ownership.

No new finding.

## 4.4 Story/history launders current cognition

Candidate R2.2-22 requires current cognition through the proper owner path.

No new finding.

## 4.5 Incidental NPC over-modeling

Progressive materialization and sparse continuity block automatic deep records.

No new finding.

## 4.6 PC mind takeover

Player-agency law is explicit and remains mandatory.

No new finding.

---

# 5. Required canonicalization changes

Canonical R2.2 specification must incorporate:

1. **AR-1:** subjective relationship facets cannot establish objective social facts;
2. **AR-2:** foundation mutation requires an explicit foundation-transition class/cause, not cumulative ordinary deltas;
3. **AR-3:** persisted transient state uses inspectable invalidation tied to existing state/time/event owners;
4. **AR-4:** derived discovery omission is not general proof of absence;
5. **AR-5:** discovery/currentness follows routed live/current authority rather than campaign-base indexes blindly;
6. **AR-6:** discovery is multi-channel, not location-only, and pre-load metadata must obey secrecy/eligibility boundaries.

None changes owner-selected Alternative A.

---

# 6. Diamond / Strong disposition after review

| Item | Result in R2.2 |
|---|---|
| D10 stable/durable/transient | **ADOPTED / REFINED** — three lifetimes under one source-Actor semantic owner; foundation gets stronger mutation boundary; transient persistence gets inspectable invalidation. |
| D11 truth/knowledge/belief/intention separation | **PARTLY INHERITED + ACTIVE DELTA ADOPTED** — Step-4 epistemics remain `world.knowledge`; R2.2 adds non-epistemic goals/intention/relationship/private continuity only. |
| D12 directed relationships/player agency | **ADOPTED** — A->B independent of B->A; player-controlled voluntary mental state excluded. |
| D13 sparse/event-driven cognition | **ADOPTED** — bounded relevant Actors and material triggers; no always-on NPC simulation. |
| S07 explicit cognition modes | **ADOPTED AS SEMANTIC PURPOSES** — small purpose vocabulary; no orchestration framework in R2.2. |
| S10 NO_CHANGE | **ADOPTED** — successful assessment without forced write. |
| S11 transient TTL | **PROBLEM ADOPTED / TURN-TTL REJECTED** — inspectable fictional event/state/time invalidation instead of generic turn counter. |
| D09 evidence-bound mutation | **ADOPTED AS SPECIALIZED APPLICATION** — bounded Actor-purpose delta plus deterministic owner/currentness/source/shape validation. |
| S27 one mutation per assessment | **REFORMULATED** — one bounded Actor + one assessment-purpose delta; may coherently update several dependent Actor-local fields. |
| S06 bounded active cast | **INHERITED / PRESERVED** — progressive materialization and current NPC/runtime doctrine already cover it. |
| S08 protected core/selective forgetting | **DORMANT** — revisit only under demonstrated Actor-local context/storage pressure. |
| S09 staged evolution | **DORMANT** — revisit for authored companions/major NPC arcs; not baseline personality machinery. |

---

# 7. Closure recommendation

After incorporating AR-1 through AR-6, R2.2 may proceed to canonical specification and resolution gate without another owner decision.

The lazy-loading mechanism itself remains intentionally unresolved until R2.3. The R2.2 closure obligation is to make **discoverability without full semantic load** a mandatory downstream contract and prevent discovery indexes from becoming semantic authority.
