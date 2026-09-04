# R2.7 WP-18 — Step 6 Whole-Project Adversarial Review

Status: **STEP 6 COMPLETE — FINDINGS REQUIRE STEP-7 PROPAGATION**

Date: 2026-09-04

Candidate basis: `f1e0a9695ea7f8cb8593f47c2f94423c94379b0c`

Companion independent reconstruction:

- `DEV/docs/superpowers/design/2026-09-04-r2-7-WP-18-story-continuity-dramaturg-planning-step-6-source-manifest-reconstruction.md`

This review attacks the Step-5 candidate after independently rebuilding the material owner/consumer graph. It does not limit itself to Step-1 assumptions or previously known Senior findings.

---

## 1. Result

```text
STEP_6_BLOCKING:      1
STEP_6_SIGNIFICANT:   7
STEP_6_MINOR:         0

HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
```

All eight findings are mechanically resolvable within accepted architecture. Step 8 is blocked until Step 7 closes and propagates every item.

---

## 2. F18-01 — BLOCKING — player-local horizon may omit consumed shared basis

**Attack.** Step-5 candidate makes local `shared_generation_hint` optional. R2.5, however, requires player-local work that consumed a shared Dramaturg generation to retain enough exact shared basis for bounded revalidation/rebase when shared planning materially moves.

**Failure mode.** A durable player-local horizon could appear usable after the shared basis it consumed changed, with no exact dependency edge from which to detect/revalidate that change.

**Required repair.** Replace optional hint semantics with an explicit local `shared_basis` discriminator:

```text
ABSENT
    local horizon did not consume shared planning

BOUND
    local horizon consumed shared planning
    -> shared_generation required
    -> bounded shared record/basis evidence required
```

If shared planning was consumed, this basis is mandatory. Shared movement triggers bounded dependency revalidation/rebase/discard. The dependency remains planning-local; it is not fictional chronology or global freshness.

**Severity:** `BLOCKING`

---

## 3. F18-02 — SIGNIFICANT — retained-generation publication/currentness boundary under-specified

**Attack.** Candidate says publication failure means no durable update, but does not sharply distinguish same-context planning work from the durable retained generation visible to independent contexts.

**Failure mode.** One Master context may treat an unpublished recomputed horizon as “current shared planning” while another can only observe the prior published generation.

**Required repair.** State explicitly:

- recomputed planning candidate is EPHEMERAL until successful retained-horizon publication;
- only a successfully published generation can become the retained cross-context coordination basis;
- publish failure/defer/conflict leaves the candidate non-durable and non-selected for other contexts;
- prior published compatible generation remains the retained basis if applicable, otherwise retained basis is absent/stale;
- gameplay/native owner changes remain true regardless of planning publication success;
- this is planning retention semantics, not a new universal HARD gameplay boundary.

**Severity:** `SIGNIFICANT`

---

## 4. F18-03 — SIGNIFICANT — multiplayer disable semantics cover shared horizon but not all retained planning

**Attack.** Candidate explicitly makes shared horizon inactive when multiplayer is disabled, while accepted durable-retention admission is multiplayer-only for both shared and player-local horizon families.

**Failure mode.** Durable player-local multiplayer planning can silently remain active during single-player mode and become an undeclared single-player durable planning owner.

**Required repair.** When multiplayer is disabled:

- shared retained horizon is semantically inactive;
- player-local retained multiplayer horizons are also semantically inactive;
- bytes may remain physically;
- ordinary single-player prep is EPHEMERAL ONLY;
- on re-enable, discover/revalidate compatible retained horizons or discard/rebuild them.

**Severity:** `SIGNIFICANT`

---

## 5. F18-04 — SIGNIFICANT — player-local membership/control/eligibility invalidation incomplete

**Attack.** Stable PLAYER is the correct route identity, but candidate does not fully define how deactivation, control transfer and current recipient eligibility affect use of retained local planning.

**Failure mode.** Private planning can be reused after the PLAYER is inactive, or accidentally transfer to a successor controller merely because the controlled PC changed hands.

**Required repair.** Local horizon load/use/write requires current active PLAYER membership and applicable role/recipient eligibility; where an entry depends materially on a controlled PC/entity, current control/subject compatibility is also required. Deactivation/control transfer does not transfer private local planning to another PLAYER. Incompatible local horizon becomes stale/unusable; bytes may remain. WP-16 remains the control owner.

**Severity:** `SIGNIFICANT`

---

## 6. F18-05 — SIGNIFICANT — generic `source_basis[]` risks becoming universal freshness token

**Attack.** Candidate uses `source_basis[]` but under-specifies its item semantics. R2.3 explicitly rejects generic freshness vectors/currentness tokens across heterogeneous owners.

**Failure mode.** Implementation invents one generic revision scalar/vector and silently makes planning the arbiter of whether Actor/world/knowledge/LIVE sources are current.

**Required repair.** Each declared source-basis item must carry:

- native owner/domain/type;
- bounded native identity/partition/key;
- owner-defined expected currentness evidence where applicable;
- no universal comparison rule.

Comparison/revalidation delegates to native owner semantics. `SOURCE_ANCHORED_CONSTRAINT` requires source basis. Provisional directions may carry declared assumptions/relevant anchors. Only declared dependencies are revalidated.

**Severity:** `SIGNIFICANT`

---

## 7. F18-06 — SIGNIFICANT — exact retained-planning physical root remains ambiguous

**Attack.** Candidate writes `<dramaturg_root>/...` and allows a future static root selector. WP-18's physical-realization question requires a baseline location, while no evidence requires a new routing selector now.

**Failure mode.** Implementation planning invents a manifest field/root negotiation prematurely or different consumers choose different planning roots.

**Required repair.** Freeze current baseline physical routes as campaign-root-relative:

```text
DRAMATURG/SHARED.yaml
DRAMATURG/PLAYERS/<player_id>.yaml
```

No registry/index is introduced. No manifest selector is required by WP-18 architecture. Any future configurable selector belongs to downstream scaffold/migration work and cannot become currentness authority.

**Severity:** `SIGNIFICANT`

---

## 8. F18-07 — SIGNIFICANT — planning catalog admission provenance does not name current planning owner

**Attack.** `DEV/CATALOG/catalog-admission-ledger.json` classifies `planning_entry_classes` as `INHERITED_ACTIVE`, but its provenance names R2.1 + Step 5.10 while material planning semantics are owned by R2.5 and finalized by WP-18 realization.

`DEV/ARCHITECTURE/CATALOG_ADMISSION.md` requires active generated identifiers to have exact accepted owner provenance.

**Failure mode.** Later catalog/schema work can route planning semantics through Story/continuity owners and erase the Actor/Story/planning separation.

**Required repair.** Step-7/final canonical spec must propagate an implementation obligation to align catalog admission provenance with accepted R2.5 planning semantics plus final WP-18 realization owner as appropriate. This is traceability alignment, not an identifier-semantic change. Do not modify catalog implementation during architecture work.

**Severity:** `SIGNIFICANT`

---

## 9. F18-08 — SIGNIFICANT — Source Manifest contains a false current Project-Map negative finding

**Attack.** Expanded Steps-2–5 Manifest still says absent `GAME/CORE/STORY.md` implies the current `DEV/PROJECT_MAP.md` Story route is stale. Fresh Step-6 read shows current Project Map no longer routes Story through that missing legacy file.

**Failure mode.** The Source Manifest itself becomes stale routing evidence and can misdirect later architecture/implementation work.

**Required repair.** Remove the false current-Project-Map attribution. If retained, absence of the legacy file is historical negative evidence only. Record the actual current Project-Map routing through accepted Step-4/Step-5/R2.x owners/current runtime consumers. Keep the Manifest open-world.

**Severity:** `SIGNIFICANT`

---

## 10. Adversarial cases after required repairs

The repaired architecture must satisfy at least:

1. local horizon created without shared planning -> `shared_basis=ABSENT` is valid;
2. local horizon created from shared generation N -> exact bounded dependency on N is retained;
3. shared generation N+1 publishes -> dependent local horizon is revalidated/rebased/discarded before material use;
4. shared candidate N+1 is computed but publication fails -> other contexts still see only successfully published retained basis;
5. multiplayer disabled -> no retained local/shared horizon is active planning in single-player mode;
6. PLAYER deactivated -> their retained local planning cannot be used merely because bytes remain;
7. PC control transfers -> old controller's private planning does not transfer to new controller;
8. Actor intentional state changes -> planning revalidates against Actor owner; planning cannot overwrite Actor cognition;
9. heterogeneous source owners move -> each source is checked under native currentness semantics, not a generic revision vector;
10. planning source disappears under lawful cleanup -> plan invalidates/rebuilds; planning does not retain canonical bytes by fiat;
11. Story missing/stale -> gameplay/recovery still uses native owners;
12. technical publication/ID/generation order differs from fictional order -> chronology remains WP-15-owned;
13. catalog provenance is inspected -> planning semantics trace to current planning owner rather than Story owner;
14. Project Map is read -> Source Manifest does not contradict its current Story routing.

---

## 11. Step-6 gate

```text
STEP_6_BLOCKING:                  1
STEP_6_SIGNIFICANT:               7
UNRESOLVED_BLOCKING_AT_STEP_6:    1
UNRESOLVED_SIGNIFICANT_AT_STEP_6: 7
HUMAN_DECISION_REQUIRED:          NO
UPSTREAM_REOPEN_REQUIRED:         NO
STEP_7_REQUIRED:                  YES
STEP_8_BLOCKED_UNTIL_STEP_7:      YES
```

No implementation, WP-19 or implementation planning is authorized by this review.
