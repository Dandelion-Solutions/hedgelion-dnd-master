# R2.7 WP-11 Step 2 — Canonical Owner Evidence

Status: **EVIDENCE SLICE COMPLETE — NO TOPOLOGY DECISION**

## Scope and source-manifest delta

This slice inspected the WP-11 manifest's governance and canonical-owner
sources, plus the primary Step-5.0--5.14, Step-4 amendment, R2.4, catalog
resolution and machine identity owners reached through those sources. The added
sources are required because their identity, recovery, Story, message, cleanup
or source-currentness rules constrain a physical-route conclusion:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-0-authority-contamination-final.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-1-frontier-model-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md`
- `DEV/docs/superpowers/specs/2026-08-20-step-5-3-temporal-pending-continuity-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-21-step-5-3-5-9-temporal-agenda-chronology-integration-canonical-amendment.md`
- `DEV/docs/superpowers/specs/2026-08-21-step-5-10-story-projection-durability-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-21-step-5-11-transcript-history-retention-compaction-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md`
- `DEV/docs/superpowers/specs/2026-08-23-step-4-single-context-role-containment-canonical-amendment.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-7-whole-project-final-audit-owner-clarification.md`
- `DEV/ARCHITECTURE/CATALOG_RESOLUTION.md`
- `DEV/CATALOG/identifier-policies.json`
- `DEV/CATALOG/entity-structures.json`

## Extracted constraints

| Evidence item | Current disposition for WP-11 |
|---|---|
| Semantic identity | Stable record IDs remain identity across retry, recovery, source movement, compaction and live absorption where their owners require continuity. A path, shard, index entry, ref, commit or enumeration order is routing evidence only. |
| Physical movement | Normalization, sharding, HOT hydration and live packing do not transfer semantic ownership. Source Actor relationships remain directed; native owner state packed into LIVE is not a new mega-owner. |
| Ordinary lookup | Native-owner route discovery and recovery must be bounded. Indexes, Agenda and reverse-protection routes are rebuildable helpers, except that a cleanup operation needs the owner-declared completeness proof before it can rely on protection absence. |
| Chronology | ID order, path order, shard order, commit/ref/CAS order and source enumeration order cannot establish fictional chronology or a global frontier. |
| Index authority | Indexes may route compact discovery but cannot establish writable current state or negative semantic absence without an explicit exhaustive owner contract. Eligibility and disclosure remain checked after routing. |
| Durable evidence families | Interaction, Command, Resolution, Continuation, MechanicalEvent, SemanticEvent and Message retain their separate lifecycles. Receipt, execution segment, intent clause, temporal binding and other embedded protocol values do not acquire independent physical families from serialization. |
| Story and planning | Story has a durable, layer-local, noncanonical projection lifecycle; its existing thousand-sequence grouping is a Story-specific constraint. Context controls and logical role products remain no-record/ephemeral unless a later owner-conforming requirement activates them. Multiplayer Dramaturg remains conditional and noncanonical. |
| Message retention | Message identity survives compaction and source movement. Any physical mapping must preserve required interaction/idempotency, source-enumeration, provenance, disclosure, live-identity and exact-certification survivor references before retirement. |
| Currentness and recovery | Campaign routing selects current native sources; checkpoints, prepared objects, session metadata and indexes do not supersede them. Recovery starts from current routing, pins exact compatible sources, then rebuilds derived routing/cache state. |
| Live state | The selected live epoch has a physically separate operational partition and exact-source fence for its claimed scope. Its route, branch presence and source revision do not make it a semantic owner or chronology source; `CLOSED_UNABSORBED` remains current truth with no ordinary writer. |
| Catalog identity | A `definition_id` resolves under exactly one `ResolvedCatalogContext`; package/snapshot identity, not an ambient search, catalog version or physical location, supplies compatibility. |

## Enumerated-family allocation check

The WP-10 logical members were classified against their accepted owners before
any route selection. `world.*` current state and source-native runtime/evidence
records require a physical-family disposition; embedded values do not. Knowledge
and disclosure use semantic composite keys but have no preselected physical
family. Story has its own noncanonical projection family; Context Runtime has no
campaign record. These are allocation facts, not a topology selection.

## Decision-gate check

No source creates a product, semantic-authority, compatibility or risk-acceptance
decision. The remaining physical route and shard choices are the delegated WP-11
mapping task and remain subject to the later current-machine and consumer slices.
