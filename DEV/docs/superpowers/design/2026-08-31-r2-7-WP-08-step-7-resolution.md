# R2.7 WP-08 Step 7 — Resolution

Status: **RESOLVED — STEP 8 CANONICALIZATION AUTHORIZED; NO HUMAN DECISION REQUIRED**

## Resolution question

Does the repaired Step-5 candidate, after Step-6 adversarial review, preserve the
primary owners and form a complete enough implementation-facing mapping to
canonicalize without choosing a new architecture, compatibility policy, product
semantic or scope?

## Constraint reconciliation

| Obligation | Resolved disposition |
|---|---|
| F01 — R2.3 Context Runtime | `RoleContextRequest`, profile identity, bounded discovery/closure, `RoleContextBundle`, protected trace and finite outcomes remain R2.3-owned runtime-local contracts. No campaign/schema/catalog persistence is admitted. |
| F02 — R2.4 TurnEnvelope/rebind | `TurnEnvelope`, registered phase/result families, phase-local rebind and protected Narrator reservation remain R2.4 runtime control. A phase is not a call, agent or durable record. |
| F03 — R2.6 / WP-07 F06 | The sole primary gameplay **text** owner is `GAME/CORE/AI_REASONING.md`; `PLAY_POLICY.md` owns activation and `RUNTIME.md` owns invocation/turn order without duplicated wording. This is an implementation obligation, not a current CORE edit. |
| R2.1 continuity/history | Derived continuity is orientation/routing only. Material claims escalate to their proper owner; physical visibility never widens eligibility; hidden reasoning and unaccepted material are excluded. |
| R2.2 Actor cognition | Each Actor assessment has an explicit transient purpose and bounded eligible evidence/current state. Admitted Actor-private continuity remains source-Actor-owned and non-epistemic; `world.knowledge` remains exclusive proposition-stance authority. |
| F04 — Chronicler/Narrator/output | No raw private handoff; no same-envelope Story feedback; fresh Narrator rebind and validated recipient-safe `EMISSION_COMMIT` remain mandatory. |
| V01 — verification | Future TDD/evaluation must prove behavioural containment, lawful later uptake, source escalation/exclusion, Actor boundary, rebind/handoff, finite failure and protected output. Existing structural cache/S6D tests alone do not discharge it. |

## Candidate and review disposition

AR-01 through AR-03 are accepted as repaired wording defects. AR-04 through AR-07
pass. No unresolved contradiction remains between the candidate and R2.1–R2.6,
Step-4/5 or current evidence. WP-07 remains closed; F06 is mapped, not reopened.

## Canonicalization decision

**A concise new implementation-facing canonical realization specification is
required.**

Reason: the final package contains a durable design commitment that is not merely
audit evidence — it allocates the sole primary shipped instruction text owner,
activation/invocation separation, runtime-local/no-durable-record boundaries and
the mandatory verification route for the existing R2.3/R2.4/R2.6 laws. Leaving
that accepted mapping only in a research or candidate-design artifact would fail
the repository's `research / design / specs / plans` taxonomy.

The Step-8 specification must be narrowly additive:

- it must cite and preserve the existing semantic owners rather than supersede
  them;
- it must record no code/module naming, schema/catalog change, provider,
  topology, storage or implementation plan;
- it must not copy raw evidence or create a general memory/result-bus authority;
- it must make the F01–F04/V01 realization obligations inspectable for a later,
  separately authorized implementation-planning unit.

## Gate check

**Human decision required: NO.** The source owners mechanically resolve the
allocation. No product semantics, authority transfer, compatibility policy, risk
acceptance or scope choice remains.

## Next step

Create the narrow Step-8 canonical realization specification and its
canonicalization/status/traceability record, then perform required verification
and remote read-back. Do not begin WP-09 or implementation planning.
