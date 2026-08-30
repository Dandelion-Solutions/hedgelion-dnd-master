# Steps 1–2 Retrospective Assurance — Slice E Integration Resolution

Status: **ASSURED / AMENDED / STEPS 1–2 REMAIN CLOSED**

Target branch: `feature/mechanical-runtime-hot-state`

Task Charter: `2026-08-19-step-1-2-assurance-slice-e-integration-task-charter.md`

Coverage/research: `2026-08-19-step-1-2-assurance-slice-e-integration-coverage-research.md`

Adversarial review: `2026-08-19-step-1-2-assurance-slice-e-integration-adversarial-review.md`

This resolution closes the whole-system integration slice of the Steps 1–2 retrospective assurance pass. It records only integration constraints forced by the already accepted architecture. Exact Step-3 execution schemas remain at their existing human Decision Gate.

## 1. Verdict

The Step-1 catalog/class architecture and Step-2 mechanical-state/evaluation architecture compose without an unresolved ownership blocker after two bounded amendments:

1. procedure-local runtime state receives an independently addressable `runtime.procedure` owner class;
2. Step 3 must materialize compact immutable mechanical-order evidence on every live Effect application whose current arbitration can depend on application recency.

No subsystem is reopened. No generic workflow engine, event-sourced current-state model, global scheduler, per-instance content versioning, or duplicate checkpoint authority is introduced.

Human decision required for Slice E: **NO**.

Confidence: **HIGH**.

## 2. One coherent catalog context remains mandatory

A typed operation, MechanicalContext, Resolution, Continuation, and hydrated live state are interpreted against one coherent `ResolvedCatalogContext`.

Plain `definition_id` does not carry a per-instance version suffix. HDM therefore does not support simultaneously interpreting the same definition ID under two semantic versions inside one active runtime.

The integration rule is:

```text
compatible catalog adoption
    -> existing live state remains valid under the new resolved context

incompatible adoption
    -> explicitly migrate every affected live/durable/checkpointed owner
       OR block/reject adoption
```

An active Effect does not silently “finish under its old definition” after the campaign adopts an incompatible new meaning for the same `definition_id`.

This rule applies to:

- Effect/Condition parameter schemas;
- Resource recovery/capacity semantics;
- Effect arbitration/reapplication semantics;
- owner-local scheduled-trigger declaration keys;
- other live typed state constrained by a reusable definition.

Exact engine/ruleset/package snapshot manifest shape remains Step 6. The logical one-context requirement is already fixed.

## 3. In-flight execution pins catalog context

A RuntimeCommand/Resolution/Continuation must retain the identity/frontier of the resolved catalog context against which it was validated.

An incompatible runtime/catalog adoption cannot silently resume a suspended Continuation under new semantics.

Maintenance must instead do one of the following under later migration/execution rules:

```text
finish/close safely before adoption
migrate the in-flight execution explicitly
block/reject the incompatible adoption
abort under a typed authorized maintenance result
```

The exact transition protocol belongs to Step 3/6. Mixed-context execution is forbidden now.

## 4. `runtime.procedure` is the procedure-local state owner

Step 2 already requires procedure-local Resources to be keyed by a specific procedure identity and shared across several Activity/Resolution invocations, including reaction children and suspension/resumption.

The accepted class-admission rule says an independently addressable operational owner required across execution, retry, suspension, recovery, or audit is a `runtime.*` record.

Therefore the logical class inventory now includes:

```text
runtime.procedure
```

Its narrow responsibility is:

```text
identity/lifetime of one active rules-bearing operational procedure
participant-scoped procedure ResourceState
procedure-local boundary/order state proven necessary by Step 3
status/lifetime epoch
optional world referents such as encounter/scene
```

It does not own:

- one Activity invocation (`runtime.resolution`);
- one player-message plan (`runtime.intent_plan`);
- suspension payload (`runtime.continuation`);
- canonical encounter fiction (`world.encounter`);
- reusable rules definitions;
- Temporal Agenda;
- arbitrary workflow/job semantics.

A `world.encounter` may be a world-facing referent for a Procedure but is not the universal owner of procedure-local operational budgets.

The exact `runtime.procedure` schema/fields are intentionally deferred to the Step-3 execution design. Slice E admits only the class/lifetime owner that Step 2 already requires.

## 5. Procedure state has exactly one mutable authority

For procedure-local ResourceState:

```text
runtime.procedure participant/resource state
    = one current mutable authority

Resolution / Continuation
    = references procedure identity + expected frontier/revisions

checkpoint
    = immutable recovery representation at one frontier
```

A parent Resolution and a reaction child therefore resolve the same Procedure by identity rather than owning separate action/reaction/movement-budget copies.

After an expected child commit, the parent advances/re-pins its frontier and recomputes from the Step-3 safe phase. It does not merge a stale embedded procedure-state snapshot back into the live owner.

## 6. Checkpoints are immutable recovery frontiers, not parallel authorities

A checkpoint may serialize continuity-critical runtime-owner state. That does not create a second mutable owner when the checkpoint has immutable frontier semantics:

```text
live runtime owner
    = current mutable authority

checkpoint F
    = immutable recovery representation of owner state at frontier F
```

As the live environment advances beyond F, the checkpoint remains historical recovery material. On restoration, a selected compatible checkpoint reconstructs new live owner state and authority continues there.

Step 5 owns publication, selection, cleanup, expiry, and multiplayer conflict rules. It may not define heuristic field-level merges between an old checkpoint and newer live authority.

## 7. Live Effect recency must survive trace/event compaction

Effect arbitration may use a registered whole-application policy such as `potency_then_recency`.

Mechanical recency cannot depend on:

- wall-clock timestamps;
- SQL/list ordering;
- lexical/numeric Effect IDs;
- indefinite retention of a creating ResolutionTrace/Event body;
- one local SQLite cache revision as durable campaign chronology.

Therefore Step 3 has a mandatory live-provenance requirement:

> Every nonterminal Effect whose current mechanics may depend on application recency must retain compact immutable mechanical-order evidence for that lifecycle episode until it terminates.

Conceptually:

```text
application_order_key
    allocated/derived at committed Effect creation or replacement
    retry-stable
    mechanically comparable when recency policy requires it
    independent of wall clock and storage order
    preserved across refresh of the same lifecycle episode
    new for create/replace
```

The exact name and encoding remain Step-3 design work. It may be derived from committed ExecutionSegment order plus an intra-segment ordinal or another equivalent stable mechanical ordering token.

A creating MechanicalEvent reference may coexist for audit, but current arbitration correctness may not require retaining the whole old event/trace forever.

## 8. Scheduled-trigger definition migration is explicit

A live Effect may store:

```text
scheduled_trigger_state[key] -> concrete TemporalBinding
```

while its definition owns:

```text
scheduled_triggers[key] -> reusable declaration
```

If an adopted catalog removes, renames, or incompatibly changes a live declaration, migration must explicitly preserve, rename, re-anchor, reset, unarm/cancel, replace/terminate the owner, or reject adoption.

Runtime cannot silently keep an orphan key, silently load the old declaration, or fall back to a generic scheduler.

## 9. Promotion/reference closure follows mechanically required forward references

Before durable publication, a durable live record cannot depend on a local-only typed reference whose target must remain resolvable for current mechanics/integrity.

Closure therefore includes as applicable:

- required `definition_id` dependencies, including session definitions that must be promoted;
- support-parent chains;
- concrete `source_id` when live mechanics/removal/provenance require it;
- separately referenced reusable rules-origin definitions;
- other typed forward references required by the live state contract.

Closure is not a campaign-global provenance crawl. Narrative provenance or an invocation-adjudicated fact does not force promotion merely because it participated in one historical execution.

Derived indexes, DAG nodes, Temporal Agenda entries, and current arbitration winners are never publication-closure authorities.

## 10. Temporal obligations and chronology evidence remain distinct

Current temporal authorities remain:

```text
Effect intrinsic TemporalBinding
Effect scheduled-trigger next-due binding
Resource recovery binding
LifeState recovery binding
procedure/runtime temporal obligation where proven
```

Retained chronology evidence instead records what quantitative passage/order has actually been established for later reasoning.

These are not duplicate clocks. Agenda is rebuilt from active obligations; it does not own or need every chronology fact.

Step 5 may compact chronology evidence only while preserving enough information for materially possible later queries to produce justified `TRUE | FALSE | INDETERMINATE` results and while never deleting evidence required by a live active binding.

## 11. Invocation facts remain execution input, not lore authority

An invocation-adjudicated fact may affect an invocation-sensitive execution and remain fixed causal input/provenance for retry, suspension, receipt, or audit.

It does not become current world truth merely because the execution committed.

State-sensitive Step-2 selectors already exclude `INVOCATION_ADJUDICATED`, preventing ephemeral facts from silently defining persistent Resource capacity, current Condition applicability, HP maximum, Resource recovery, or current Effect duration.

Step 4 may later promote a proposition into durable lore/world truth explicitly. That promotion does not retroactively alter which fact value the historical Resolution used.

## 12. Derived state remains reconstructable

After losing SQLite/index/cache state, runtime can rebuild from source authorities:

- effective Conditions from live Effects + current applicability + definitions;
- Effect arbitration/fallback from target/family + live application parameters/provenance/order evidence;
- support reverse indexes from forward `support_effect_id`;
- Resource capacity/availability from owner state + definitions + engine-state mechanics;
- scoped dependency DAG from registered metadata + concrete bound mechanics;
- Temporal Agenda from authoritative owner-local bindings;
- scheduled-trigger due entries from live Effect state + definition declarations;
- catalog semantics from the compatible resolved catalog context;
- suspended execution from Continuation + Procedure + checkpoint state once Step 3 fixes their exact contract.

A derived cache may be restored as an optimization only after validating its frontier/context. Correctness never depends on retaining it.

## 13. Machine alignment and catalog version

`runtime.procedure` is now admitted to:

- `DEV/CATALOG/core-catalog.json` runtime record kinds;
- `DEV/CATALOG/identifier-policies.json` with stable campaign-scoped sequential identity;
- `DEV/SCHEMAS/identifier-policies.schema.json`.

Focused TDD contract:

- `DEV/TESTS/test_runtime_procedure_class_contract.py`.

The initial RED pass showed only the expected class/policy/schema absence while maintenance audit and all pre-existing tests stayed green. The class-alignment GREEN then passed full validation.

Because `CATALOG_INVENTORY.md` explicitly requires a catalog version change for a new ID, a second RED check required one coherent new catalog version. The four coordinated machine catalogs now use:

```text
catalog_version = 1.3.0
```

while `schema_version` remains unchanged because the catalog envelope schema generation itself did not change.

The version-coherence GREEN passed the full maintenance audit and DEV unit suite.

## 14. Documentation drift classification

`DEV/ARCHITECTURE/MECHANICAL_RUNTIME_PROPOSAL.md` is an older `PROPOSAL / Phase C` artifact and contains pre-Step-2 examples such as generic Effect stacks and engine-owned pseudo-facts that later normative contracts explicitly supersede.

This is **Architecture Documentation Debt**, not live authority. Before implementation planning uses that proposal as a source, it must receive a supersession warning/cleanup against the accepted Activity/Rule Element/Step-2 contracts.

Likewise, any stale prose catalog-version label outside the normative inventory/machine catalogs must be aligned mechanically when touched; it cannot override machine catalog `1.3.0`.

## 15. Step-3 mandatory carry-forward

The saved Step-3 Decision Brief must include:

1. `runtime.procedure` as the one procedure-local operational owner;
2. Resolution/Continuation references to Procedure identity rather than copies of procedure ResourceState;
3. parent/child reaction sharing and re-pin/recompute semantics;
4. compact live Effect `application_order_key`-equivalent provenance;
5. RuntimeCommand/Resolution/Continuation pinning of ResolvedCatalogContext identity;
6. incompatible catalog-adoption barrier/migration semantics for in-flight execution;
7. owner-local scheduled-trigger due execution and atomic `REARM | UNARM | OWNER TERMINAL` handling;
8. explicit invocation-fact values/provenance/missing-input semantics/fingerprinting;
9. checkpointable in-flight state with checkpoints as immutable recovery frontiers.

These constraints do not pre-decide the Step-3 human choices about exact ExecutionSegment/Signal/Event/Continuation ownership and phase ordering.

## 16. Final disposition

Recommendation: **KEEP Steps 1–2 closed with Slice-E amendments.**

No unresolved integration blocker remains in Steps 1–2.

Human decision required: **NO**.

Confidence: **HIGH**.

The next genuine human architecture gate is the preserved Step-3 execution-boundary Decision Gate.
