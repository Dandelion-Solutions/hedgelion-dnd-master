# R2.7 — Global Semantic Owner Matrix

Status: **IN PROGRESS — WP-02 EVIDENCE ARTIFACT**

Date: 2026-08-24

Purpose: whole-project technical inventory of accepted semantic/operational ownership boundaries. This matrix is **derivative evidence**, not a new authority source. Exact semantics remain in linked owning specifications/contracts.

Primary use:

1. `ARCHITECTURE -> MACHINE` mapping in later R2.7 domains;
2. `MACHINE -> ARCHITECTURE` duplicate-owner/stale-surface audit;
3. implementation-planning derivation after R2.7 closure.

---

## 1. Ownership taxonomy

R2.7 distinguishes four importantly different categories.

### A. Semantic/current authority

Owns a current or durable semantic concern whose competing writable copy would be a correctness defect.

Examples: current Actor HP, current fictional knowledge stance, current Procedure resource state.

### B. Historical/evidence authority

Owns an accepted occurrence/evidence identity for exactly what happened/was communicated/calculated, without becoming current world-state authority.

Examples: MechanicalEvent, runtime.message, semantic event.

### C. Narrow noncanonical/operational authority

Owns its own bounded local lifecycle/progress/control concern but does not own gameplay truth.

Examples: Story layer projection progress, collaboration collection generation, TurnEnvelope control state.

### D. Derived/helper projection

May be persisted or cached, but owns no semantic concern represented from another owner and is rebuildable/replaceable under its contract.

Examples: indexes, Agenda, ContextTrace, MechanicalContext, reverse-reference caches.

Persistence/physical storage alone never promotes C/D into A.

---

## 2. Global accepted owner matrix

| Concern | Accepted owner / owner class | Owned semantics | Explicit non-owned semantics / false authority | Primary accepted source(s) |
|---|---|---|---|---|
| Executable engine vocabulary/capabilities | closed engine capability/protocol registry | legal executable primitives/protocol vocabulary | campaign/LLM may not invent executable semantics | `CATALOG_CONTRACTS.md` |
| Reusable definition identity/content | admitted `definition.*` record in one valid resolved catalog source/context | reusable typed rules/content meaning under stable `definition_id` | not mutable instance state; no same-ID shadow override | `CATALOG_CONTRACTS.md`, `CATALOG_RESOLUTION.md` |
| Resolved catalog selection | selected package/frontier source set composing one logical `ResolvedCatalogContext` | which compatible definition set/capability line is accepted for an operation | not world entity; not mutable gameplay state; no ambient filesystem/search/model authority | `CATALOG_RESOLUTION.md` |
| Particular world entity current state | corresponding natural `world.*` record/owner | kind-specific current mutable world state | definition/catalog, Story, event history, indexes are not parallel writable current state | `CATALOG_CONTRACTS.md` + kind model |
| Actor mechanical/current instance state | source `world.actor` | instance HP/components, life state, resources, placement and admitted mutable actor state | resolved mechanics/cache, archetype, generic resources duplicate HP, scene/condition lists | `ACTOR_MODEL.md` |
| Actor current non-epistemic private continuity | source Actor identity / Actor-owned state | foundation, sparse evolving cognition, transient-private state when retained, directed A->B relationship view | objective truth, `world.knowledge`, target Actor state, PC voluntary mental state | R2.2 canonical |
| Asset current instance state | source `world.asset` | placement/control, quantity, equipment, attunement, resources, durability, access exception | derived possession/access totals, definition properties, event history | `ASSET_MODEL.md` |
| Effect/Condition application current state | corresponding natural Effect/application owner | target-local effect/condition lifecycle and values | copied Actor condition list | Actor/Effect Step-2 contracts; Step-5 integration |
| Objective independently identified proposition | `world.lore_fact` or ordinary natural world owner where proposition identity is unnecessary | objective truth/status for proposition scope | knowledge/belief, disclosure, Story, Narrator prose | Step-4 canonical |
| Current fictional proposition stance | `world.knowledge` keyed by subject/fact | aware/known/believed/suspected/rejected relation + current bounded support | objective truth; human disclosure; duplicate Actor belief store | Step-4 canonical; R2.2 |
| Human player material exposure | `runtime.disclosure` recipient/fact relation | material information committed as exposed to human player | PC knowledge; objective truth; host read receipt | Step-4 canonical; Step 5.12 |
| Accepted external exchange identity | `runtime.interaction` | stable accepted invocation/exchange identity + message/context linkage | world mutation, transaction, Procedure state, host chat position | Step-3 canonical; Step 5.11 |
| Interpreted ordered material clauses | `runtime.intent_plan` for accepted plan semantics | finite ordered interpreted clauses/dispositions from Interaction | transaction/current state; LLM prose alone does not execute | Step-3 canonical |
| Embedded IntentClause / ActionRequest / TransitionRequest | owning IntentPlan/RuntimeCommand protocol context | typed value semantics inside parent | no independent lifecycle/authority merely due serialization | Step-3 canonical; catalog class-admission law |
| Accepted root execution request/closure | `runtime.command` | idempotent root request, accepted input/context identity, mandatory descendant closure disposition | detailed Resolution cursor, Procedure state, narration | Step-3 canonical |
| Rules procedure-local operational state | `runtime.procedure` | independently recoverable procedure-local resources/lifecycle | Resolution, Encounter, checkpoint, session cannot duplicate | Step-3 canonical |
| One Activity invocation state | `runtime.resolution` | accepted bindings, execution status/cursor, fixed RNG, prior exports, child refs, current continuation link | world current state; Procedure resource state; LLM hidden reasoning | Step-3 canonical |
| Suspended Resolution generation | `runtime.continuation` | portable resume generation, fixed inputs/RNG/choices/dependencies/pending response | prior model/chat context; generic session state | Step-3 canonical; Step 5.7 |
| ExecutionSegment | owning Resolution or RuntimeCommand + segment sequence | smallest atomic execution edge as embedded identity | no standalone runtime record/lifecycle in baseline | Step-3 canonical |
| Committed mechanical occurrence evidence | `runtime.mechanical_event` | immutable mechanically relevant committed fact + causal identity | current world state; chronology by ID order | Step-3 canonical |
| Segment/operation Receipt | owning execution record, immutable receipt value | observable/idempotent committed result evidence | copied mutable state authority | Step-3 canonical |
| Diagnostic calculation evidence | `runtime.resolution_trace` | bounded diagnostic/calculation evidence | mechanics authority, hidden CoT, current state | Step-3 canonical |
| Semantic accepted history/causal evidence | `runtime.semantic_event` / LOG semantic history owner | accepted semantic occurrence/provenance according to event contract | current state; total chronology merely by log order | Step-4/5 canonical integration |
| Accepted communication history | `runtime.message` | stable accepted communication evidence identity; exact accepted text while retained; compact provenance after compaction | truth of message proposition; PC knowledge; human exposure by itself; host chat cursor | Step 5.11/5.12 |
| Verbatim historical capability | exact retained message/natural exact owner/verified Transcript under exact contract | exact textual evidence for the exact retained representation | objective truth; reconstruction from hash/model memory | Step 5.11 |
| Native temporal obligation | natural temporal owner carrying its `TemporalBinding`/lifecycle/occurrence contract | existence and state of due/recovery/process obligation | Agenda, global scheduler, chronology `due` flag | Step 5.3 + 5.9 integration |
| Temporal candidate routing | no independent semantic owner; derived Agenda | bounded candidate/due recheck routing | temporal obligation, scheduler authority | Step 5.3/5.7/5.9 |
| Accepted chronology relation/evidence | establishing accepted owner/event or stable typed relation assertion under chronology contract | causal/order/metric relation within declared domain/context | current world state, global clock, temporal obligation, Git/ID order | Step 5.9 |
| Current campaign-domain routing | current campaign authority/native routing contract | selection of current native source(s), live routes, owner partitions | copied native owner state; universal scalar frontier | Step 5.7/5.8/5.14 |
| Live current truth for claimed mutable scope | native semantic owners physically represented through the currently selected live epoch/source | current state for live-claimed owner/partition with exact-source fencing | live file as semantic mega-owner; campaign base as fallback current truth | Step 5.8 |
| Live mutation claim/routing evidence | selected LiveRoute/immutable claim set | bounded write-authority/source routing for epoch | world state, read permission, ACL, chronology | Step 5.8 |
| Campaign durable publication | selected campaign/native ref transition under Step-5.6 protocol | establishment of durable generation/current ref result | prepared Git tree/commit object before accepted ref transition | Step 5.6 + Step 5.14 |
| Dirty/HOT publication bookkeeping | runtime operational representation selected by Step 5.5/implementation | which accepted owner state is unpublished/dirty and pending materialization | independent gameplay semantic owner; `runtime.dirty_record` retired | Step 5.0/5.5/5.6; R2.3 |
| Recovery attempt composition | ephemeral deterministic recovery operation | pinned source composition and validation state for one attempt | universal recovery snapshot/frontier; future authority | Step 5.7 |
| Checkpoint descriptor | optional immutable checkpoint artifact | its own historical/maintenance descriptor/provenance semantics | current state, RRC proof, save success, current route, chronology | Step 5.7 |
| Runtime session/handoff coordination | `runtime.session` within its admitted coordination/lifecycle contract | session/continuation coordination metadata explicitly owned by session contract | write authority, host lease, gameplay truth, generic recovery snapshot | Step 5.0 preserved owner + Step 5.14 negative law; exact machine detail later WP-14/16 |
| Campaign ID allocation | `runtime.id_allocator` | campaign-scoped allocation counters/promotion allocation state | entity semantics/chronology; Story layer IDs | `CATALOG_CONTRACTS.md`, Step 5.0 |
| Story record content | Story layer record | durable noncanonical presentation/history projection content under source basis/availability | canon, current state, knowledge, disclosure, chronology, gameplay recovery | Step-4 + Step 5.10 + R2.1 |
| Story layer projection progress | StoryLayerProjectionState for that layer | layer-local allocator high-water, typed source-domain coverage, required projection-local indexes/order metadata | campaign frontier, gameplay RRC, chronology, source truth | Step 5.10 |
| Chronicler | no durable semantic owner; logical generative/editorial role | proposal/draft transformation only | final Story IDs, coverage, publication, canon | Step 5.10; R2.4 |
| Continuity projection | Story or transient derived continuity under source contract | orientation/routing/prose continuity only | truth/currentness/knowledge/disclosure/exactness/mechanics | R2.1 |
| Context request/need profile | registered consumer/task contract | requiredness, allowed channels, representation floors, finite bounds | campaign truth; LLM cannot enlarge eligibility | R2.3 |
| RoleContextBundle | ephemeral Context Runtime projection | exact bounded role-local execution input for one purpose/basis | durable memory/current truth; omission != absence | R2.3 |
| ContextTrace/dry-run trace | deterministic diagnostic evidence | assembly diagnostics/inclusion/currentness/eligibility reasons | prompt evidence by default; semantic authority | R2.3 |
| Context indexes/caches | derived routing/query structures | bounded discovery/lookup acceleration | presence/absence/current state unless explicit exhaustive owner contract | R2.2/R2.3 |
| HOT/SQLite owner-state working copy | same underlying semantic owner, physically hydrated/current local representation | current ESTABLISHED owner state may be newer than durable Git | SQLite format itself; cache/index/projection tables | R2.3 |
| TurnEnvelope | transient registered control state | legal phase/control binding for one assistant turn | world truth, cognition, Story coverage, disclosure, mechanics | R2.4 |
| InterpreterResult / ActorProposal / PreparationDraft / StoryProjectionDraft / NarrationResult | phase-local typed proposal/result contract until accepted by native deterministic owner | bounded proposed/handoff semantics | canon/state merely by model generation | R2.4 + owning downstream contracts |
| Narrator visible output commitment | deterministic NarrationResult validation + logical EMISSION_COMMIT | commitment of validated player-visible representation to supported host path | truth/mechanics; exact host read receipt | Step 5.12; R2.4/R2.6 |
| Collaboration obligation | bounded collaboration identity/generation | contribution collection/waiting/current generation and accepted contribution refs | gameplay consequence, PC control, chronology, persistence authority | R2.5 |
| Player contribution | accepted Interaction/input owner; collaboration references it | exact accepted player-authored contribution semantics under relevant input class | another player’s PC authority; transcript copy in collaboration | R2.5 |
| Player-local Dramaturg horizon | local noncanonical planning projection | current local planning generation/content/source basis | canon/current state/knowledge/disclosure/Story coverage | R2.5 |
| Shared Dramaturg horizon | multiplayer-only noncanonical shared planning projection | shared planning generation/current planning basis/content | canon, chronology, agency, gameplay consequence, Story | R2.5 |
| Project/chat memory | host ambient context only | host convenience/context assistance | HDM campaign authority/currentness/knowledge/disclosure | R2.6 |

---

## 3. Explicit false-authority matrix

The following equivalences are rejected by accepted architecture.

```text
catalog definition                != mutable entity current state
ResolvedCatalogContext            != world owner
LLM draft/proposal/narration      != accepted mutation/canon
MechanicalEvent                   != current world state
runtime.message                   != truth
runtime.message                   != PC knowledge
runtime.message                   != runtime.disclosure by itself
runtime.disclosure                != PC knowledge
world.knowledge                   != objective truth
Actor private continuity          != world.knowledge
Actor A relationship to B         != B relationship to A
Story                             != canon/current state/recovery authority
Story coverage                    != campaign frontier
Story availability                != disclosure
Dramaturg planning                != future history/canon
collaboration obligation          != gameplay consequence
Context Runtime                   != memory/truth authority
RoleContextBundle                 != durable campaign memory
ContextTrace                      != role evidence by default
index/manifest/search rank        != semantic authority
index omission                    != semantic absence by default
HOT/SQLite format                 != semantic owner
checkpoint                        != current state/RRC/save authority
session metadata                  != write authority/host lease
Temporal Agenda                   != temporal obligation/scheduler
chronology evidence               != global clock/world state
Live source                       != semantic mega-owner
Git ref/commit/ID/time order      != fictional chronology
prepared Git object               != published state
host chat history                 != campaign history/currentness
Retry/Edit/branch/delete          != campaign rewind
Project/chat memory               != campaign authority
cleanup/protection indexes        != target/consumer lifecycle owner
```

---

## 4. Ownership transfer versus physical movement

A recurring architecture law:

> **Physical movement or normalization does not transfer semantic ownership unless an explicit owner/lifecycle transition says it does.**

Examples:

- Actor continuity may be normalized into another table/shard but remains source-Actor-owned.
- Native owner state may be packed into LIVE physical state but live file does not become semantic mega-owner.
- Current owner state may be hydrated in SQLite/HOT and be newer than durable Git without SQLite format becoming authority.
- Definition may move session->campaign while preserving semantic `definition_id` according to explicit promotion contract.
- Live-born accepted owner IDs survive later campaign absorption; absorption moves durability/routing, not identity.
- Story/Transcript may preserve exact communication representation without becoming truth authority.

---

## 5. Acceptance-boundary law

Across the architecture, nondeterministic LLM products remain proposals until an admitted deterministic/semantic owner accepts them.

Canonical pattern:

```text
LLM interpretation / proposal / editorial draft / narration draft
    -> deterministic binding + owner/currentness/eligibility/shape validation
    -> native owner acceptance / publication / EMISSION_COMMIT as applicable
```

This is not one universal transaction type. Each native owner defines the acceptance semantics for its concern.

Important examples:

- IntentPlan interpretation does not execute mechanics.
- ActorProposal does not mutate Actor/`world.knowledge` before deterministic validation.
- PreparationDraft never becomes canon by persistence or repetition.
- Chronicler draft does not advance Story coverage or allocate final Story IDs.
- Narrator generation alone is not outbound/disclosure; Step-5.12 `EMISSION_COMMIT` is required.
- generated repair/recovery prose cannot replace missing native authority.

---

## 6. Known areas requiring later exact machine mapping

This owner matrix intentionally does not pre-decide physical schemas/paths. Later R2.7 domains must map at least:

- exact persistent representation of R2.2 Actor-private continuity and directed relationships;
- exact `world.knowledge`, `runtime.disclosure`, `runtime.message`, Story and planning roots/schemas;
- exact runtime operational owner persistence/hydration for command/procedure/resolution/continuation/session;
- live physical packing while preserving native semantic owners;
- chronology relation evidence representation;
- collaboration obligation and local/shared Dramaturg horizon representation;
- HOT/SQLite owner-state vs derived/cache table separation;
- exact native root/routing structures used by recovery;
- current schemas/templates that still encode retired/duplicate owners.

These are mapping obligations, not permission to alter owner semantics.

---

## 7. WP-02 slice-A conclusion

```text
SLICE: canonical owner inventory + authority taxonomy
RESULT: COMPLETE
KNOWN OWNER-LEVEL CONFLICT: NONE
OWNER_GATE: NONE
NEXT_SLICE: derived/helper/non-owner taxonomy + current machine reverse inventory
```

The next WP-02 slice must inspect actual current machine/runtime surfaces against this matrix. An existing file/table/field receives no authority merely because it exists.