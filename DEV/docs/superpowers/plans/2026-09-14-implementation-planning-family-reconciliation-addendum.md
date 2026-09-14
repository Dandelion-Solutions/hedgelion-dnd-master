# HDM Implementation Planning — Native Family Reconciliation Addendum

Status: **CURRENT MANDATORY AUTHOR REPAIR — PLANNING / OWNER RECONCILIATION ONLY**
Date: 2026-09-14
Baseline before publication: `a91163f9d503f4e62f05cdcbc9cb864402593301`
Production implementation authorized: **NO**.

This addendum repairs a family-level R018 planning/reconciliation defect discovered by the authority/dependency graph audit. It does not invent new gameplay semantics.

## 1. Finding

**AUTHOR FINDING 8 — SIGNIFICANT.**

WP-11 lists 18 world native physical families. The current S6D semantic catalog admits 15. The exact set difference is:

```text
world.faction
world.player
world.thread
```

`world.thread` is already covered by the mandatory WP-15 thread catalog repair.

The remaining two mismatches have different causes and must not be repaired symmetrically.

### `world.faction` — false independent family

Current semantic owners admit `world.organization`; faction is classification/facet (`organization.faction`). `CATALOG_CONTRACTS.md` explicitly states that facets classify/search only and do not create identity. `ENTITY_STRUCTURES.md` / machine entity structures define `world.organization` and no independent `world.faction` owner.

Therefore WP-11's lower-scope physical row

```text
world.faction -> WORLD/FACTIONS -> INDEX/FACTION_INDEX.yaml
```

cannot create an independent semantic owner without contradicting WP-11's own scope. For v1.0 implementation planning that row is **SUPERSEDED_AS_STALE_PHYSICAL_PROJECTION** by the current semantic owner set.

### `world.player` — accepted later owner missing machine admission

WP-16 canonically requires stable campaign PLAYER identity/binding/control/authorization under `world.player`. Current PLAYER schema and identifier policy already carry much of that contract, but catalog-2.0 `world_record_kinds`, admission ledger, and entity structures do not admit/structure `world.player`.

This is a real machine-alignment debt, not a reason to delete PLAYER.

## 2. Mandatory v1.0 family set consequence

For the relevant rows:

```text
world.organization
  semantic owner: YES
  faction classification: organization.faction facet
  v1 route: WP-11 world.organization route
  separate world.faction record: NO

world.player
  semantic owner: YES (WP-16)
  v1 route: WP-11 WORLD/PLAYERS route law
  discovery index: PLAYER_INDEX remains nomination/discovery only
  authorization authority: PLAYER record after current revalidation

world.thread
  semantic owner: YES (WP-15)
  machine cutover: mandatory Author Finding 4 overlay
```

No other current WP-11 world-family mismatch remains after these three dispositions.

## 3. RD-04 / catalog realization changes

RD-04 remains catalog/routing/identity machine owner and must incorporate the following coordinated v1 actions.

### Remove false faction family realization

Do **not** add or preserve:

```text
world.faction
WORLD/FACTIONS
INDEX/FACTION_INDEX.yaml
GAME/SCHEMA/faction.schema.yaml
```

as v1 native-family authority.

Future implementation may delete/replace legacy `GAME/**` faction artifacts because v1.0 is clean-slate and legacy v0.8 is not a preservation constraint.

Faction organizations use `world.organization` identity/structure/route. A facet filter or higher-level query may classify organizations as factions, but no faction index becomes semantic or absence authority.

### Admit `world.player` coherently

Future coordinated catalog actions:

- `DEV/CATALOG/core-catalog.json`: admit `world.player` in `world_record_kinds`;
- `DEV/CATALOG/catalog-admission-ledger/families/world_record_kinds.json`: add accepted later-owner admission with WP-16 evidence;
- `DEV/CATALOG/entity-structures.json`: add exact `world.player` structure and `definition_binding = forbidden`;
- `DEV/CATALOG/identifier-policies.json`: retain campaign-owned stable PLAYER identity; explicitly forbid LIVE-born PLAYER identity/creation;
- `DEV/ARCHITECTURE/CATALOG_INVENTORY.md` and `DEV/ARCHITECTURE/ENTITY_STRUCTURES.md`: align active projections;
- relevant catalog schemas/conformance tests: require one coherent admission/structure/identity result.

The world-envelope identity is the stable campaign `player_id`. The PLAYER state projection must preserve the accepted WP-16 fields/invariants represented by the current PLAYER contract, including at minimum status, stable external GitHub binding metadata, controlled-PC relations, activation/deactivation semantics, applicable preferences/policy grants, and provenance fields. The exact v1 GAME representation may be rebuilt rather than preserving the legacy wrapper shape.

`world.player` is campaign-only access/control authority and cannot be LIVE-claimed or LIVE-created.

## 4. RD-14 / clean-slate scaffold consequences

RD-14 blank/scaffold generation must not perpetuate legacy faction authority.

Future blank v1 scaffold:

- no authoritative `WORLD/FACTIONS` family root;
- no `FACTION_INDEX.yaml` as a v1 native-family index;
- no `faction.schema.yaml` as a v1 independent world-owner schema;
- includes the v1 `WORLD/PLAYERS` route/root material required by WP-11/WP-16;
- includes `PLAYER_INDEX.yaml` only in its accepted non-authoritative discovery role if retained by the final v1 topology;
- validates the current catalog family set, not legacy directory presence.

No v0.8 compatibility shim/migration is required solely to preserve these legacy GAME surfaces.

## 5. R018 proof repair

Aggregate domain coverage is insufficient. R018 must be checked by concrete family.

Add/strengthen per-family proof so the matrix proves for every accepted family:

```text
semantic owner
-> admitted machine kind OR explicit no-record disposition
-> exact structure
-> identity policy
-> physical route/root
-> owning RD
-> proof
```

Specific cases:

1. `world.organization` + `organization.faction` proves no independent `world.faction` family/root/index/schema survives;
2. `world.player` proves catalog admission + exact structure + campaign identity + WP-11 route + WP-16 authorization owner;
3. `world.thread` proves the separate Author Finding 4 coordinated cutover;
4. runtime family census includes the fixed `runtime.id_allocator` exceptional route and all WP-11 runtime families without omission.

The package must not claim R018 complete from broad `INFO/ACTOR/EXECUTION/...` slice counts alone.

## 6. Version / migration disposition

Planning-only publication Version Impact: **NONE**.

Future v1 implementation must run Version Impact Gate for actual catalog/GAME contract changes. Product-owner constraint is authoritative for this planning block:

```text
GAME/** may be fully rebuilt for v1.0.
legacy v0.8 is not a preservation constraint.
```

Therefore no legacy faction family is retained merely for compatibility.

## 7. Finding disposition

```text
AUTHOR_FINDING_8: SIGNIFICANT
WORLD_FACTION: SUPERSEDED_AS_FALSE_INDEPENDENT_FAMILY
WORLD_PLAYER: COORDINATED_CATALOG_ADMISSION_REQUIRED
WORLD_THREAD: ALREADY_ROUTED_BY_FINDING_4
ARCHITECTURE_REOPEN: NO
HUMAN_DECISION_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
```
