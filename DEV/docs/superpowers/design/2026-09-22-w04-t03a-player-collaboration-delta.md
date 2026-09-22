# W04.T03A PLAYER collaboration delta

Status: **BOUNDED OWNER-LOCAL INPUT — NOT A PHYSICAL PLAYER-SCHEMA PATCH**

Producer: **W04.T03A**

Output:

```text
W04_PLAYER_COLLABORATION_DELTA_READY
```

## Accepted input and write boundary

This delta consumes the accepted W04.T01C checkpoint at
`7b66ac881aa8a60dd6d03bd97d1ab74e1a96da62`. It is limited to the RD16 test
surface and this owner-local delta fixture:

- `DEV/TESTS/test_rd16_world_family_machine_integration.py`;
- `DEV/TESTS/fixtures/w04_player_collaboration_delta.json`.

No physical shared PLAYER schema, collaboration runtime, T07 surface or
Wave-05 final-writer surface is changed by this checkpoint.

## Strict PLAYER collaboration fragment

The bounded `world.player` input fragment requires
`collaboration_route_refs[]`. Each reference contains exactly:

```text
{
  obligation_id: non-empty string,
  generation: positive integer
}
```

Reference objects and the collection are strict. Duplicate exact references
are rejected. Missing, stale or mismatched route references fail closed and
remain repair/recovery evidence rather than an authorization result.

## Authority and fallback boundary

The route references nominate exact scoped obligation/generation identities
only. They do not grant PLAYER membership, controlled-PC authority, input
authority, lifecycle transition, currentness or control transfer. The delta
declares no authorization fallback and specifically excludes:

- `MANIFEST.players.player_ids`;
- generic `PLAYER_INDEX.yaml` lookup.

The collaboration owner source is checked to contain neither fallback. Exact
obligation dereference and owner revalidation remain the authoritative
collaboration path; physical schema integration is deferred to its named
future final writer.

## Verification and version impact

`PlayerCollaborationStrictStateIntegrationTests` covers the strict fragment,
missing/duplicate reference rejection, non-authoritative fields and fallback
absence. The fixture and test are development evidence only and introduce no
runtime module, persistent schema, campaign-contract, storage, catalog or
release namespace.

```text
VERSION_IMPACT: NONE
SYSTEM_IMPACT: NONE
```
