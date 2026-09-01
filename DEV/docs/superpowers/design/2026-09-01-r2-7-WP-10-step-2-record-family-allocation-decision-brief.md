# R2.7 WP-10 — Human Decision Package: Logical Record-Family Allocation

Status: **DECISION ACCEPTED — ALTERNATIVE A; STEP 3 AUTHORIZED**

## Decision scope

This package chooses a *logical* allocation for concerns whose accepted primary
owners require or conditionally require campaign representation. It neither
changes semantic owners nor chooses a path, schema, record encoding, HOT/SQLite
layout, partition topology, migration, template/generator change or bootstrap
sequence.

The reclassification evidence is:
`DEV/docs/superpowers/research/2026-09-01-r2-7-WP-10-step-2-owner-reclassification-correction.md`.

## Non-negotiable boundaries

- `world.knowledge` is one subject/fact stance authority; legacy PC/NPC/faction
  fields cannot become parallel current stores.
- Actor continuity/relationships remain source-Actor-local; no Story, target
  Actor, RoleContextBundle or knowledge merge.
- TemporalBinding remains with its natural temporal owner; Agenda is derived.
- Step-3 lifecycle/evidence owners remain distinct from session, checkpoint,
  semantic event and narration.
- Disclosure, message and Story retain separate delivery/history/projection
  authority. Story never becomes current/canon/recovery authority. Its retained
  source basis is Story-layer provenance only; it is distinct from the runtime-local
  R2.3/WP-09 source basis, which receives no campaign record.
- Collaboration is conditional; Dramaturg horizons are multiplayer-only
  noncanonical projections. WP-09 controls and generic helpers have no record.

## Alternative A — documentation-level logical allocation matrix (recommended)

| Logical family | Concerns mapped |
|---|---|
| Actor-local continuity | retained private continuity and directed relationships |
| Knowledge relation | current `world.knowledge` subject/fact stance |
| Effect/application | independently lifecycled effect/condition application |
| Runtime lifecycle namespace | separate logical members: Interaction, IntentPlan, Command, Procedure, Resolution and Continuation; each retains its own mutation, recovery and lifecycle boundary |
| Runtime immutable-evidence namespace | separate logical members: mechanical event, receipt and bounded trace; each retains its own immutable retention contract |
| History/delivery namespace | separate logical members: semantic event/relation, disclosure and retained message; none is an aggregate or surrogate for another's authority, mutation or retention contract |
| Story projection | Story content and layer progress with its retained Story-layer provenance/source basis only; never the runtime-local R2.3/WP-09 source basis |
| Native temporal component | TemporalBinding embedded with its natural owner; no global family |
| Campaign operations | ID allocator |
| Optional collaboration | active collaboration generation and contribution refs |
| Multiplayer planning projection | local/shared Dramaturg horizons only when multiplayer and present |

The table is a documentation-level allocation matrix. “Namespace” groups several
separate logical record members solely for traceability; it is **not** a new central
registry, runtime service, subsystem or semantic authority. Each member remains
owned, mutated, recovered and retained only under its primary owner contract.

**Advantages:** exact audit vocabulary, mechanically testable non-merge rules and
a direct close for WP-10's owner-to-family question.  
**Cost/risk:** more logical family names and future cross-family integrity
contracts.  
**Failure probes:** knowledge duplicated in Actor records; Continuation stored as
Session; TemporalBinding in Agenda; Story as recovery source; message as
disclosure; inactive collaboration/Dramaturg roots created unconditionally.  
**Downstream:** all physical placement, schemas, HOT, topology, migration and
generator/bootstrap realization.

## Alternative B — strict owner-local aggregates plus two cross-owner relations

Map Actor continuity/relationships and effect applications into their *native
owner-local logical aggregates*; use only a Knowledge relation and a Runtime
lifecycle/evidence namespace as cross-owner families, with separate member
boundaries for every Step-3 owner. Keep semantic event,
disclosure, message and Story as separate history/delivery/projection families;
keep allocator operational; preserve temporal-owner locality and optional
collaboration/Dramaturg rules.

**Advantages:** fewer logical root classes; aligns with owner-local lifecycle.  
**Cost/risk:** aggregate boundaries must be precise enough that Actor-local
continuity/effects are not confused with legacy PC/NPC fields; harder later
cross-owner discovery and integrity checks.  
**Failure probes:** effect copied into every Actor condition list; relationship
made symmetric by aggregate shape; derived index treated as exhaustive proof;
aggregate split accidentally creates two writable stores.  
**Downstream:** same physical decisions as Alternative A; this option does not
authorize embedding in the existing schemas.

## Not an ordinary alternative — defer allocation downstream

A simple deferral leaves WP-10's mandatory exact record-family question
unanswered. It is valid only if the Human Architect explicitly changes the
WP-10 mandate and roadmap, names the receiving owner (at minimum a new bounded
record-family allocation work package before WP-11/12/18/19/20 realization),
defines the safe temporary boundary and accepts that WP-10 cannot otherwise be
closed. No such transfer is proposed by this package.

## Accepted decision

**Human Architect decision: Alternative A accepted.** This records a documentation-level logical allocation matrix only; it does not authorize path, schema, runtime, topology, migration, bootstrap or implementation changes.

## Recommendation and exact question

**Recommendation: Alternative A.** It makes every required/conditional concern
auditable without silently selecting physical implementation.

**Human Architect: choose Alternative A, Alternative B, or explicitly authorize
the mandate/roadmap deferral described above.**
