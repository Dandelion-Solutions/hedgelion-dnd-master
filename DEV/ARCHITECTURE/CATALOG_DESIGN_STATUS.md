# HDM Catalog Design Status

Status: **R2.7 ACTIVE — WP-03 CATALOG/CLASS CANONICALIZATION**

This file is a current-status routing index, not a second normative specification.

Process authority:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Current R2.7 execution state:

- `DEV/docs/superpowers/research/2026-08-24-r2-7-audit-status.md`

Current catalog semantics/classification:

- `DEV/ARCHITECTURE/CATALOG_INVENTORY.md`
- `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md`
- `DEV/ARCHITECTURE/CATALOG_RESOLUTION.md`

Machine contracts:

- `DEV/CATALOG/core-catalog.json`
- `DEV/CATALOG/entity-structures.json`
- `DEV/CATALOG/identifier-policies.json`
- `DEV/CATALOG/mechanical-surfaces.json`

---

## Current machine generation

```text
catalog_generation = 2.0.0
release_state = UNRELEASED / R2.7 STRUCTURAL CANONICALIZATION
```

The owner explicitly approved a clean-slate pre-release architecture transition: no real campaign depends on the previous scaffold, so R2.7 does not preserve `1.6.0` compatibility aliases or migration paths.

`2.0.0` is the working final-architecture generation and may receive coordinated changes from later R2.7 owning domains before the final architecture gate closes.

---

## WP-03 structural changes

WP-03 removes stale early machine assumptions and registers accepted later architecture:

- generic `world.relationship` retired; subjective directed relationship state is source-Actor-owned under R2.2;
- `runtime.disclosure` admitted;
- `runtime.collaboration_obligation` admitted as the narrow recoverable R2.5 contribution-collection owner;
- Step-4 objective truth/lore lifecycle/epistemic/disclosure vocabularies registered;
- Step-5 SOFT/HARD shorthand replaced in machine vocabulary by semantic-survival/current-durability/edge-obligation axes;
- Step-5 repository ref outcome vocabulary registered;
- R2.2 Actor-continuity/cognition/relationship facet vocabulary registered;
- R2.3 Context Runtime discovery/representation/outcome vocabulary registered;
- R2.4 logical-role/Story-service and typed gateway values registered;
- R2.5 collaboration/input/planning classifications registered;
- chronology/recovery/Story/message-retention closed vocabularies registered for downstream schemas.

No Story or Dramaturg planning projection is promoted to gameplay/world authority by these registries.

---

## Known downstream machine work

Catalog class completeness does not mean all physical realization is already final.

R2.7 still owns, in later domains:

- WP-04 Actor/Asset state shapes;
- WP-05 execution records;
- WP-07 truth/knowledge/disclosure/message schemas;
- WP-10 durable record-family schemas;
- WP-11 final IDs/roots/sharding/indexing, including source-native identities;
- WP-12 HOT/SQLite;
- WP-14 recovery/checkpoint/session;
- WP-15 chronology persistence;
- WP-16 LIVE identity/currentness/packing;
- WP-17 collaboration schema;
- WP-18 Story/planning projection schemas;
- WP-20 future post-release catalog/schema evolution policy.

Broad runtime behavior implementation remains blocked until R2.7 closes and implementation planning begins.

---

## Retired machine identities remain retired

Current design must not restore as baseline:

- `world.timeline_marker`;
- generic `world.relationship`;
- standalone Secret authority;
- `runtime.dirty_record`;
- `runtime.publication_batch`;
- `runtime.execution_segment`;
- `runtime.resolution_chain`;
- generic pending-work owner;
- generic campaign-wide chronology/frontier owner.

Exact negative regression coverage is expanded during R2.7 and finalized by WP-22.
