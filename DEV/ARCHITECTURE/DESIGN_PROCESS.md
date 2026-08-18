# HDM Engine Design Process

Status: **AGREED**

## Purpose and scope

Superpowers is a required development-process aid for HDM engine architecture.
It is not part of the game runtime, campaign bootstrap, release package, or
player environment. A campaign must never depend on the plugin being installed.

Product requirements and explicit architecture decisions remain owned by the
project owner. Superpowers governs how alternatives, risks, plans, and reviews
are worked through; it does not decide what HDM should become.

## Architecture gate

Before a new architecture block is accepted:

1. verify that Superpowers is actually available in the current work
   environment; installation history alone is not proof;
2. load and follow the relevant available Superpowers workflow for architecture,
   planning, or critical review;
3. state the block's scope, constraints, alternatives, failure modes, chosen
   minimum design, and exit criteria;
4. run a separate critical pass against the proposed decision before changing
   its status to accepted;
5. record the result and the next exact continuation point in the active
   roadmap/status document.

Only one roadmap stage may be active. Research, evidence gathering, and clearly
labelled drafts may proceed before the gate closes; implementation or later
architecture stages may not silently displace it.

## Unavailable-plugin rule

If Superpowers is not exposed after its connection is verified:

- report the observed limitation instead of claiming the skill was used;
- architecture may remain a draft, but may not be marked accepted merely by
  substituting an undocumented improvised workflow;
- only an explicit project-owner decision, made after the limitation is stated,
  may accept that one block through a documented fallback;
- the exception does not disable the gate for later blocks.

The owner-approved second critical audit recorded in
`CRITICAL_ARCHITECTURE_AUDIT.md` is the initial documented fallback. Step 2 and
later stages must pass this process independently.

## Evidence without bureaucracy

Do not create a workflow object, database row, or schema field for this gate.
One short note in the roadmap or architecture status is sufficient:

- workflow used, or explicit fallback authority;
- review result;
- unresolved items and their owner;
- exit-gate status.

This requirement must not add calls, context, or latency to an HDM gameplay
turn. It applies only to engine architecture and related implementation plans.
