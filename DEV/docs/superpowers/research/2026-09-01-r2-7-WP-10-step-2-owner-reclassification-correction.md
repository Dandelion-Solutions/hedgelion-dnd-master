# R2.7 WP-10 — Step 2 Evidence Correction: Owner Reclassification

Status: **STEP-2 EVIDENCE CORRECTION — DECISION PACKAGE INPUT**

The prior inventory's aggregate “unmapped” label was too coarse. This correction
does not change an owner or prescribe a physical representation.

| Concern | Exact owner / primary source | Now-required classification | Logical-family conclusion |
|---|---|---|---|
| Actor private continuity | source Actor; R2.2 | **conditional** when the accepted lifecycle retains it | owner-local Actor continuity component; no target-Actor, knowledge, Story or context surrogate |
| Directed Actor relationships | source Actor relationship view; R2.2 | **conditional** when current relationship state exists | owner-local directed relation component; A→B never implies B→A |
| `world.knowledge` stance | subject/fact relation; Step-4 | **required** whenever a current fictional stance is retained | one logical knowledge-relation family keyed by subject/fact; PC/NPC/faction legacy fields cannot be a second authority |
| Effect/application | natural effect/application owner; Actor/Step-3 contracts | **conditional** when an independently-lifecycled application exists | natural owner-local effect/application component; a copied condition list is projection only |
| Step-3 Interaction/IntentPlan/Command/Procedure/Resolution/Continuation | their distinct runtime owners; Step-3 | **conditional**: admitted accepted lifecycle/evidence exists only when the corresponding execution state/occurrence exists | distinct runtime lifecycle/evidence families; session/checkpoint/event-log cannot merge them |
| Mechanical event / receipt / resolution trace | Step-3 | **conditional** on committed operation / retained diagnostic contract | immutable execution-evidence family; trace excludes hidden reasoning |
| Semantic event / chronology relation | Step-4/Step-5.9 | **conditional** on accepted occurrence/relation | accepted history/relation family; no total-clock or current-state surrogate |
| TemporalBinding | native temporal owner; Step-5.3 | **conditional** on a live temporal obligation | no standalone universal TemporalBinding family: binding remains with its natural owner; Agenda is derived only |
| Disclosure | `runtime.disclosure`; Step-4/5.12 | **conditional** on material committed exposure | delivery/disclosure relation family; message/knowledge/read receipt are prohibited substitutes |
| Message/exact transcript | `runtime.message`; Step-5.11 | **conditional** on accepted retained communication and its retention class | message-history family; exact text only where retention contract requires it |
| Story content/progress | Story layer / projection state; Step-5.10 | **conditional** on retained Story layer | noncanonical projection family with source basis; never canon/currentness/recovery |
| ID allocator | runtime allocator; catalog/Step-5 | **required** once campaign allocates promoted IDs | campaign operational allocator family; no chronology or Story-ID substitution |
| Collaboration obligation | R2.5 | **conditional trigger:** active registered collaboration generation | collaboration family only while an obligation exists; references do not own gameplay consequence |
| Dramaturg horizons | R2.5 | **dormant** in single-player; **conditional multiplayer-only** when the relevant horizon exists | noncanonical local/shared planning-projection family; not Story/canon/chronology |
| RoleContextBundle, ContextTrace, profiles, source basis, estimator | R2.3/R2.4/WP-09 | **explicit no-record** | runtime-local only; never a campaign/session/checkpoint/catalog record |
| Agenda, indexes, caches, HOT/SQLite format, recovery attempt, Chronicler, TurnEnvelope/proposals | their primary owners | **explicit no-record** as independent semantic campaign families | derived, physical or transient only |

All logical-family conclusions leave path, schema, HOT representation, topology,
migration and bootstrap to downstream authorised work.