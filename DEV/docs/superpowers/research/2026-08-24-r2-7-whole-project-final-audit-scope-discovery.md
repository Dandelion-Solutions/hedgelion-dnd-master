# R2.7 — Whole-Project Final Architecture Audit — Scope Discovery

Status: **RESEARCH / SCOPE DISCOVERY — PRE-BRIEF SYNTHESIS**

Date: 2026-08-24

Purpose:

> Determine the complete question set that must be answered before HDM may leave architecture and enter implementation planning.

This artifact corrects an overly narrow initial framing of R2.7 as primarily a Round-2 machine-realization pass. R2.7 is the final architecture gate before implementation planning; therefore its audit scope must cover the **whole accepted HDM architecture and its current machine/runtime realization surfaces**, not only the external-idea/Round-2 delta.

No implementation is authorized here.

---

# 1. Scope conclusion

The final audit must reconcile three complete layers:

```text
ALL ACCEPTED ARCHITECTURE
    Round 1 / Steps 1-5
    + later amendments / owner decisions
    + Round 2 / R2.1-R2.6

CURRENT MACHINE / RUNTIME SURFACES
    GAME/CORE
    GAME/SCHEMA + GAME/CAMPAIGN templates
    GAME/INSTALL + RULES + MIGRATIONS + TOOLS
    DEV/ARCHITECTURE + DEV/CATALOG + DEV/SCHEMAS
    DEV/TESTS + DEV/TOOLS + DEV/RELEASE + CI

IMPLEMENTATION-PLANNING READINESS
    exact ownership
    exact representation/path/interface destinations
    migration/bootstrap/release consequences
    test/evaluation obligations
    no unresolved architecture blocker
```

Round-2 DIAMOND/STRONG accounting remains one required sub-ledger. It is not the coverage boundary of the final audit.

---

# 2. Source-manifest families for the audit

The audit Source Manifest must include and reconcile, by dependency rather than by filename chronology:

1. **Process and sequencing owners** — `AGENTS.md`, design-process files, project map, current roadmap.
2. **Round-1 semantic owners** — Steps 1-5 owning canonical specs, owner decisions, amendments, model contracts, final assurance/review artifacts.
3. **Round-2 semantic owners** — R2.1-R2.6 canonical specs/gates/owner decisions plus active/dormant evidence dispositions.
4. **Durable architecture/model contracts** — catalog, Actor, Asset, Activity, Rule Element, access, branch/storage and other current DEV architecture owners.
5. **Shipped runtime contracts** — all implicated `GAME/CORE/*.md`, with `CORE_INDEX.md` used only as routing.
6. **Persistent/interchange machine contracts** — all implicated `GAME/SCHEMA/*.schema.yaml`, campaign templates, index templates, rule/local-storage templates.
7. **Development machine contracts** — `DEV/CATALOG/*.json`, `DEV/SCHEMAS/*.schema.json`, identifier/mechanical-surface policies.
8. **Bootstrap/update/migration surfaces** — install instructions, Project Instructions, bootstrap runtime, campaign generator, engine update/migration contracts.
9. **Persistence/recovery/concurrency surfaces** — storage, publication, save, session, live, chronology, integrity, maintenance support.
10. **Verification surfaces** — executable tests, scenario/adversarial catalogs, maintenance audit, CI validation, release builder/checklist.
11. **Release/version/legal boundary** — GAME/DEV package split, version metadata, runtime package builder, release workflow and required legal copies.
12. **Research/evaluation evidence only where still relevant** — role-containment evidence, R2.6 acceptance inventory, retained dormant/revisit triggers. Research does not override owners.

The root README is not an automatic audit/edit target; only exact inaccuracies are reported unless the owner separately authorizes edits.

---

# 3. Whole-project audit question inventory

The following domains define the required audit horizon. Each must end with `SATISFIED`, `GAP`, `CONFLICT`, `DEFERRED_WITH_SAFE_TRIGGER`, or `OUT_OF_SCOPE_BY_OWNER_DECISION` at the architecture/mapping level.

## WP-01 — Product/deployment and repository boundary

Questions:

- Is the supported MVP product profile consistent across architecture, runtime and install instructions?
- Is `GAME/` the complete shipped runtime dependency set, with no correctness dependency on `DEV/`?
- Are public-HDМ vs private-Lab responsibilities unambiguous?
- Are forbidden transport/tool fallbacks stated consistently wherever runtime/bootstrap can trigger repository work?
- Are host assumptions classified as semantic requirements, deployment prerequisites or post-MVP evaluation concerns rather than mixed together?

## WP-02 — Global authority / duplicate-owner audit

Questions:

- Does every mutable/current semantic concern have exactly one authority?
- Are definition/catalog, instance/current state, derived views, indexes/caches, Story/planning and session metadata clearly separated?
- Can any YAML/JSON, SQLite table, index, chat history, Story record, checkpoint or preparation artifact accidentally become a second owner?
- Are deterministic acceptance boundaries distinguished from LLM interpretation/proposal/narration everywhere?

## WP-03 — Catalog/class/capability completeness

Questions:

- Do current catalog classes and machine IDs cover all accepted entity/definition/runtime categories from Steps 1-3 and later consumers?
- Are class admission, definition binding, capabilities and protocol vocabulary consistent between prose contracts, `DEV/CATALOG`, schemas and runtime consumers?
- Are obsolete/superseded classes or fields still referenced anywhere?
- Is extension capability bounded without accidental provider/plugin architecture creep?

## WP-04 — Actor / Asset / mechanical-state model

Questions:

- Are Actor/Asset current-state owners and archetype/instance boundaries consistent across architecture, machine schemas and GAME persistent records?
- Can resources, HP/health, effects, conditions, durations, life-state/recovery and related mechanical state be represented without duplicate ownership?
- Are selector/query/recovery semantics machine-realizable from current records?
- Are R2.2 cognition/relationship additions integrated without duplicating `world.knowledge` or player-owned PC mental state?

## WP-05 — Deterministic execution pipeline

Questions:

- Is the complete accepted chain from Interaction/IntentPlan through RuntimeCommand, Resolution/direct transition, ExecutionSegment, events/receipts, Procedure/Continuation and owner mutations represented?
- Are identity, idempotency, retry and fixed-RNG laws implementable from persisted/operational data rather than hidden model state?
- Do current `RUNTIME`, `MECHANICS_INTEGRITY`, `RANDOMNESS`, activity/rule-element contracts and DEV schemas agree?
- Can any domain CORE module narrate a material mechanic without the accepted execution proof path?

## WP-06 — Rules, adjudication and domain-module compatibility

Questions:

- Do combat, magic, exploration, dialogue, encounters, advancement, rewards and other gameplay modules route material mechanics through the deterministic model?
- Are quick rulings/source research policies consistent with rules-source and character-readiness contracts?
- Does any domain module invent persistent state, chronology, knowledge or authority outside its owning model?
- Are house rules/local rulings represented and routed consistently?

## WP-07 — Truth, knowledge, disclosure and communication evidence

Questions:

- Are objective truth, fictional knowledge, human disclosure, accepted message evidence, Story and planning mechanically distinct?
- Does every required durable/operational owner have a representation or an explicit `NO DURABLE RECORD` result?
- Are lawful transfer/update semantics representable without copying knowledge into Actor/live/session records?
- Are exact-history/Transcript semantics and compaction limits preserved?

## WP-08 — LLM role/context/instruction architecture

Questions:

- Are Interpreter/Dramaturg/Actor/Chronicler/Narrator/Commentator logical responsibilities mapped without persisting hidden chain-of-thought?
- Are `RoleContextRequest`, discovery/packet closure, `RoleContextBundle`, `ContextTrace`, degradation outcomes and minimal handoffs mapped to concrete deterministic support surfaces where needed?
- Is the behavioral rule `ineligible now -> do not materially use/disclose; lawfully eligible later -> may use normally` owned once and applied consistently?
- Do CORE activation and Project Instructions implement one-context role rebinding without creating a giant duplicated prompt or unsafe role inheritance?

## WP-09 — Context loading, retrieval and resource-bounded operation

Questions:

- Can current records/indexes support bounded discovery before full load for every relevant domain?
- Are required packet floors, optional degradation and `UNSATISFIABLE` representable without exact hidden token telemetry?
- Are there any hidden campaign-wide scans in normal hot paths?
- Are scene/location/current indexes sufficient as routing hints without becoming closed-world authority?
- Are context/resource assumptions compatible with the supported ChatGPT profile?

## WP-10 — Durable campaign record-family completeness

Questions:

- Does every accepted durable/current semantic owner map to an exact native record family/root/schema, or explicitly to no native durable record?
- Are current campaign template families sufficient for all Steps 1-5 and Round-2 requirements?
- Which existing scaffold roots are historical/insufficient and require replacement/addition?
- Do manifest/config/current/session/checkpoint/event/world records contain only responsibilities they actually own?

## WP-11 — Physical storage topology, identity and indexing

Questions:

- Which record families are flat vs deterministically sharded across the **entire project**, not only Round-2 additions?
- What exact shard arithmetic/routing applies to every high-cardinality family?
- Are stable IDs semantic identity while paths remain routing only?
- Does every lookup path compose with monolithic `*_INDEX.yaml` without large-directory enumeration?
- Are index contents bounded, non-secret-bearing where required, rebuildable and non-authoritative?
- Are known GitHub directory/API constraints accounted for in every potentially large family?

## WP-12 — HOT / SQLite / transaction realization

Questions:

- Which semantic-owner states may have a newer HOT copy than the durable Git frontier?
- Which SQLite structures are owner-state working copies vs derived indexes/caches/projections?
- How are hydration, dirty tracking, transaction boundaries, publication sets, currentness/CAS metadata and recovery represented?
- What may be lost after crash, what is rebuilt, and what native record receives durable materialization?
- Is there any SQLite-only durable canon or duplicate owner?

## WP-13 — Durability edges, SAVE and publication

Questions:

- Are SOFT/HARD/named durability-edge semantics mapped for all owners?
- Can `SAVE_ALL_DIRTY` discover/materialize the complete required closure?
- Does campaign publication preserve Python/core-prepared complete-delta + Connector Git-data/ref CAS semantics?
- Are ambiguous ACK, stale ref, conflict and retry outcomes finite and non-replaying?
- Can any per-record or convenience write bypass atomic publication requirements?

## WP-14 — Recovery, checkpoints, session handoff and repair

Questions:

- Can a fresh process reconstruct the required runtime closure entirely from current authoritative sources?
- Are checkpoints optional accelerators/evidence rather than authority?
- Are session/handoff records coordination-only and safely discardable/reconstructable where required?
- Are corruption/suspect-canon repair paths bounded and authority-preserving?
- Are maintenance/export/reset commands consistent with accepted recovery and access laws?

## WP-15 — Temporal owners, processes and chronology

Questions:

- Does every temporal obligation/occurrence live with a native owner rather than a generic scheduler?
- Is Agenda/candidate routing rebuildable and non-authoritative?
- Are domain-typed order and metric chronology representable without a global world clock/frontier?
- Can processes/clocks/off-screen change and split-scene progress compose with the chronology model?
- Can Git/ref/host/message/ID order accidentally leak into fictional chronology anywhere?

## WP-16 — Multiplayer, access control and live state

Questions:

- Are authenticated participant identity, PLAYER binding, controlled-PC authority, membership and permissions represented consistently across access, schema, bootstrap and runtime?
- Does LIVE own only its selected shared actionable scope and compose correctly with campaign currentness/recovery?
- Are multi-live/cross-scope transitions and closed-unabsorbed states realizable without distributed fictional partial establishment?
- Are absence/deactivation semantics consistent with agency and world continuity?

## WP-17 — Async collaboration and agency-safe progression

Questions:

- What exact record/currentness owner, if any, stores collaboration obligation/window/generation/contributions?
- Are required/optional contributors, purpose/scope/generation binding and stale-response behavior implementable without a global active-player queue?
- Can the system determine and represent maximal safe frontier without letting transport order choose fiction?
- Are join/rejoin and recipient catch-up mapped to current authoritative routes and disclosure rules?

## WP-18 — Story, continuity and Dramaturg planning

Questions:

- Where do Story records, indexes, coverage/source basis and Chronicler service state live?
- Are Story, continuity projections and prospective Dramaturg planning physically and semantically distinct?
- Where do player-local and multiplayer-only shared Dramaturg horizons live; how are generation, CAS/rebase, discovery, invalidation and lifecycle represented?
- Is `preparation has no entitlement to occur; canon invalidates preparation` enforced in instruction/runtime/test mapping?
- Can any retained planning/Story state become required canon/recovery authority accidentally?

## WP-19 — Bootstrap, campaign creation and initial materialization

Questions:

- Can the shipped package bootstrap itself using only GAME assets and supported host capabilities?
- Does `init_campaign.py`/template materialize every required root/index/manifest/schema/version owner required by the final architecture?
- Is first-play readiness ordering consistent with character readiness, publication, campaign card, access and rules-source requirements?
- Does bootstrap avoid forbidden alternate Git transports and undefined capability probing?

## WP-20 — Engine update, schema evolution and migration

Questions:

- Which final architecture changes require persistent schema/version changes or migrations for existing campaigns?
- Are engine/version compatibility and provenance semantics sufficient to choose/apply migrations safely?
- Can migrations preserve IDs, authority, currentness, history/recovery and multiplayer state?
- Are forward/backward incompatibilities explicit rather than silently tolerated?
- Is rollback/update failure behavior defined without corrupting campaign authority?

## WP-21 — Diagnostics, observability, cleanup and retirement

Questions:

- Are receipts/traces/logs/maintenance views sufficient to diagnose correctness without persisting hidden CoT?
- Are cleanup/retirement rules mapped for all record families that can become obsolete?
- Can cleanup prove blocker coverage/current basis without trusting best-effort indexes or age?
- Are Story/planning/index/cache rebuild/repair paths explicit?
- Are debug/support surfaces prevented from becoming gameplay authority or recipient-secret leak channels?

## WP-22 — Verification/test/evaluation completeness

Questions:

- Does every accepted architecture law map to an appropriate unit/contract/integration/scenario/LLM-acceptance test owner?
- Which existing tests are stale, contradict later accepted architecture or encode obsolete scaffolds?
- Are Protocol-4-derived MVP evaluations retained as post-implementation acceptance rather than architecture-stage fake implementation?
- Are negative laws/rejected abstractions protected by regression tests where materially likely to regress?
- Can CI/maintenance audit mechanically validate schemas/catalogs/templates/Project-Instructions parity and architecture invariants that are machine-checkable?

## WP-23 — Release/package/version/legal readiness

Questions:

- Does the release builder package exactly the intended GAME runtime and exclude DEV?
- Are version metadata and compatibility markers coherent across DEV/GAME/release output?
- Are install assets, Project Instructions and packaged runtime copies consistent?
- Are migration/release checks sufficient for persistent format changes introduced by implementation?
- Are required legal/attribution files present in both repository/runtime locations without architecture artifacts leaking private research provenance?

## WP-24 — Performance/scale/operational budget

Questions:

- Are normal-turn reads/writes bounded for realistic campaigns?
- Do file count, GitHub API/directory limits, context loading, index size, publication call count and multi-chat contention have explicit architecture-level bounds/fallbacks?
- Are optimization candidates distinguished from correctness requirements and guarded by revisit triggers?
- Is any accepted design relying on background polling/workers/heartbeats unavailable in the target product?

## WP-25 — Error/degradation/failure semantics

Questions:

- For missing capability, stale source, permission mismatch, malformed record, schema mismatch, context UNSATISFIABLE, corrupted current state, ambiguous publication and live conflict, is safe behavior explicit?
- Does failure ever cause guessing, silent authority substitution, mechanics replay, force push, cross-player action invention or hidden data promotion?
- Are recoverable vs blocked vs unsupported deployment outcomes distinguishable to implementation?

## WP-26 — Documentation/routing/supersession consistency

Questions:

- Do current routing/index/status docs point implementation work to actual owners?
- Are stale Step-6/old topology/old path/old schema assumptions identified and scheduled for repair?
- Do CORE headers/CORE_INDEX/Project Instructions agree on activation and authority?
- Are current canonical docs clearly distinguished from historical proposals/status snapshots?
- Are README mismatches reported rather than opportunistically rewritten?

## WP-27 — Final implementation-planning readiness

Questions:

- Can every implementation workstream be derived from an approved owner/machine/test mapping?
- Are dependency order, migration order, test-first obligations and publication/release consequences explicit?
- Is every remaining unknown either implementation detail, post-MVP evaluation, safe deferred trigger or owner-resolved trade-off?
- Is there any unresolved architecture question whose answer could materially change implementation topology/data model/interfaces?

Implementation planning may begin only when the answer to the last question is **no**.

---

# 4. Coverage method

Whole-project coverage does **not** mean reading every file as equally authoritative or rewriting the entire repository.

The audit must use a bidirectional proof:

```text
ARCHITECTURE -> MACHINE
for every accepted owning law/responsibility:
    identify concrete runtime/schema/storage/instruction/test destination

MACHINE -> ARCHITECTURE
for every current runtime/schema/catalog/template/tool/test responsibility:
    identify accepted owner
    or classify as stale/debt/implementation-only/derived
```

This second direction is essential. It catches old scaffold state that would otherwise survive merely because no new architecture document mentions it.

Coverage artifacts must preserve item-level semantics for enumerated source sets. In particular:

- Round-1 global invariants/owner contracts;
- Step-2/3 machine-contract families;
- Step-5 closure/recovery/concurrency laws;
- 82 Round-2 DIAMOND/STRONG dispositions plus S14/S53/D15 later changes;
- current persistent schema/catalog families;
- current test/evaluation obligations.

Coverage never means activating dormant work.

---

# 5. Required final-audit artifacts

The revised R2.7 should produce, at minimum:

1. **Whole-project Source Manifest / coverage ledger**.
2. **Global semantic-owner matrix**.
3. **Architecture -> machine realization matrix** spanning Round 1 + Round 2.
4. **Machine -> architecture reverse-conformance ledger** for current GAME/DEV surfaces.
5. **Persistent record/root/index/sharding matrix** for the full campaign model.
6. **HOT/SQLite realization matrix**.
7. **Instruction/CORE/Project-Instructions ownership map**.
8. **Bootstrap/migration/version/update matrix**.
9. **Verification/evaluation/release-readiness matrix**.
10. **Gap/conflict/debt/stale-reference ledger** with exact disposition.
11. **Whole-project adversarial composition review**.
12. Owner Decision Brief(s) only for genuine residual product/architecture trade-offs.
13. **Canonical final architecture/machine-realization specification**.
14. **Implementation-planning entry resolution gate**.

---

# 6. Consequence for the existing R2.7 brief

The existing `2026-08-24-r2-7-machine-realization-holistic-closure-task-brief.md` is directionally useful but insufficient as the final architecture gate because many required mappings/exit criteria are expressed primarily in terms of R2.1-R2.6 and the Round-2 evidence ledger.

Its valid material is retained, especially:

- exact physical storage/index/HOT mapping;
- Context Runtime/TurnEnvelope mapping;
- R2.5 collaboration and Dramaturg mapping;
- instruction ownership;
- post-MVP Protocol-4 test handoff;
- holistic duplicate-owner/composition review.

The revised brief must expand those into the whole-project audit defined above and explicitly include Round-1 mechanics/execution, all current GAME runtime/domain surfaces, bootstrap/update/migration, release/version/legal and reverse-conformance of existing machine contracts.
