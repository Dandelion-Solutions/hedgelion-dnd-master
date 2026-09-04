# R2.7 WP-18 — Story / Continuity / Dramaturg Planning — Step-4 Collaborative Architecture Review

Status: **STEP 4 COMPLETE — ALTERNATIVE C ACCEPTED WITH REFINEMENTS / NO HUMAN-OWNED MATERIAL DECISION**

Date: 2026-09-04

Reviewed artifact:

- `DEV/docs/superpowers/design/2026-09-04-r2-7-WP-18-story-continuity-dramaturg-planning-step-3-decision-brief.md`

This review challenges the Step-3 recommendation from product-semantics, authority, recovery, concurrency, privacy, machine-realization and YAGNI perspectives. It does not implement the design.

---

## 1. Review question

Can the recommended scoped-horizon architecture satisfy the accepted Story/R2.2/R2.5/currentness contracts without introducing hidden authority, under-specified lifecycle or a machine-only convenience subsystem?

Recommendation under review:

> **LAYER-LOCAL STORY PROJECTIONS / DERIVED CONTINUITY / EPHEMERAL SINGLE-PLAYER PREP / SCOPED MULTIPLAYER DRAMATURG HORIZONS / NATIVE-OWNER-FIRST INVALIDATION**

---

## 2. Challenge: does `DRAMATURG/SHARED.yaml` become a campaign plot owner?

**Risk:** A durable shared preparation file may socially and technically become “the plot”, especially if it contains cross-player threads/convergence/mystery constraints.

**Resolution:** The file is admitted only as a noncanonical projection/preparation owner for **preparation coherence**, never for truth, accepted fiction or execution. The candidate spec must require:

- every material source-anchored claim to retain source identity/basis;
- provisional directions to remain explicitly noncanonical;
- current owner revalidation before material use;
- current player/Actor/mechanics/native transitions to invalidate incompatible preparation;
- no protected ending/convergence;
- no write from planning directly into current native owner state except through ordinary gameplay/world-authoring paths that independently establish canon.

The shared horizon may constrain what different Dramaturg passes remember as preparation, not what players must do or what fiction must become.

**Disposition:** accepted with explicit anti-promotion law.

---

## 3. Challenge: is one shared document a scalability mistake?

**Risk:** Multiplayer contention could make one file hot.

**Evidence:** Current accepted R2.5 semantics define one small shared horizon, not a high-cardinality planning database. WP-11 prefers monolithic bounded indexes/owners until measured scale proves a partitioning trigger. Planning loss is quality-only and conflicts are expected to rebase/discard rather than serialize gameplay.

**Resolution:** Keep one shared document baseline. Revisit partitioning only with WP-24/measured evidence that bounded file size or contention materially violates budgets and cannot be solved by smaller horizon content.

**Disposition:** no preemptive partitioning.

---

## 4. Challenge: should each planning entry have stable identity?

**Risk:** Selective rebase/edit seems easier with entry IDs.

**Counter-risk:** Stable independent IDs create reference lifecycle, reverse lookup, orphan cleanup and possible semantic identity that no current consumer requires.

**Resolution:** Entries remain embedded typed values inside one horizon generation. A deterministic within-document key may be used for local comparison/update if implementation needs it, but it is not an independently addressable campaign record identity and cannot create backlinks/retention authority.

**Disposition:** no independent planning-entry record family.

---

## 5. Challenge: is generation enough to prove currency?

**Risk:** A newer generation can still be stale relative to Actor/LIVE/world changes.

**Resolution:** Generation serializes one horizon's publication history only. Current usability requires revalidation of material source basis and current mode/authorization. Generation alone never proves semantic currentness.

The candidate must distinguish:

```text
planning generation
campaign branch/current owner revision
LIVE epoch/currentness
Actor source revision/basis
fictional chronology
```

No scalar unification.

**Disposition:** accepted with explicit generation nonauthority.

---

## 6. Challenge: should inactive/invalid planning be persisted as lifecycle enums?

**Risk:** Without stored lifecycle, old bytes look active.

**Counter-risk:** A stored `valid=true`, `active=true` or lifecycle state can itself become stale and create another currentness owner.

**Resolution:** Semantic usability is derived from current campaign mode/scope + compatible planning contract + source/currentness validation. Stored metadata may include generation/source basis/invalidation hints, but not a self-sufficient validity assertion.

On multiplayer disable, shared bytes need not be deleted immediately. They are ineligible by current mode. On re-enable, revalidate or discard/rebuild before use.

**Disposition:** derived lifecycle state preferred.

---

## 7. Challenge: can planning refs accidentally hold canon alive forever?

**Risk:** Long-lived prep referencing obsolete entities/events could block cleanup.

**Resolution:** No default planning retention blocker is admitted. Source-anchored constraints must tolerate current-source movement/removal by invalidation/rebase. Only an explicit future consumer with an owner-level retention promise could change this.

Story retains only the already accepted source-enumeration/compaction continuity obligations.

**Disposition:** no planning GC retention authority.

---

## 8. Challenge: does retained local planning leak private player material?

**Risk:** Repository/runtime may physically access all planning files.

**Resolution:** Physical readability remains separate from role/recipient eligibility. `DRAMATURG/PLAYERS/<player_id>.yaml` is semantically scoped to that stable PLAYER. Shared horizon construction must not copy private/local material unless independently eligible and intentionally shared under the relevant owner contract.

Narrator never receives raw local/shared planning by physical co-presence alone; R2.4/WP-08 typed handoff/fresh rebind still applies.

**Disposition:** accepted with recipient-safe projection boundary.

---

## 9. Challenge: should local planning be keyed by PC instead of PLAYER?

**Risk:** One player can control more than one PC over campaign history.

**Evidence:** R2.5 defines player-local horizon and WP-16 makes stable PLAYER the human participation/control owner. PC control can change while the same PLAYER identity persists.

**Resolution:** Key retained local planning by stable `player_id`. Entries may reference current controlled PC(s) as ordinary source basis, but PC identity does not replace the player-local horizon owner.

**Disposition:** PLAYER-keyed route accepted.

---

## 10. Challenge: should single-player next-horizon prep be retained at session end?

**Risk:** `CAMPAIGN_OPERATIONS.md` says “retain only plausible next-horizon prep”, which could imply durable persistence.

**Interpretation:** “retain” is an operational prep instruction, not an independent durability admission. WP-10/WP-11 explicitly leave single-player durable planning unadmitted and R2.4 allows ephemeral typed handoffs/current context.

**Resolution:** Baseline single-player planning remains ephemeral. Session/chat continuity may preserve it opportunistically, but recovery correctness never depends on it. If context is lost, reprepare from current owners.

**Disposition:** no durable single-player owner.

---

## 11. Challenge: Story layer-local indexes versus no global Story index

**Risk:** Narrative continuity may need cross-layer/campaign queries.

**Resolution:** Step 5.10 already permits required local indexes/editorial metadata and bounded source-domain catch-up. R2.3 provides progressive retrieval. Cross-layer references are presentation aids, not a reason for a global authoritative index. A derived/rebuildable search aid may be added only if a concrete measured consumer later requires it.

**Disposition:** preserve no baseline global Story index.

---

## 12. Challenge: could Chronicler starvation require a durable scheduler?

**Risk:** Gameplay-priority deferral may indefinitely postpone Story.

**Evidence:** Step 5.10/R2.4 intentionally use queue-free pull catch-up; backlog is derivable and R2.6 requires later anti-starvation evaluation.

**Resolution:** Do not change correctness architecture. Later evaluation may tune bounded service opportunity policy, but not by creating a durable scheduler unless measured evidence proves current design insufficient and a new owner is approved.

**Disposition:** no scheduler/service record.

---

## 13. Challenge: can Story or planning recover lost HOT/SOFT canon?

**Risk:** They may be the only surviving readable narrative evidence.

**Resolution:** No. WP-13/WP-14 and current runtime explicitly require truthful durable/current-owner recovery. Story/planning may aid orientation/diagnosis but cannot synthesize missing accepted canon, mechanics, RNG or player choices.

**Disposition:** native-owner-first recovery remains mandatory.

---

## 14. Challenge: catalog/admission-ledger provenance mismatch

**Observation:** Current machine vocabulary for planning exists, but admission-ledger semantic provenance does not fully name the accepted R2.5 retained-planning owner.

**Resolution:** Candidate spec must include a future machine-alignment obligation to route planning vocabulary provenance through the accepted R2.5/WP-18 owner chain. Do not modify catalog during architecture Steps 2–8.

**Disposition:** implementation-facing propagation obligation, not architecture reopen.

---

## 15. Challenge: Story/planning schema absence

**Observation:** Current machine tree lacks dedicated Story/planning schemas and current manifest lacks the future Story root selector.

**Resolution:** This is expected R2.7 realization debt. Candidate architecture must be sufficiently implementation-facing to define record/value ownership, routing, invariants and tests, but implementation remains downstream after Senior closure.

**Disposition:** no architecture-time schema write.

---

## 16. Refined candidate direction

Alternative C survives review with these refinements:

1. one accepted layer-local Story topology, no global Story index/service state;
2. no generic continuity owner;
3. source Actor remains sole current intentional-state owner;
4. single-player prep remains ephemeral;
5. multiplayer retained planning uses one shared + per-PLAYER local bounded horizon documents;
6. entries embedded, no independent IDs/registry;
7. generation serializes only horizon publication, not semantic currentness/chronology;
8. semantic usability derived by current mode/authorization/source revalidation;
9. no default planning GC retention blockers;
10. no raw private/local planning promotion into shared/Narrator context;
11. planning conflicts rebase/discard; never restore plot;
12. R2.6 acceptance obligations remain post-implementation;
13. machine provenance/schema/test alignment is a downstream implementation obligation.

---

## 17. Review disposition

```text
ALTERNATIVE_A:                REJECTED — fails accepted multiplayer consumer
ALTERNATIVE_B:                REJECTED — unnecessary global owner/registry complexity
ALTERNATIVE_C:                ACCEPTED WITH REFINEMENTS
HUMAN_DECISION_REQUIRED:      NO
UPSTREAM_REOPEN_REQUIRED:     NO
MATERIAL_RISK_ACCEPTANCE:     NO
IMPLEMENTATION_AUTHORIZED:    NO
NEXT_STEP:                    STEP 5 CANDIDATE SPECIFICATION
```
