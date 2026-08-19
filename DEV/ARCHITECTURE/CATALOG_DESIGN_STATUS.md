# HDM Catalog Design Status

Status: **STEPS 1–3 CLOSED / STEP 4 IN PROGRESS — FINAL STEP-3 SAME-HEAD CI PENDING**

Target branch: `feature/mechanical-runtime-hot-state`

This file is a current-status index, not a second normative specification.
Detailed reasoning/history lives in the linked architecture/spec documents and
Git history.

Canonical process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`

Sequencing authority:

- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

## 1. Current checkpoint

Steps 1–2 are complete and retrospectively assured.

Step 3 has completed its owner decision, candidate specification, adversarial
review, canonical specification, machine-contract TDD alignment, integrated A–N
cases and final critical review. The final review reports zero unresolved Step-3
blockers.

Step 3 becomes unconditionally closed when `Validate engine source` succeeds on
the final documentation/status HEAD containing this checkpoint.

Step 4 is the sole active numbered architecture stage.

## 2. Current catalog/class baseline

- catalog version: `1.4.0`;
- one coherent `ResolvedCatalogContext` interprets plain definition IDs;
- same-ID shadowing inside one resolved context is invalid;
- incompatible catalog/runtime adoption migrates coherently or blocks;
- `definition_id` compatibility is explicit per `world.*` kind;
- `runtime.procedure` is the independently addressable sole live owner for
  procedure-local participant ResourceState;
- `world.encounter`, `runtime.procedure`, `runtime.resolution`, and
  `runtime.continuation` are distinct lifetimes;
- `ExecutionSegment` and pending child invocation descriptors are protocol values,
  not standalone runtime classes;
- no `runtime.resolution_chain`, scheduler/job class or generic workflow engine is
  part of the accepted baseline.

Normative inventory and machine catalogs:

- `DEV/ARCHITECTURE/CATALOG_INVENTORY.md`
- `DEV/CATALOG/core-catalog.json`
- `DEV/CATALOG/entity-structures.json`
- `DEV/CATALOG/identifier-policies.json`
- `DEV/CATALOG/mechanical-surfaces.json`

## 3. Step-3 canonical execution boundary

Canonical specification:

- `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md`

Final critical review:

- `DEV/docs/superpowers/specs/2026-08-19-step-3-final-critical-review.md`

Machine-contract plan:

- `DEV/docs/superpowers/plans/2026-08-19-step-3-execution-boundary-machine-contract.md`

Current responsibility split:

```text
Interaction
    -> IntentPlan
        -> RuntimeCommand
            -> ActionRequest -> Resolution(Activity)
            OR
            -> TransitionRequest -> direct deterministic execution

RuntimeCommand
    root mandatory execution-chain closure owner

runtime.procedure
    sole procedure-local ResourceState owner

Resolution / direct transition
    -> embedded committed ExecutionSegment(s)
        -> MechanicalEvents
        -> receipts / idempotency
        -> mandatory child invocation descriptors

Continuation
    one suspended Resolution generation
```

### Intent / command

- IntentPlan is finite ordered message-level orchestration, not a transaction;
- earlier committed clauses do not roll back because a later clause fails;
- initial conditional intent uses one narrow forward guard over typed prior-clause
  status/export, not a workflow DSL;
- RuntimeCommand separates action versus already-adjudicated deterministic
  transition paths;
- RuntimeCommand remains `command.accepted` while mechanically mandatory
  descendants/pending work remain open and becomes `command.settled` only at
  closure;
- retry identity compares against stored accepted context/input before ambient
  rebinding.

### Procedure / Resolution / Continuation

- `runtime.procedure` owns participant-local spent ResourceState;
- Resolution means exactly one Activity invocation;
- reaction/trigger child Resolutions reference the same root command and
  Procedure where applicable;
- Continuation references Procedure but cannot copy its ResourceState;
- Continuation preserves fixed RNG, prior typed exports, dependency frontier,
  accepted invocation facts, expected child refs and bounded choice/reaction
  offers;
- derived MechanicalContext/Agenda/DAG/winner caches and trusted prospective
  deltas are not Continuation authority;
- expected child commit causes parent re-pin/re-read/recompute from a safe phase,
  not stale snapshot restoration.

### Segment / Event / trigger

- ExecutionSegment is the smallest local atomic execution-persistence edge and is
  embedded under its owner;
- MechanicalEvent identity is `segment + ordinal` and exists only after commit;
- mandatory post-commit child/firing identity is representable in the same
  committed segment as the triggering Event;
- firing keys make retries idempotent;
- execution-chain safety limits preserve pending mandatory work rather than
  silently truncating it;
- noncommutative simultaneous work requires registered ordering, controller
  choice, or typed order adjudication — never SQL/list order.

### LLM / input authority

- LLM interpretation may choose among bounded candidates and supply only
  explicitly registered fiction-dependent invocation facts;
- invocation facts require explicit boolean value + provenance; missing is not
  false;
- deterministic engine-owned state cannot be supplied as trusted LLM fact;
- RuntimeCommand/Resolution/Continuation retain accepted catalog-context/input
  identity needed for retry/recovery;
- incompatible catalog adoption cannot silently reinterpret suspended execution.

### Effect / temporal integration

- live recency-sensitive Effects may retain positive integer
  `application_order_key` as compact target/application-family-local episode
  evidence;
- recency is not wall time, Effect ID order, SQL order or old trace retention;
- boundary occurrence has stable producer/scope/occurrence identity;
- advancement freezes at reached due coordinate until mandatory same-coordinate
  consequences close or are durably suspended;
- unconsumed requested advancement remains explicit continuation input;
- owner-local scheduled triggers create ordinary child Resolution work; Temporal
  Agenda remains a rebuildable index.

## 4. Current machine evidence

Step-3 schema set now includes:

- `invocation-fact.schema.json`;
- `intent-clause.schema.json`;
- `boundary-occurrence.schema.json`;
- `pending-child-invocation.schema.json`;
- `execution-segment.schema.json`;
- `resolution-receipt.schema.json`;
- `runtime-intent-plan-state.schema.json`;
- `runtime-command-state.schema.json`;
- `runtime-procedure-state.schema.json`;
- `runtime-resolution-state.schema.json`;
- `runtime-continuation-state.schema.json`;
- `runtime-mechanical-event-state.schema.json`.

`world-effect-state.schema.json` also carries the compact
`application_order_key` evidence required by Step-3/Step-2 recency integration.

Focused tests cover the individual ownership contracts plus integrated canonical
cases A–N.

`DEV/TOOLS/audit_engine.py` requires the Step-3 schema set, validates examples,
validates all four machine catalogs, and enforces one coherent catalog version.

## 5. Step-4 active problem

Step 4 owns truth, knowledge/disclosure, narrative projection and minimum durable
promotion.

The central ownership graph to settle is:

```text
objective world/lore truth
    -> who knows / may see it
    -> knowledge-safe LLM context

retained runtime.message transcript
    + committed world/lore/MechanicalEvent sources
        -> runtime.semantic_event
            -> world.chapter
                -> optional public/spectator projection
```

These layers must not become competing truths.

Required Step-4 results include:

1. one authority for objective propositions/truth status;
2. one authority for disclosure/knowledge per subject/player/context;
3. explicit promotion semantics from situational adjudication into durable lore;
4. a SemanticEvent projection contract that compacts history without becoming
   writable current-state authority;
5. a Chapter contract that supports editable literary narration while remaining
   anchored to factual sources;
6. transcript-retention semantics sufficient for dialogue/scene reconstruction
   without making raw chat canonical world truth;
7. spectator/public visibility filtering that prevents secret leakage;
8. knowledge-safe bounded discovery/context for LLM interpretation;
9. promotion closure so durable lore/event/chapter references cannot depend on
   unpublished local entities/definitions.

## 6. Narrative/history layer carry-forward

The intended layering is now explicit but not yet fully specified:

```text
Transcript / runtime.message
    what participants actually said, when retained

MechanicalEvent
    technical committed mechanics fact

SemanticEvent
    compact factual campaign-history projection

Chapter
    human-readable authored narrative/history projection
```

For future spectator use, a viewer-facing ChatGPT should be able to combine a
visibility-safe SemanticEvent spine, selected public transcript and Chapters to
reconstruct the campaign coherently. The private canonical campaign store itself
must not be exposed as the spectator source when it contains restricted facts.

Exact transcript retention, public projection transport and Git publication are
split across Step 4 semantics and Step 5 durability/transport.

## 7. Later-stage ownership

### Step 5

- repository-backed checkpoint publication/restoration;
- SOFT/HARD durability and multiplayer revision/conflict semantics;
- chronology evidence persistence/compaction and cross-scene reconciliation;
- private canonical versus public/spectator Git projection transport;
- transcript/history retention/compaction mechanics;
- checkpoint cleanup/expiry.

### Step 6

- exact engine/ruleset/package/catalog snapshot metadata;
- full D&D seed/migration/catalog-gap closure;
- complete structured selector/input/dependency metadata coverage;
- proven specialized scheduled/simultaneous-order semantics;
- mode isolation and LLM execution budget;
- final holistic architecture/catalog/seed audit.

## 8. Documentation debt

`DEV/ARCHITECTURE/CATALOG_MODEL.md` and
`DEV/ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md` are historical derivation
material containing older examples/version labels. They are not current authority
for IDs/ownership. Current authority is the normative inventory, machine catalogs
and canonical specs. Add/strengthen supersession warnings before implementation
work relies on those historical examples.

## 9. Exact continuation

Proceed with **Step 4 / Lore, Knowledge, Disclosure, Narrative Projection, and
Promotion** using a solution-blind Task Brief and the canonical deep-design
process.
