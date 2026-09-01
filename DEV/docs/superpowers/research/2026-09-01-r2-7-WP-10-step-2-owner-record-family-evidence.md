# R2.7 WP-10 — Step 2 Evidence A: Semantic Owners and Record Families

Status: **STEP-2 EVIDENCE SLICE A — CANONICAL OWNER / NO-RECORD INVENTORY**

## Method and coverage

This evidence slice re-opened all 141 exact paths in the WP-10 Source Manifest
on public ref `b86ebd6e3e9f6dc29b5afa8a961b239d9312e33b` (141 readable; 0 missing). It extracts the semantic
owner inventory from the primary R2.1–R2.6, Step-3–Step-5 and direct architecture
owners, using the global owner matrix only as a derivative completeness check.

Terms:

- **native** means the accepted owner has campaign/current or durable state that
  cannot be replaced by a helper surface;
- **record evidence** names an existing current GAME family only; its presence
  is not proof of semantic adequacy;
- **no native durable record** is used only where primary authority expressly
  makes the concern derived, embedded, ephemeral or runtime-local;
- **unmapped** is evidence of an absent exact current representation, not a
  decision to add a root, schema, topology, migration or bootstrap mechanism.

## Owner-to-family evidence ledger

| Accepted concern / owner | Classification | Current record evidence | Explicit rejection / Step-2 disposition |
|---|---|---|---|
| Engine capability vocabulary | definition/catalog authority, not campaign state | DEV catalog only | no native campaign record; catalog cannot own mutable campaign state |
| Definition identity/content | resolved catalog definition | DEV catalog only | no native campaign record; no same-ID campaign shadow |
| ResolvedCatalogContext | operational selection context | none in GAME family | no native campaign record; not a world entity |
| Campaign identity/routing/runtime and ruleset identity | native durable campaign authority | MANIFEST + manifest schema | mapped; storage/runtime identity only, never world/current frontier |
| Campaign preferences/boundaries | native durable campaign configuration | CONFIG + config schema | mapped; preferences are not ChatGPT memory |
| Campaign card | compact derivative projection | CAMPAIGN_CARD + card schema | mapped as projection only; never gameplay/access/canon authority |
| Current compact campaign routing/chronology frontier | native compact current routing | STATE/CURRENT + current-state schema | mapped; not generic pending state or full scene/entity authority |
| Checkpoint descriptor | optional immutable recovery descriptor | CHECKPOINTS template + checkpoint schema | mapped as descriptor only; not current state/RRC/save authority |
| Campaign semantic occurrence/history | immutable event/history authority | event schema + LOG template | partial machine evidence; append-only event is not current world authority |
| Current natural world entity | kind-specific world owner | WORLD family inferred by MANIFEST, per-kind schemas/templates | root routing exists; adequacy is audited in slice B |
| Actor current mechanics/lifecycle | source `world.actor` | PC and NPC schemas | partial/legacy representation evidence; definitions, caches and scene lists remain non-owners |
| Actor private continuity and directed relationships | source Actor-owned continuity | no exact GAME schema/template family identified | **unmapped**; cannot be merged into knowledge, Story, role context or target Actor |
| Asset current instance state | source `world.asset` | item schema/index template | partial machine evidence; derived possession/access totals are non-owners |
| Effect/condition application | natural effect/application owner | conditions embedded in PC/NPC surfaces | **unmapped** exact natural family; embedded lists do not establish independent effect authority |
| Objective proposition | `world.lore_fact` / natural world owner | lore schema/index template | mapped for lore fact; knowledge/disclosure are distinct |
| Fictional proposition stance | `world.knowledge` subject/fact relation | PC/NPC/faction knowledge fields | **unmapped** distinct owner; PC schema labels its legacy knowledge projection non-authoritative |
| Human material exposure | `runtime.disclosure` relation | no GAME schema/template | **unmapped**; message and PC knowledge are not substitutes |
| Interaction | `runtime.interaction` accepted exchange identity | no exact runtime schema/template | **unmapped**; not session or chat position |
| IntentPlan and embedded clauses | `runtime.intent_plan` | no exact runtime schema/template | **unmapped**; no independent clause record follows from serialization |
| RuntimeCommand | `runtime.command` root closure | no exact runtime schema/template | **unmapped**; command is not Resolution or narration |
| Procedure | `runtime.procedure` local resources/lifecycle | no exact runtime schema/template | **unmapped**; session/checkpoint cannot duplicate it |
| Resolution | `runtime.resolution` accepted activity invocation | no exact runtime schema/template | **unmapped**; not world state or hidden reasoning |
| Continuation | `runtime.continuation` resumable generation | no exact runtime schema/template | **unmapped**; generic session state cannot replace it |
| ExecutionSegment and receipt | embedded execution identity/evidence | no exact runtime schema/template | no independent baseline record; receipt never becomes mutable state |
| Mechanical event | immutable `runtime.mechanical_event` evidence | event schema only (semantic-event) | **unmapped** exact family; semantic event is not mechanical event by name |
| Resolution trace | bounded diagnostic evidence | DEV schema only | no inferred campaign authority; trace excludes hidden CoT |
| Semantic event/causal relation | accepted immutable history/evidence | event schema + LOG template | machine family exists; not total global clock/current state |
| Message / retained exact transcript | `runtime.message` history / contract-bound exactness | no exact GAME schema/template | **unmapped**; message does not imply truth, knowledge or disclosure |
| Temporal obligation / TemporalBinding | native owner-local obligation | temporal-binding DEV schema only | **unmapped** exact GAME family; Agenda is derived routing only |
| Agenda | derived temporal candidate routing | no GAME family required | explicit no native durable record |
| Chronology relation | accepted event/relation evidence | event and current/scene frontier fields | partial machine evidence; ID/log order is not chronology |
| Live current owner state / LiveRoute claim | selected native owner through live source | live-scene schema | partial machine evidence; live source is not mega-owner |
| Dirty/HOT bookkeeping | narrow operational publication state | no exact GAME schema/template | no gameplay owner; physical realization deferred to WP-12 |
| Recovery attempt | ephemeral deterministic operation | no persistent family required | explicit no native durable record |
| Session/handoff coordination | `runtime.session` bounded coordination | SESSIONS template + session schema | mapped only to stated coordination lifecycle; no chat/history/write authority |
| ID allocator | `runtime.id_allocator` campaign allocation state | no exact GAME schema/template | **unmapped**; no chronology/Story identity transfer |
| House Rules/Ruling identity/currentness | campaign policy authority | HOUSE_RULES.md + policy sidecar schema/template | mapped; prose and structured sidecar retain distinct roles |
| Story content and layer projection progress | noncanonical durable projection under source basis | no exact GAME schema/template | **unmapped**; Story never replaces canon/currentness/knowledge |
| Chronicler | generative/editorial role | no record required | explicit no native durable owner |
| Continuity projection | Story/transient derived orientation | no record required | explicit no native durable authority |
| ContextNeedProfile / RoleContextBundle / ContextTrace | registered runtime-local control/diagnostic | DEV schemas/contracts only | explicit WP-09 no durable representation |
| Context indexes/caches | derived helper | no record required | explicit no semantic-owner record |
| HOT/SQLite hydrated copy | physical representation of existing owner | no GAME family requirement | no new owner; WP-12 boundary |
| TurnEnvelope / phase proposals/results | transient typed R2.4 control/proposal | no record required before acceptance | explicit no durable campaign owner |
| Narrator visible output commitment | accepted emission/delivery contract | no exact GAME schema/template | **unmapped** representation; never truth/mechanics/read receipt |
| Collaboration obligation / contribution refs | bounded collaboration lifecycle | no exact GAME schema/template | **unmapped** obligation; contribution remains accepted input/Interaction |
| Player-local/shared Dramaturg horizons | noncanonical planning projection | no exact GAME schema/template | **unmapped**; not canon/chronology/gameplay consequence |
| Host/project/chat memory | host ambient context | none | explicit no campaign authority or record |

## Cross-cutting evidence

1. Existing MANIFEST, CONFIG, CURRENT, CARD, CHECKPOINT, INDEX and SESSION
families each carry narrow invariants. None is a lawful catch-all for an unmapped
owner.
2. Existing PC schema explicitly rejects legacy knowledge/relationship/flattened
mechanics as replacement for the accepted Round-2 owner migration. Existing
NPC/faction knowledge fields likewise do not remove the Step-4 distinction.
3. The only explicit current runtime-local no-record verdicts relevant to this
domain are the WP-09 Context Runtime controls and the R2.4 transient control/
proposal artifacts. Their absence is conforming evidence, not a template gap.
4. The evidence distinguishes logical record-family incompleteness from physical
placement/topology, migration, HOT hydration and bootstrap materialization, which
remain downstream WP-11/12/19/20 concerns.

## Step-2 slice-A findings

- **F10-A1 — current GAME records do not demonstrate an exact native family for
  Actor-private continuity, `world.knowledge`, independent effect/application,
  Step-3 runtime owners, disclosure/message/Story, temporal binding, ID allocation
  or collaboration/Dramaturg owners.** This is a machine-to-architecture coverage
  finding, not a decision to create any particular root/schema.
- **F10-A2 — several existing family names contain non-authoritative legacy or
  projection fields.** They cannot be credited as native-owner satisfaction merely
  because their names resemble the semantic owner.
- **F10-A3 — no semantic conflict or human-owned policy choice is established by
  this slice.** The next slice must test every current schema/template and consumer
  before any Step-3 resolution/canonicalization conclusion.

Next: Step-2 evidence B — all current GAME schema/template families and their
generator/storage consumer route.
