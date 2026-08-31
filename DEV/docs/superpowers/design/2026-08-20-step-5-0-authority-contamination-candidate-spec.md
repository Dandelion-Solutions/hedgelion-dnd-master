# Step 5.0 — Authority / Contamination Candidate Specification

Status: **CANDIDATE — OWNER DECISIONS ACCEPTED / ADVERSARIAL REVIEW PENDING**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Basis:

- `2026-08-20-step-5-expanded-architecture-agenda.md`
- `2026-08-20-step-5-0-authority-contamination-task-brief.md`
- `2026-08-20-step-5-0-authority-contamination-research-draft.md`
- `2026-08-20-step-5-0-authority-contamination-decision-brief.md`
- owner review of Decisions 1–2 and the timeline-marker clarification

This candidate resolves only Step 5.0. It SHALL NOT define Step 5.1 frontier representation, Step 5.2 recovery serialization, Step 5.8 multiplayer protocol redesign, or Step 5.9 chronology persistence representation.

---

## 1. Accepted contamination rule

An active catalog/template abstraction that appears to own semantics but has no surviving accepted owner/lifecycle contract SHALL be removed from the active architecture rather than left as a machine-visible placeholder.

Re-admission is allowed only when a later design slice proves independent identity/lifecycle or another concrete representation requirement.

Registration means admission. HDM SHALL NOT introduce a special state in which an ID is simultaneously present in the closed catalog and normatively unusable.

---

## 2. Retire now

The following active surfaces are retired by Step 5.0:

```text
WORLD/SECRETS/

STATE/TACTICAL/
scene.tactical_state_path

STATE/CURRENT.pending_global_consequences

world.timeline_marker
transition.timeline_place
event.timeline.placed

runtime.dirty_record
runtime.publication_batch
```

Rationale by class:

- `WORLD/SECRETS/` contradicts the Step-4 decision that Secret is not an independent truth/knowledge authority.
- `STATE/TACTICAL/` and `scene.tactical_state_path` provide an untyped generic storage slot after Step 3 already assigned concrete operational owners. A later tactical persistence owner may be admitted if a real independent lifecycle is proven.
- `pending_global_consequences` is an untyped catch-all that overlaps owner-local temporal obligations, RuntimeCommand pending-child closure, domain world state, and event causality.
- `world.timeline_marker` is retired because its prior unique role was standalone scalar-slot placement authority. Numeric sparse ordering itself is NOT prohibited.
- `runtime.dirty_record` and `runtime.publication_batch` came from the early physical SQLite proposal before Step-5 lifecycle/failure analysis. Dirty bookkeeping and publication transactions remain required concepts, but independent runtime-record identity is not pre-approved.

---

## 3. Timeline-slot clarification

Step 5.0 SHALL NOT prohibit numeric or sparse ordering values.

The following remains valid as a local/domain ordering technique:

```text
430 -> 440 -> 450
```

A numeric key is compatible with partial-order chronology when its ordering domain is explicit and it does not claim an ordering between otherwise independent domains.

The problematic old interpretation is a campaign-global scalar placement authority such as:

```text
A3 = 430
B2 = 440
=> silently asserts A3 < B2
```

when scenes A and B were actually independent and their relative order was undefined.

Therefore:

- retire the standalone `world.timeline_marker` owner and its placement transition/event now;
- retain current event/scene partial-order semantics;
- leave exact chronology persistence representation to Step 5.9;
- allow Step 5.9 to use sparse numeric local/domain sequence values if analysis proves them useful;
- let Step 5.8 multiplayer design supply concurrency constraints that Step 5.9 must respect.

This is a deferred representation question, not a ban on numbers.

---

## 4. Checkpoint pointer authority

The sole latest-checkpoint pointer SHALL be:

```text
MANIFEST.last_checkpoint_id
```

Retire:

```text
STATE/CURRENT.last_checkpoint_id
CHECKPOINTS/LATEST.yaml
```

Checkpoint records remain immutable recovery-frontier descriptors rather than current-state authority.

Step 5.7 owns exact checkpoint path/index lookup, validation, retention and migration. Step 5.0 only removes duplicate writable pointers.

---

## 5. Current chronology and event routing fields

`CURRENT.world_time.frontier` remains the current compact globally reconciled chronology frontier pending Step 5.1/5.9.

Retire from MANIFEST:

```text
MANIFEST.world_time.frontier
MANIFEST.last_event_id
```

Retain:

```text
MANIFEST.world_time.calendar_id
CURRENT.world_time.frontier
CURRENT.last_event_id
```

`CURRENT.last_event_id` is only a provisional semantic-log/recovery cursor pending later Step-5 design. It SHALL NOT be treated as a total fictional chronology authority.

---

## 6. Campaign root-layout cleanup

Current campaign-storage paths are branch-root-relative.

Active CORE/runtime wording SHALL use:

```text
LIVE/LIVE_STATE.yaml
STATE/...
WORLD/...
LOG/...
CHECKPOINTS/...
```

and SHALL NOT describe current campaign storage as `CAMPAIGN/LIVE/...` or another `CAMPAIGN/...` wrapper path.

This does not remove `GAME/CAMPAIGN/` as the engine-source template directory. `GAME/TOOLS/init_campaign.py` legitimately copies the contents of that template directory into the new campaign branch root.

Legacy-layout support may be reintroduced only by an explicit migration/compatibility contract. Step 5.0 does not preserve stale current-doc path aliases merely because an early version used them.

---

## 7. Concepts explicitly preserved

The following are not contamination and remain admitted:

```text
runtime.session
runtime.message
runtime.interaction
runtime.intent_plan
runtime.command
runtime.resolution
runtime.procedure
runtime.continuation
runtime.mechanical_event
runtime.semantic_event
runtime.resolution_trace
runtime.checkpoint
runtime.id_allocator
runtime.maintenance_audit
runtime.catalog_gap_report
```

In particular:

- `runtime.id_allocator` already has accepted independent campaign-scoped state required by allocation/promotion.
- Procedure/Resolution/Continuation/RuntimeCommand have accepted Step-3 ownership even though their durable placement/enumeration remains a Step-5 carry-forward.
- checkpoint identity remains admitted even though checkpoint recovery protocol is not yet fully designed.
- session/message identities remain admitted; later retention/recovery slices may narrow their persistence semantics without treating them as current-world authority.

---

## 8. Deferred, not decided in 5.0

The following must not be silently resolved by cleanup:

- exact dirty-set representation;
- whether publication preparation ever needs an independently addressable durable runtime record;
- publication manifest wire shape;
- runtime operational record storage root/placement;
- cold-start enumeration of active Procedure/Resolution/Continuation/command roots;
- exact recovery-cut/frontier representation;
- `event.event_time.advanced` final role;
- live-scene generic fact/event compaction shapes;
- exact multiplayer chronology constraints;
- global/cross-scene chronology persistence representation;
- Story projection publication/retention;
- transcript retention;
- player disclosure host-delivery acknowledgement.

These belong to later named Step-5 slices.

---

## 9. Catalog evolution

Removing registered world/runtime/transition/event IDs changes the closed vocabulary.

The coordinated machine catalogs SHALL advance from `1.5.0` to `1.6.0`.

All machine catalog files that carry `catalog_version` SHALL remain coherent, and any closed schema that enumerates retired kinds SHALL be updated in the same change.

Existing IDs are retired, not repurposed.

---

## 10. Step-5.0 exit conditions

Step 5.0 may close only after:

1. the listed active placeholders/IDs/pointers are retired;
2. current active CORE/storage wording has no current-layout `CAMPAIGN/...` wrapper leak;
3. one latest-checkpoint pointer remains;
4. current chronology retains partial-order semantics and no accidental total-order requirement is introduced;
5. accepted Step-3 owners remain intact;
6. later-slice questions are explicitly carried forward rather than guessed;
7. adversarial review finds no unresolved material owner decision;
8. full maintenance audit and DEV unit suite pass on the exact final HEAD.

After closure, STOP. Step 5.1 requires an explicit post-5.0 review and SHALL NOT begin automatically.
