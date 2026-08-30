# Step 5.0 — Authority / Contamination Audit — Final Resolution

Status: **COMPLETE — OWNER REVIEW CHECKPOINT / STEP 5.1 NOT STARTED**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Full-cycle basis:

- `2026-08-20-step-5-expanded-architecture-agenda.md`
- `../design/2026-08-20-step-5-0-authority-contamination-task-brief.md`
- `../design/2026-08-20-step-5-0-authority-contamination-research-draft.md`
- `../design/2026-08-20-step-5-0-authority-contamination-decision-brief.md`
- `../design/2026-08-20-step-5-0-authority-contamination-candidate-spec.md`
- `../design/2026-08-20-step-5-0-authority-contamination-adversarial-review.md`

This document closes Step 5.0 only. It does not begin or pre-decide Step 5.1.

---

## 1. Final verdict

Step 5.0 found no broad failure in the Steps 1–4 ownership model. It did find a
set of early-project abstractions, duplicate pointers and obsolete storage-path
affordances that could have leaked into later durability, multiplayer and
chronology design.

The accepted cleanup rule is:

> An active machine/template abstraction that appears to own semantics but has
> no surviving accepted independent owner/lifecycle contract is retired before
> later design may depend on it. If a later slice proves a real independent
> identity/lifecycle requirement, it may explicitly re-admit the appropriate
> abstraction through normal catalog evolution.

This rule does **not** remove accepted semantic owners whose durable placement is
merely deferred.

Confidence: **HIGH**.

---

## 2. Retired active abstractions

The following are no longer valid active building blocks:

```text
Standalone Secret storage/schema authority
    GAME/CAMPAIGN/WORLD/SECRETS/
    GAME/SCHEMA/secret.schema.yaml

Untyped tactical storage bucket
    GAME/CAMPAIGN/STATE/TACTICAL/
    scene.tactical_state_path

Generic pending-work bucket
    STATE/CURRENT.pending_global_consequences

Standalone scalar timeline owner
    world.timeline_marker
    transition.timeline_place
    event.timeline.placed

Premature persistence bookkeeping records
    runtime.dirty_record
    runtime.publication_batch
```

Retirement of `runtime.dirty_record` / `runtime.publication_batch` does not remove
runtime dirty bookkeeping or coherent publication transactions as concepts. It
only removes the assumption that either concept already deserves an independently
addressable `runtime.*` record. Step 5.5/5.6 own that proof.

---

## 3. Chronology clarification

The retirement of `world.timeline_marker` is **not** a ban on numeric chronology
values.

Sparse numeric/local ordering remains valid inside an explicit chronology
domain, for example:

```text
430 -> 440 -> 450
```

The retired assumption was that one standalone campaign-global scalar placement
owner should impose order across otherwise independent scenes/events.

Current chronology remains a partial order using causal/after relations, local
scene ordering and optional material time. Step 5.8 supplies multiplayer
concurrency constraints; Step 5.9 owns the final chronology persistence model
and may choose sparse numeric sequence values where useful.

`identifier-policies.json` therefore retains:

```text
timeline_slot = ordering_value_not_identity
```

---

## 4. Checkpoint pointer normalization

The sole latest-checkpoint pointer is now:

```text
MANIFEST.last_checkpoint_id
```

Retired duplicates:

```text
STATE/CURRENT.last_checkpoint_id
CHECKPOINTS/LATEST.yaml
```

Checkpoint records remain immutable recovery-frontier descriptors, not current
state authority. Step 5.7 owns exact path/index lookup, checkpoint validation,
retention and migration.

A checkpoint record and a changed latest-checkpoint pointer must eventually be
published coherently so the pointer cannot expose a missing target; Step 5.7
carries that invariant forward.

---

## 5. Chronology/event routing normalization

Campaign configuration retains:

```text
MANIFEST.world_time.calendar_id
```

Current chronology/recovery routing retains provisionally:

```text
CURRENT.world_time.frontier
CURRENT.last_event_id
```

Removed duplicates:

```text
MANIFEST.world_time.frontier
MANIFEST.last_event_id
```

`CURRENT.last_event_id` is a compact semantic-log/recovery cursor pending later
Step-5 design. It is explicitly not a fictional total-order authority.

---

## 6. Campaign storage path normalization

Current campaign-storage layout is branch-root-relative:

```text
MANIFEST.yaml
STATE/
INDEX/
WORLD/
LOG/
CHECKPOINTS/
LIVE/
```

Current live-state path is:

```text
LIVE/LIVE_STATE.yaml
```

Obsolete campaign-storage wrapper spellings such as
`CAMPAIGN/LIVE/LIVE_STATE.yaml` and `CAMPAIGN/MANIFEST` were removed from active
runtime contracts.

`GAME/CAMPAIGN/` remains legitimate: it is the engine-source template directory.
`GAME/TOOLS/init_campaign.py` copies its **contents** to the new campaign branch
root. This source-template location is not a campaign-storage wrapper.

---

## 7. Preserved accepted owners

Step 5.0 deliberately retains the accepted runtime identities:

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

- Procedure remains sole owner of procedure-local ResourceState;
- Continuation remains one suspended Resolution generation;
- RuntimeCommand remains mandatory descendant closure owner;
- pending-child descriptors retain mandatory post-commit work identity;
- Effect/Resource/LifeState temporal bindings remain authoritative temporal
  obligations;
- Temporal Agenda remains a disposable/rebuildable index;
- `runtime.id_allocator` remains admitted because campaign allocation/promotion
  already requires its independent state.

The absence of a finalized repository placement/enumeration contract for several
of these owners is an intentional later Step-5 problem, not evidence that they
should be collapsed into generic STATE or checkpoint blobs.

---

## 8. Hidden-tail findings resolved during adversarial review

The full cycle found two useful second-order leaks after the initial decision:

1. deleting the empty `WORLD/SECRETS/` template root alone was insufficient
   because `secret.schema.yaml` and the SCHEMA index still advertised a separate
   Secret authority; these were retired too;
2. catalog evolution required updating all coordinated catalog versions and
   closed enumerating schemas/tests, not just JSON registry instances.

The Step-5.0 regression suite protects these cases explicitly.

---

## 9. Catalog result

Closed machine vocabulary advanced coherently:

```text
catalog_version = 1.6.0
```

Coordinated surfaces:

- `DEV/CATALOG/core-catalog.json`
- `DEV/CATALOG/entity-structures.json`
- `DEV/CATALOG/identifier-policies.json`
- `DEV/CATALOG/mechanical-surfaces.json`
- applicable closed JSON schemas
- current normative catalog Markdown

Existing retired IDs were not repurposed.

The Step-4 Chapter-retirement regression test was generalized so it continues to
assert the Step-4 baseline while permitting later coherent catalog versions.

---

## 10. Explicit later-slice carry-forward

Step 5.0 intentionally leaves these questions open for their named owners:

### Step 5.1

- frontier taxonomy and relation;
- current/durable/recovery/live/projection frontier semantics;
- whether `CURRENT.last_event_id` survives the final frontier model.

### Step 5.2 / 5.7

- Resumable Runtime Closure;
- repository placement and cold-start enumeration of active operational owners;
- checkpoint recovery cut/hydration/validation.

### Step 5.3

- complete pending-work inventory;
- temporal Agenda rebuild;
- no-lost/no-double due-work semantics;
- RNG continuity across recovery.

### Step 5.5 / 5.6

- concrete dirty-set representation;
- publication transaction/crash consistency;
- whether independent publication runtime identity is actually required.

### Step 5.8 / 5.9

- multiplayer/live ownership reconciliation;
- cross-scene chronology persistence;
- final ordering-domain model;
- possible sparse numeric local/domain ordering values.

### Step 5.10–5.13

- Story projection durability/catch-up;
- transcript/history retention;
- host delivery/disclosure acknowledgement;
- GC/orphan cleanup frontiers.

No item above is silently answered by Step 5.0 cleanup.

---

## 11. Verification protocol

Step 5.0 used TDD for the active cleanup.

The RED pass introduced `DEV/TESTS/test_step_5_0_contamination.py`; maintenance
audit remained green while the new tests failed on the expected old active
surfaces.

The GREEN cleanup then removed/normalized the approved surfaces and extended the
regression coverage to hidden Secret/schema and root-layout path leaks.

Closure is valid only with a fresh exact-HEAD repository validation proving both:

```text
Run full maintenance audit = success
Run DEV unit tests          = success
```

No Step 5.1 work may begin as part of satisfying this verification gate.

---

## 12. Final gate

After fresh exact-HEAD validation:

```text
Step 5.0 = CLOSED
Step 5.1 = NOT STARTED
next action = owner review of Step-5.0 result
```

No broad implementation planning is authorized by this closure.
