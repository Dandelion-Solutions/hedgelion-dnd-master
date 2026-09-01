# R2.7 WP-10 — Step 2 Decision Brief: Logical Record-Family Allocation

Status: **HUMAN ARCHITECT DECISION REQUIRED — STEPS 3–8 BLOCKED**

## Evidence

Step-2 evidence A–C establishes that the accepted semantic owners include
Actor-private continuity, `world.knowledge`, independent effect/application,
Step-3 runtime command/procedure/resolution/continuation/interaction evidence,
disclosure/message/Story, TemporalBinding, ID allocation and collaboration/
Dramaturg concerns. The current GAME schemas/templates provide no exact native
campaign family for those concerns. Existing embedded PC/NPC/faction fields and
MANIFEST/CURRENT/SESSION/CHECKPOINT/LOG/INDEX surfaces explicitly cannot serve as
catch-all replacements.

Primary owners establish the **semantic boundaries**, but do not select the
logical campaign record-family allocation for this group. Selecting it would
create cross-domain interfaces for WP-11/12/18/19/20 and is therefore a human
architecture decision, not a mechanical documentation repair.

## Decision required

Choose the WP-10 disposition:

1. **Allocate bounded logical native record families in WP-10 (recommended).**
   WP-10 would canonically map only the accepted owners that require campaign
   representation to distinct logical record families, while preserving no-record
   verdicts and deferring physical topology, HOT, migration and bootstrap.
2. **Defer the allocation to downstream domains.**
   WP-10 would record the current family gap without a canonical logical mapping.
   This preserves maximum latitude but leaves its required exact
   owner-to-record-family question unresolved.
3. **Authorize a named alternative scope.**
   Specify a different owner-compatible grouping/deferral policy.

## Recommendation

Choose option 1. It directly discharges WP-10 without changing accepted semantic
owners or selecting physical implementation. The subsequent candidate must retain
separate authority for every accepted owner and must not use existing convenience
surfaces as substitutes.

No runtime, schema, catalog, CORE, migration, topology, bootstrap or
implementation-plan change is proposed by this brief.
