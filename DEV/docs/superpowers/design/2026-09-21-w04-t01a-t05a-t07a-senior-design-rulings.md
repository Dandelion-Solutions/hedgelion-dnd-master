# Wave 04 T01A / T05A / T07A — Senior Design Rulings

Status: **ACCEPTED SENIOR SYSTEM-IMPACT RESOLUTION / TARGETED REPAIR AUTHORIZED**

Date: 2026-09-21
Reviewed stop head: `35f979b3e05e10cc759f01361e7271d36941ff4e`

These rulings refine machine realization only. They do not create a new semantic
owner, do not authorize Wave 05, and do not supersede the stable Wave-04 plan.

## 0. Mandatory clean-basis restoration

Fresh GitHub Connector comparison disproved the stop-state claim that the
rejected implementations had been fully restored.

Before any new implementation RED, restore the following paths exactly to
`0bd665860386e04ecd2efb589e58069a4d6da033`, deleting paths that were absent
there:

```text
DEV/SCHEMAS/intent-clause.schema.json
DEV/SCHEMAS/native-history-currentness.schema.json
DEV/SCHEMAS/native-history-publication.schema.json
DEV/SCHEMAS/runtime-collaboration-obligation-state.schema.json
DEV/TESTS/test_rd11_context_runtime.py
DEV/TESTS/test_rd12_collaboration.py
DEV/TESTS/test_rd13_story_t0_commentator.py
GAME/SCHEMA/collaboration_obligation.schema.yaml
GAME/TOOLS/collaboration.py
GAME/TOOLS/context_runtime.py
GAME/TOOLS/history.py
```

Preserve the three System-Impact briefs, this ruling, the Wave-04 execution
cursor and `DEV/CURRENT_PROGRESS.md`.

The restore removes unaccepted bytes; `VERSION_IMPACT: NONE`. Verify baseline,
run local `hdm-reviewer`, publish non-force and read back before new REDs.

---

## 1. SR-W04-T01A — finite collaboration opportunity route

Disposition: **TARGETED_REPAIR_REQUIRED / NO ARCHITECTURE REOPEN**.

### Native opportunity identity

For Wave-04 generation 1 the finite decision-opportunity identity is the
**accepted current collaboration-relevant IntentClause itself**:

```text
DecisionOpportunityIdentity := (interaction_id, clause_id)
runtime.interaction -> runtime.intent_plan -> embedded IntentClause
```

Do not introduce `world.scene.state.coordination_opportunities`, a generic
coordination-opportunity record, a local currentness issuer, a semantic callback,
or caller-selected coordination family.

T01A may machine-realize a finite dependency schema for only the already
accepted R2.5/WP-17 classes:

```text
JOINT_VOLUNTARY_ACTION
SHARED_DECISION_OR_NEGOTIATION
SHARED_SCARCE_RESOURCE_CHOICE
SCENE_CHRONOLOGY_CONVERGENCE
PC_CONSEQUENCE_DECISION
```

Exact spelling may follow repository conventions. No free-form/generic
OWNER_DEFINED class is admitted in generation 1.

The accepted IntentClause may carry immutable interpreted data:

```text
collaboration_semantic_class
normalized_semantics
dependency_kind
purpose
bounded dependency scope
required contributor refs: player_id + optional pc_id
explicit native basis refs required by the dependency kind
```

It may not carry authoritative `coordination_family`, `is_current`,
`positive_material_dependency` or equivalent verdicts.

### Revalidation and classification

Campaign reads use the trusted host-injected `RepositoryPort` plus WP-11
known-ID routes. Reload and validate:

1. exact current campaign pin;
2. exact Interaction;
3. exact IntentPlan + target clause;
4. immutable collaboration/dependency fields;
5. current principal -> exact current PLAYER/control through W03;
6. every required contributor's current PLAYER/PC control;
7. every explicit native basis ref required by the dependency class.

If Procedure/Continuation/Choice/Reaction already owns response/order semantics,
return `RULE_OWNED_ORDERED`; Collaboration does not mirror it.

For `ACTIONABLE_INTENT` held by collaboration, the clause remains
`intent.pending` with no accepted RuntimeCommand before handoff.

After successful validation, `collaboration.py` may issue one **ephemeral
derived admission result**. It owns only Collaboration admission/collection
semantics.

```text
no positive dependency -> INDEPENDENT_IMMEDIATE
positive proved collective dependency -> AGENCY_DEPENDENT_COLLECTIVE
stale/ambiguous/missing required authority -> fail closed
```

Failure to prove independence never creates a collective obligation.

Required negatives include caller-selected family/contributors, caller semantic
booleans/callbacks, stale Interaction/IntentPlan/PLAYER/native basis, and generic
collaboration when a native ordered owner applies.

Fresh Version Impact is mandatory for actual persisted IntentClause/collaboration
contract changes. Prior aborted assessments are non-precedential.

---

## 2. SR-W04-T05A — trusted Context resolution and role/purpose eligibility

Disposition: **TARGETED_REPAIR_REQUIRED / NO ARCHITECTURE REOPEN**.

### Trusted transport

Campaign exact reads use the existing host-injected
`GAME/TOOLS/policy_basis.py::RepositoryPort`.

Do not add a per-request/caller-supplied `exact_load`, validator, semantic
resolver or current/eligible callback.

For selected LIVE state, T05A may realize one narrow **read-only machine
interface** for the already accepted Step-5.8 current-source read/sync law:

```text
selected live source/ref
-> currentness probe when needed
-> exact source revision
-> exact source payload if changed/not already pinned
```

It is transport only. It does not choose the route or return semantic eligibility
verdicts. If a Python interface is needed, own it with the existing LIVE owner;
this is the read counterpart of accepted Step-5.8 transport, not a new owner.

### Bound Context runtime

Realize a host-bound service, conceptually:

```text
BoundContextRuntime(
  repository = trusted RepositoryPort,
  live_reader = trusted read-only LiveSourceRead capability,
  owner_resolver_dispatch = fixed engine code
)

BoundContextRuntime.assemble(RoleContextRequest, discovery_hints)
```

Gameplay requests cannot replace those capabilities.

There is no missing native campaign record saying role/purpose eligible. R2.3,
R2.4, WP08 and WP09 already assign that to:

```text
registered RoleContextRequest
+ registered ContextNeedProfile
+ role / purpose / subject / recipient binding
```

T05A may realize the finite engine-owned profile table/contracts. Current logical
roles remain:

```text
INTERPRETER
DRAMATURG
ACTOR
CHRONICLER
NARRATOR
```

The existing `context-need-profile.schema.json` may be extended where required
to bind the registered role/purpose contract. Callers cannot invent profiles,
channels, role-purpose pairs or broader eligibility.

Before semantic use, fixed engine dispatch resolves candidates through their
native owner:

- PLAYER/control -> W03 access owner + exact PLAYER reload;
- selected LIVE -> route + exact source read + W03 LIVE validation;
- information/knowledge/disclosure -> native owners under recipient/purpose;
- campaign-native record -> RepositoryPort exact path + owner validation;
- unsupported family -> fail closed / registered terminal-degraded Context result.

Only an internal post-resolution object may carry `current=True` /
`eligible=True`; those are never accepted discovery authority.

Required negatives: caller loader replacement, forged flags, semantic callback,
stale PLAYER/LIVE, wrong role/purpose/profile/recipient, index/scene/cache-only
admission, unsupported source family.

Fresh Version Impact is mandatory; prior aborted NONE is non-precedential.

---

## 3. SR-W04-T07A — native history composition root and source adapter

Disposition: **TARGETED_REPAIR_REQUIRED / NO ARCHITECTURE REOPEN**.

The structural `NativeHistoryOwnerPort` must not return.

### Accepted source-domain contract

Step-5.10 plus the 2026-09-08 baseline source contracts already define:

```text
source_domain = campaign.semantic_events@S
lane = evt
candidate = accepted runtime.semantic_event
candidate_id = CID([semantic_event_id])
cursor = evt:<positive admission ordinal>
origin S = LOCAL | LIVE:<native epoch id>
semantic_contract_generation = 1
```

Every accepted SemanticEvent enters its origin-local evt lane once.

The current W01 owner-local `runtime.semantic_event.semantic_order` field is
authorized as the generation-1 machine representation of the positive native
evt **admission ordinal**. It is source-enrollment order only, never fictional
chronology, causal order, Git order or Story order.

### Trusted composition root

Replace:

```text
read_native_history(arbitrary NativeHistoryOwnerPort, ...)
```

with a bound native-history runtime/service created at trusted host composition.

It consumes:

- existing trusted `RepositoryPort` for campaign exact reads;
- the selected-LIVE read capability from SR-W04-T05A for LIVE origins;
- current campaign/LIVE routing;
- a narrow Step-5.10 evt-lane enrollment-window adapter.

That window adapter is an authorized machine realization of the accepted Source
Projection Domain Contract, not a new semantic owner. Per-call callers cannot
replace it.

It returns raw exact source-window evidence only:

```text
campaign_id
origin
exact source revision
lower-exclusive evt ordinal
upper evt basis
bounded ordered event entries / exact event refs
interval-completeness evidence
```

`history.py` validates identity, schema, provenance, origin, revision, ordinal
and interval continuity before issuing accepted history objects.

### Enrollment anchor realization

The accepted source contract explicitly leaves physical native enrollment-anchor
implementation for later realization. T07A/T07B may realize the evt anchors with
the existing SemanticEvent family envelope or an owner-valid compact native
family/source index containing stable event ID, origin, admission ordinal and
exact route/source binding.

It must preserve:

- stable event identity;
- original origin through LIVE absorption;
- positive per-origin ordinal;
- no late insertion behind a valid contiguous cursor;
- exact source/currentness binding;
- bounded interval completeness.

If the required shared physical index/schema is Wave-05-owned, emit a bounded
Wave-05 delta instead of taking over that final writer.

No second history payload store, generic registry, global history sequence,
directory scan or latest-looking selection is authorized.

A `NativeHistoryPublication`, if retained as a runtime type, is ephemeral
evidence over accepted native events, not another persisted history file.

LOCAL evidence binds to accepted W02 campaign publication/currentness; LIVE
evidence binds to exact selected LIVE/CAS authority. Absorption preserves original
LIVE origin and event identity.

Recovery pins the routed source and reads only a bounded evt interval or exact
known refs. If source scope, upper basis or interval completeness cannot be
proved, return UNKNOWN/UNAVAILABLE. Never reconstruct from Story/narration or
fall back from a missing routed LIVE source to campaign.

Required negatives: arbitrary structural source cannot mint history, caller event
list cannot establish coverage, stale/wrong origin/revision, duplicate or
nonmonotonic/noncontiguous anchor evidence where contiguous coverage is claimed,
incomplete upper/scope proof, Story/narration fallback, missing-LIVE campaign
fallback.

Fresh Version Impact starts from restored basis; aborted T07A bumps are
non-precedential.

---

## 4. Resumption

After the mandatory restore checkpoint has local reviewer PASS, publication and
remote read-back:

```text
W04.T01A = AUTHORIZED
W04.T05A = AUTHORIZED
W04.T07A = AUTHORIZED
```

They may execute concurrently under existing write-set rules.

The recorded CLS↔HDM preflight remains PASS unless its explicit semantic-change
trigger fires before T07A RED.

Dependent Wave-04 tasks remain gated by named reviewed producers. Wave 05 remains
unauthorized.

VERSION_IMPACT: NONE for this ruling document.
