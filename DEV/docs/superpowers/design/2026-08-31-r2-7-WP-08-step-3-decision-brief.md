# R2.7 WP-08 Step 3 — Decision Brief

Status: **DECISION RECORDED — HUMAN DECISION REQUIRED: NO**

## Decision question

Does WP-08 evidence require a new semantic owner, an architecture/topology change,
a compatibility-policy choice, risk acceptance, scope change, or reopening WP-07
before the existing R2.1–R2.6/Step-4/5 architecture can be mapped to machine
surfaces?

## Evidence basis

- Step-2 canonical-owner evidence E01–E11;
- current instruction/representation evidence S01–S10;
- reverse runtime/catalog/test evidence M01–M09;
- closed WP-07 Step-8/F06 carry-in.

## Established facts

1. One physical conversational context with logical role rebind is accepted law.
2. R2.3 Context Runtime, R2.4 TurnEnvelope/instruction hierarchy and R2.6
   observable containment already own the required semantics.
3. R2.1/R2.2 add source-escalation, Actor-purpose and Actor-private/
   `world.knowledge` constraints; existing Actor/catalog structures align at the
   data-owner layer.
4. CORE cache and activation are useful existing support surfaces, but neither
   turn physical presence into eligibility nor replace a role-local bundle.
5. MechanicalContext/S6D runtime context is a separately owned mechanical
   contract. It must not be promoted to R2.3 role-context authority.
6. F06 remains an implementation obligation under existing R2.6/R2.7 owners.

## Alternatives considered

| Alternative | Disposition | Rationale |
|---|---|---|
| Create a new role/agent/prompt/memory subsystem | REJECTED | Contradicts accepted one-context/logical-role and no-new-authority laws. |
| Treat existing CORE operational prose or mechanical context as complete role-context realization | REJECTED | Evidence proves partial support only; it lacks request/profile/bundle/trace/phase/typed-handoff authority. |
| Map accepted obligations through existing instruction, runtime, catalog and test owners | ADOPTED | Preserves all accepted owners and makes missing realization/verification explicit. |

## Automatically recorded technical decision

WP-08 proceeds with an implementation-facing mapping package under existing
owners, without a new semantic architecture:

- `WP-08/F01` — R2.3 request/profile/discovery/closure/bundle/trace/outcome
  realization mapping;
- `WP-08/F02` — R2.4 TurnEnvelope/registered phase/rebind/minimum-transport
  realization mapping;
- `WP-08/F03` — R2.6 explicit active-role/RoleContextBundle/lawful-handoff
  instruction mapping, discharging WP-07/F06;
- `WP-08/F04` — Narrator/Chronicler/EMISSION_COMMIT protected-output mapping;
- `WP-08/V01` — behavioral containment, lawful-later-use, handoff/rebind,
  degradation and recipient-safe verification mapping.

These are obligations for the remaining Step 4–8 design sequence. They do not
authorize implementation planning or runtime/schema/catalog/CORE changes.

## Human decision required

**NO.** The alternatives are settled by accepted canonical owners and the
observed machine surfaces. No product semantics, authority reassignment,
compatibility policy, risk acceptance or hard scope choice remains.

## Next step

Run Step 4 collaborative review against the decision and evidence.