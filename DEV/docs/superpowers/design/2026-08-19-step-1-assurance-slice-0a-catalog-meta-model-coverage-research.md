# Step 1 Retrospective Assurance — Slice 0A Coverage and Research

Status: **ASSURANCE SYNTHESIS — ADVERSARIAL REVIEW PENDING**

Target branch: `feature/mechanical-runtime-hot-state`

Task Charter: `2026-08-19-step-1-assurance-slice-0a-catalog-meta-model-task-charter.md`

## 1. Method

The Task Charter was written before reopening the detailed accepted catalog design. This pass then compared the independently reconstructed requirements against:

- `DEV/ARCHITECTURE/CATALOG_MODEL.md`;
- `DEV/ARCHITECTURE/CATALOG_INVENTORY.md`;
- `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md`;
- `DEV/ARCHITECTURE/CRITICAL_ARCHITECTURE_AUDIT.md`;
- `DEV/CATALOG/core-catalog.json`;
- `DEV/CATALOG/entity-structures.json`;
- universal definition/world schemas and current Step-2 aligned schemas.

Targeted external comparison used current official project documentation for Foundry D&D5e Activities/Active Effects, Foundry PF2e Rule Elements, and Avrae Automation. These are prior art rather than design authorities for HDM.

## 2. Coverage summary

| Requirement family | Coverage | Finding |
|---|---|---|
| closed executable capability vocabulary | FULL | engine registries are closed; LLM/content cannot invent executable IDs |
| reusable validated content separate from executable semantics | FULL | `definition.*` composes registered capabilities |
| world instance identity/state separate from definitions | FULL | universal `world.*` envelope + kind schemas |
| runtime operational records separate from world canon | FULL | inventory and registry classify `runtime.*` separately |
| transient protocol values separate from records | IMPLICIT | class inventory is explicit, but admission/persistence rule should be normative |
| facets/tags separate from mechanics | FULL | repeatedly explicit; prose/tags/details are nonmechanical |
| stable dispatch/validation ownership | FULL | machine catalog + schemas own selectable IDs/shapes |
| campaign extension without Python for ordinary content | FULL | campaign/ruleset definitions compose known capabilities |
| missing capability fails explicitly | FULL | catalog-gap path exists; no arbitrary executable fallback |
| bounded LLM discovery | PARTIAL / owned later | catalog is searchable by definitions/tags/facets, but execution-facing discovery contract is Step 3 |
| progressive materialization | FULL | Actor/world model permits incidental fiction before mechanical materialization |
| local-to-durable promotion | PARTIAL / owned later | identity/promotion rules exist; publication mechanics belong later |
| descriptive metadata cannot become mechanics | FULL | explicit universal contract |
| custom rulesets without universal scripting language | FULL | data extension allowed; new executable semantics require engine work |
| principled class-admission criterion | IMPLICIT | logic exists in several docs but is not one normative decision rule |
| migration consequence of class-boundary changes | PARTIAL / owned later | no silent repurposing; explicit migration required, exact migration protocol later |

## 3. What the current architecture gets right

### 3.1 The fundamental separation is stronger than common VTT prior art

Foundry D&D5e attaches Activities and Active Effects to broad Item-like content containers. PF2e similarly uses Rule Elements on Items spanning feats, class features, equipment, and effects. Avrae exposes a flexible automation tree whose nodes can roll, branch, mutate counters, add initiative effects, and call other automation.

Those systems prove that data-driven composition is practical, but their generic containers are not automatically appropriate for HDM. HDM has a different trust boundary: an LLM is expected to author and map content dynamically. Therefore separating:

```text
closed engine capability
reusable content definition
world instance
runtime record
transient protocol value
```

is not needless taxonomy. It is a safety/determinism boundary preventing a plausible string or JSON object from acquiring executable meaning merely because the LLM emitted it.

### 3.2 Facets are correctly non-executable

The accepted model handles multi-role objects without exclusive inheritance while retaining mechanical authority in typed payload/capabilities. This is preferable to making `asset.weapon`, `actor.swarm`, or similar classifiers silently grant mechanics.

### 3.3 Definitions and instances are correctly separate

The reusable definition/world record split passes the independent identity/lifecycle test across standard cases: one sword, one actor, one active Effect, one placed hazard, and one organization can evolve independently while sharing reusable content.

### 3.4 Runtime state is correctly recognized as non-world but potentially durable

The existence of `runtime.continuation`, `runtime.checkpoint`, `runtime.resolution`, and related records prevents the false dichotomy `not world canon => disposable`. Step 3/5 still own exact persistence, but the meta-model has a valid category for continuity-critical operational state.

## 4. Findings

### 0A-F1 — class/record admission rule is scattered rather than normative

**Severity: MODERATE.**

The accepted documents contain the ingredients of a good admission rule:

- a new definition needs reusable mechanical/semantic identity;
- world state belongs to a particular independent thing;
- embedded values are appropriate when no independent identity/lifecycle is required;
- runtime records are operational owners;
- protocol values normally have no independent identity.

However, the rule is distributed across `CATALOG_MODEL.md`, `CATALOG_INVENTORY.md`, and `CATALOG_CONTRACTS.md`. This makes future catalog growth vulnerable to taxonomy-by-analogy: a new noun may become a `definition.*` or `world.*` merely because a similar noun already has one.

**Required correction:** add one normative class-admission decision rule to `CATALOG_CONTRACTS.md`/inventory:

```text
1. Does it introduce engine-executable semantics?
   -> capability/protocol registry; content cannot invent it.
2. Is it reusable validated content composed from known semantics?
   -> definition.
3. Is it one particular campaign thing/fact with independent identity/lifecycle/provenance?
   -> world record.
4. Is it an independently addressable operational owner needed across execution/retry/recovery?
   -> runtime record.
5. Otherwise, if it exists only inside an owner/request/calculation and has no independent lifecycle/reference need:
   -> embedded typed protocol/value object.
6. Facets/tags classify; they never answer any of the above by themselves.
```

This is a formalization of accepted architecture, not a class-boundary change.

### 0A-F2 — runtime-record versus protocol-value persistence boundary needs one explicit invariant

**Severity: MODERATE.**

`runtime.*` and `value.*` are already separate registries, but the acceptance criterion should state explicitly:

- protocol values do not acquire independent durable identity merely because they are serialized inside a trace/Continuation/checkpoint;
- their owning runtime record owns persistence/versioning/lifecycle;
- if a value later needs independent addressing, retries, references, or lifecycle, promoting it to a runtime record is an architecture change rather than silently assigning it an ID.

Exact runtime schemas remain Step 3 work and do not need to be pulled into Step 1.

### 0A-F3 — reusable hazard versus active Effect/Condition/hazard instance needs a clarification

**Severity: MINOR.**

`definition.hazard` intentionally covers reusable traps, poisons, diseases, curses, and environmental hazards. Runtime state, however, may legitimately be represented differently depending on independent identity/lifecycle:

- placed trap or persistent environmental hazard -> `world.hazard`;
- disease/curse/poison currently affecting an Actor -> Condition/Effect application when that is the actual lifecycle owner;
- consumable poison object -> `world.asset` referencing an asset definition.

The catalog must not imply that every application of a `definition.hazard` materializes `world.hazard`. Clarify that a definition kind does not force a corresponding instance kind; runtime owner follows the concrete lifecycle semantics.

### 0A-F4 — historical/event/world chronology classes require later integration proof, not a Step-1 redesign

**Coverage: DEFERRED_OK, watch in Slice E.**

`runtime.mechanical_event`, `runtime.semantic_event`, `world.timeline_marker`, `world.lore_fact`, and `world.chapter` are intentionally distinct, but their global authority relationship depends on Steps 3–5. The Step-1 meta-model has enough categories to express the separation. Slice E must verify that later contracts do not turn several of them into duplicate historical truth authorities.

## 5. Targeted counterexamples

### Unsupported campaign mechanic

A campaign artifact asks for a mechanic outside all registered operations/selectors. Correct result remains a catalog-gap/unsupported path; adding descriptive prose or a facet cannot make it executable. PASS.

### Improvised chair weapon

The chair remains an Asset; an existing attack/use Activity can bind it as a source. No `definition.improvised_weapon` or new world class is required merely for the temporary role. PASS.

### Session-local NPC later becomes important

A local Actor can be progressively materialized and promoted. Reusable definition creation is optional unless a reusable semantic/mechanical identity is needed. PASS at class boundary; publication details later.

### Continuation survives crash

A Continuation is not world canon but has independent operational identity/lifecycle. `runtime.continuation` is therefore justified. PASS; payload/durability later.

### Disease affecting an actor

If the disease's current mechanics/lifecycle are target-local and independently removable/expiring, an Effect/Condition application is the runtime owner; a reusable hazard definition may be its origin without creating a `world.hazard` duplicate. Current architecture can represent this, but wording should make it explicit.

## 6. Strongest argument against the current meta-model

The strongest alternative is a much smaller model: one generic reusable `Item/Definition`, one generic world `Entity`, and a broad automation payload, following the flexibility demonstrated by Foundry/Avrae.

That design would reduce class count and make novel content authoring easier. It is not recommended for HDM because it shifts semantic dispatch into `type` fields, payload conventions, generic expressions, or runtime code paths inside broad containers. With LLM-authored content, that increases the probability of hidden executable interpretation and weakens compile-time class/ownership validation. HDM benefits more from explicit boundaries than those systems do.

## 7. Recommendation

**KEEP the accepted Step-1 catalog meta-model.**

Apply F1–F3 as normative clarifications, not redesigns. Carry F4 to the whole-system assurance pass.

Human decision required: **NO**.

Recommendation confidence: **HIGH**.

Evidence that would change the recommendation: a real ruleset/campaign case that repeatedly requires new `definition.*`/`world.*` kinds solely because the current five-way classification cannot express independent lifecycle/identity without abusing an existing owner; or proof that LLM discovery cannot work with typed definitions without a generic content container.
