# Step 5.0 — Authority / Contamination Decision Brief

Status: **DECISION GATE**

Date: 2026-08-20

Target branch: `feature/mechanical-runtime-hot-state`

Basis:

- `2026-08-20-step-5-0-authority-contamination-task-brief.md`
- `2026-08-20-step-5-0-authority-contamination-research-draft.md`
- Steps 1–4 canonical/assurance contracts
- current active CORE, GAME schemas/templates and catalog `1.5.0`

This brief contains only choices whose consequences are structural enough to merit owner review before mutating active closed vocabulary/template surfaces. Mechanical cleanup already implied by the chosen alternatives will be handled after the gate and then independently adversarially reviewed.

---

# Decision 1 — How should Step 5 treat premature/obsolete active abstractions?

## Problem

The audit found concepts that remain registered or physically copied into campaigns despite lacking a surviving accepted owner contract, including:

- `WORLD/SECRETS/` after Step-4 Secret retirement;
- `STATE/TACTICAL/` + `scene.tactical_state_path` without a typed tactical owner;
- `CURRENT.pending_global_consequences` without lifecycle/identity/idempotency semantics;
- old scalar-slot `world.timeline_marker` + placement transition/event after adoption of partial-order chronology;
- `runtime.dirty_record` and `runtime.publication_batch`, inherited from the early physical SQLite proposal before Step-5 lifecycle/failure analysis.

Leaving them active gives later designers/runtime implementers an apparently valid building block and can silently pre-decide later architecture.

## Alternative A — Leave active, document “do not rely yet”

Pros:

- minimum catalog/template churn;
- preserves every early option;
- later slices can refine in place.

Cons:

- repeats the `world.chapter` failure mode;
- closed catalog registration still advertises legitimacy;
- empty template directories are copied into every new campaign;
- later designers must remember non-machine caveats against machine-visible vocabulary;
- obsolete and merely-undesigned concepts remain indistinguishable.

Assessment: **not recommended**.

## Alternative B — Quarantine but keep IDs/template placeholders

Add strong normative wording that certain IDs/paths are reserved and non-authoritative until later slices close.

Pros:

- less churn than removal;
- explicit warning stronger than status quo.

Cons:

- physical/machine affordance remains;
- runtime/catalog consumers can still discover the IDs;
- creates a special “registered but not actually admitted” state that weakens the closed-vocabulary model.

Assessment: better than A, but structurally awkward.

## Alternative C — Retire proven ownerless/obsolete abstractions now; re-admit only after proof

Principle:

> A catalogued/template abstraction that claims semantic ownership but has no surviving accepted owner contract is removed from the active surface. If a later slice proves independent identity/lifecycle is actually required, it explicitly admits a suitable class/value then.

Apply now to the proven set:

```text
WORLD/SECRETS/                 remove new-campaign placeholder
STATE/TACTICAL/                remove new-campaign placeholder
scene.tactical_state_path      retire
CURRENT.pending_global_consequences
                               retire
world.timeline_marker          retire
transition.timeline_place      retire
event.timeline.placed          retire
runtime.dirty_record           retire
runtime.publication_batch      retire
```

Do **not** remove accepted/real but incompletely placed concepts such as Procedure, Continuation, checkpoint, session, message or id allocator.

Do **not** decide `event_time_advance`, live compaction staging, scene local-fact shape, publication-manifest shape or runtime-record storage placement; assign them to named later slices.

Pros:

- strongest protection against architecture leakage;
- preserves closed-vocabulary meaning: present means admitted;
- later re-admission requires evidence and versioned review;
- mirrors the successful Chapter retirement approach.

Cons:

- catalog version churn if a later slice re-admits a concept;
- future dirty/publication implementation may use a similar name again after proving need;
- requires migration awareness for development-era data/templates.

### Recommendation

**Alternative C.**

Reason: the project has concrete evidence that inactive-but-present abstractions become design premises. Re-admission cost is smaller than allowing a false owner to propagate through Steps 5–6.

Confidence: **HIGH**.

---

# Decision 2 — Which surface owns the latest-checkpoint pointer before 5.7 refines checkpoint protocol?

## Problem

Current active surfaces allow three latest-checkpoint pointers:

```text
MANIFEST.last_checkpoint_id
CURRENT.last_checkpoint_id
CHECKPOINTS/LATEST.yaml
```

This is an actual duplicate writable-pointer problem, not merely redundant display.

Checkpoint content remains an immutable recovery projection and does not become current state regardless of the pointer choice.

## Alternative A — `CHECKPOINTS/LATEST.yaml`

Pros:

- checkpoint-domain locality;
- currently carries both ID and path.

Cons:

- extra mutable file and startup read;
- MANIFEST is already mandatory and STORAGE explicitly refers to MANIFEST checkpoint pointers;
- maintaining path duplicates information that 5.7 can make deterministic/indexed.

Assessment: **not recommended**.

## Alternative B — `CURRENT.last_checkpoint_id`

Pros:

- CURRENT is already recovery/routing-oriented.

Cons:

- latest checkpoint is campaign-level recovery metadata rather than scene/current-world routing;
- duplicates data already expected in mandatory MANIFEST;
- conflicts with current STORAGE wording.

Assessment: **not recommended**.

## Alternative C — `MANIFEST.last_checkpoint_id`

Keep MANIFEST as the sole latest-checkpoint pointer. Retire:

```text
CURRENT.last_checkpoint_id
CHECKPOINTS/LATEST.yaml
```

5.7 later defines exact checkpoint path/index lookup and migration from legacy pointer files.

Pros:

- matches current authoritative STORAGE wording;
- MANIFEST is already read after campaign selection;
- one pointer, no extra mutable projection file;
- does not determine checkpoint payload/frontier design.

Cons:

- MANIFEST remains mutable for recovery routing metadata as well as configuration;
- exact checkpoint path derivation still belongs to 5.7.

### Recommendation

**Alternative C — MANIFEST sole pointer.**

Confidence: **HIGH**.

---

# Derivable cleanup that does not need a separate owner choice if Decisions 1–2 are approved

The following corrections follow from already-accepted contracts:

1. current live path references become `LIVE/LIVE_STATE.yaml`; `CAMPAIGN/LIVE/...` remains only explicit legacy-layout terminology;
2. `MANIFEST.world_time.frontier` is retired because current chronology explicitly assigns the reconciled frontier to `CURRENT.world_time.frontier`; `calendar_id` remains campaign configuration;
3. duplicate `MANIFEST.last_event_id` is retired; `CURRENT.last_event_id` remains only a provisional semantic-log/recovery cursor pending 5.1/5.9 and MUST NOT mean fictional total chronology;
4. live perception/knowledge arrays are explicitly operational/evidence only pending 5.8 compaction alignment;
5. `runtime.session` HEAD fields are session coordination evidence, never branch authority;
6. Dramaturg preparation remains noncanonical regardless of session “retain prep” wording;
7. `runtime.id_allocator` remains admitted because its independent campaign identity/lifecycle is already required by the accepted ID/promotion contract;
8. accepted Step-3 operational owners remain admitted even though storage placement/enumeration is deferred to 5.2/5.7.

---

# Recommendation package

Approve:

```text
Decision 1: C — retire proven ownerless/obsolete active abstractions now
Decision 2: C — MANIFEST.last_checkpoint_id is sole latest-checkpoint pointer
```

Then Step 5.0 proceeds with:

1. Candidate resolution using this authority map;
2. independent adversarial review focused on accidental capability loss and hidden recovery dependencies;
3. resolution gate;
4. only then targeted active cleanup/catalog versioning/TDD as required by the approved design;
5. fresh repository validation;
6. Step-5.0 closure summary;
7. STOP — do not begin Step 5.1 until owner review.

No Step-5 frontier, recovery-image, checkpoint-payload, multiplayer, chronology or Story persistence format is selected by these decisions.
