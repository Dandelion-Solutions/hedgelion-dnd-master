# W01.T03 legacy schema retirement — Implementation Impact Brief

## Trigger

`W01.T03` requires retirement of superseded `GAME/SCHEMA/pc.schema.yaml`,
`npc.schema.yaml`, and `item.schema.yaml` after the W01.T02 knowledge cleanup
survives. The exact current tree still has an active maintenance-audit consumer
of `pc.schema.yaml` in `DEV/TOOLS/audit_engine.py`, while that shared final
writer is explicitly deferred to `MAINTENANCE_AUDIT_FINAL_INTEGRATION_READY`.

## Last safe SHA

`214afd28a64216b3f12fde3e517286fd25daaf9f` is the fresh published producer
base. The native Actor/Asset/Effect realization checkpoint that accompanies
this brief leaves all three legacy schema bytes intact.

## Current task

`W01.T03 — Actor, Asset and Effect continuity`

## Approved expectation

W01.T03 owns native Actor/Asset/Effect schemas and continuity admission. It
may retire the three legacy schemas only after the W01.T02 knowledge cleanup is
preserved. Shared documentation and `DEV/TOOLS/audit_engine.py` have one final
writer in Wave 05.

## Evidence and discovered pressure

- W01.T02's `GAME/CORE/INFORMATION.md` explicitly retains the distinction that
  legacy embedded PC/NPC/Faction knowledge arrays are migration input or
  derived convenience, never writable authority.
- `DEV/TESTS/test_rd02_information_native_contracts.py` proves that retained
  knowledge-cleanup law.
- `DEV/TOOLS/audit_engine.py` reads `SCHEMA/pc.schema.yaml` in
  `audit_schema_and_templates()` and requires its legacy player-authorship
  wording.
- `DEV/TESTS/test_s6d_02_catalog_admission_contract.py` also reads the legacy
  PC schema. Its assertion is a stale verification consumer, but the audit
  consumer is a protected deferred shared writer.

Deleting the legacy schemas now would make the required maintenance audit fail.
Repairing that audit consumer changes a deferred shared file outside W01.T03's
allowed write scope.

## Affected owners and protected invariants

- W01.T03 native Actor/Asset/Effect owner-local realization;
- W01.T02 knowledge-cleanup evidence and its prohibition on legacy knowledge
  authority;
- the Wave-05-only maintenance-audit final writer;
- no duplicate entity/knowledge authority and no discarded retained evidence.

## What can proceed without the disputed change

The owner-local continuity tools, strict DEV schemas, strict installed native
schema projections and focused rejection witnesses can be checkpointed. They
explicitly reject legacy/provisional input and preserve the T02 information
evidence. The three legacy schemas remain present only because the active
deferred audit currently consumes one of them.

## Safe options

1. Senior authorizes a narrowly scoped current-consumer repair that removes the
   audit/test dependency before legacy schema retirement; or
2. Wave 05's final shared audit writer performs the consumer reconciliation and
   W01.T03 retirement then resumes from that authorized closure.

## Recommendation

Obtain a Senior ruling on whether the narrowly mechanical audit/test consumer
repair belongs in W01.T03 despite its deferred shared-writer classification.
Do not delete the three legacy schema files before that ruling.

## Cost/risk if wrong

Deleting first leaves the repository's mandatory maintenance audit broken.
Deferring without an explicit disposition leaves superseded schema bytes in the
current tree longer than intended, but does not make them accepted native
authority because the W01.T02 cleanup and W01.T03 admission checks reject that
role.

## Unpublished work

The accompanying local checkpoint is unpublished by task instruction.
