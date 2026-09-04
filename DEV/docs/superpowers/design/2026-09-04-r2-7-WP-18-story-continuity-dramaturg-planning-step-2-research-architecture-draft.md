# R2.7 WP-18 — Story / Continuity / Dramaturg Planning — Step-2 Research & Architecture Draft

Status: **STEP 2 COMPLETE — EVIDENCE EXTRACTED / ARCHITECTURE DRAFT READY FOR STEP 3**

Date: 2026-09-04

Approved Step-1 basis: `1db145712632aca7b2e89c655d468192e1004a86`

This artifact executes the approved Architecture Task Brief. It records owner-level evidence, machine/runtime reverse evidence, negative findings, applicability qualifiers and the architecture draft that Step 3 must evaluate. It selects no final architecture by itself.

---

## 1. Evidence method and completeness discipline

Evidence was recovered from current owning specifications before derivative/runtime surfaces. The open-world Source Manifest was expanded whenever an owning source exposed another material consumer or when current machine/runtime behavior could contradict the framing.

The extraction covered:

- Step-4 Story/truth/role separation;
- Step-5.10 Story projection durability;
- Step-5.11 exact history/compaction;
- Step-5.12 disclosure;
- Step-5.13 cleanup/retention;
- R2.1 continuity/history;
- R2.2 Actor continuity;
- R2.3 Context Runtime;
- R2.4 single-context role execution;
- R2.5 multiplayer retained planning;
- R2.6 host assurance;
- WP-08..WP-17 applicable realization/currentness owners;
- current Actor/catalog/schema/test realization;
- current Story/planning catalog/schema negative evidence;
- current direct runtime consumers named in the recovered Step-1 dependency graph and additional consumers discovered while following their contracts.

Search snippets, roadmaps and PROJECT_MAP routes were used only for discovery. Material conclusions below come from current owner/consumer content.

---

## 2. Established semantic owners

### E18-01 — Story is a durable noncanonical source-bound projection family

Controlling owners: Step 4 + Step 5.10.

Story is retrospective presentation/history, not current state or gameplay authority. The accepted layer family is:

```text
STORY/TRANSCRIPT
STORY/EVENTS
STORY/MECHANICS
STORY/NARRATIVE
```

Each layer owns its own projection progress. Story omission is not semantic absence. Story cannot establish objective truth, Actor cognition, fictional knowledge, human disclosure, fictional chronology, current mechanics or recovery canon.

Applicability: durable Story is already accepted architecture. WP-18 must realize/reconcile it rather than ask whether Story should exist.

### E18-02 — Story projection progress is layer-local and source-contract-relative

Controlling owner: Step 5.10.

A Story layer has durable projection state equivalent to:

```text
layer identity
layer Story-ID allocator high-water
coverage_by_source_domain[]
required local indexes/editorial metadata
```

Coverage is typed by source domain and semantic contract generation. It is not Git HEAD, campaign-wide chronology, global Story freshness or a universal frontier.

Backlog is derived from source-domain enumeration minus compatible coverage. No durable skip ledger, scheduler, queue or worker is required.

### E18-03 — Chronicler service state is not an independent durable owner

Controlling owners: Step 5.10 + R2.4.

`NO_BACKLOG | SERVICE(window) | DEFER(reason)` is a turn-local service decision. Chronicler may transform an admitted source bundle, but does not own final IDs, coverage, publication, canon or a persistent job queue.

Architecture implication: baseline outcome is `NO DURABLE CHRONICLER SERVICE RECORD`. Durable Story projection state is sufficient to derive backlog after restart.

### E18-04 — Story publication is independent, gameplay-priority and noncanonical

Controlling owners: Step 5.10 + WP-13.

Story publication uses ordinary validated/non-force publication mechanics but is not part of the correctness-critical gameplay commit frontier. Story conflict or failure cannot roll back accepted gameplay. Cross-layer atomicity is not required.

Technical publication/ID/file order is not fictional chronology.

### E18-05 — Story exactness is consumer-specific

Controlling owner: Step 5.11.

Story Transcript can be an exact archive only where its source contract says so. It is not a universal substitute for `runtime.message` or another exact semantic evidence owner. Compaction may occur only when every surviving consumer's required semantic/exactness floor remains satisfied.

### E18-06 — Story visibility is not disclosure

Controlling owners: Step 4 + Step 5.12 + R2.3.

A Story record may be physically readable to the runtime and still be ineligible for a specific role/player. Context admission requires current role/subject/purpose eligibility. Story cannot grant PC knowledge or human disclosure merely because it exists.

### E18-07 — Story has specific retention continuity; generic refs do not

Controlling owner: Step 5.13.

Cleanup blockers exist only where an owning contract explicitly promises them. Story source enumeration/coverage may require specific source retention continuity. Generic refs, indexes or mere physical presence are not retention authority.

---

## 3. Continuity and Actor boundaries

### E18-08 — No generic continuity owner is admitted

Controlling owners: R2.1 + R2.3.

Continuity is typed retrieval from current owners plus admitted history/projections. Story can orient broad retrieval, followed by bounded escalation to the proper current/exact source when a material decision depends on it.

Architecture implication: baseline outcome is `DERIVED ONLY`; no `continuity_state`, memory graph, vector authority or campaign-wide continuity frontier is required.

### E18-09 — Source Actor owns current non-epistemic intentional continuity

Controlling owner: R2.2.

Sparse durable Actor cognition may include:

```text
long_term_goal
current_objective
next_intention
material_commitments[]
reconsideration_cues[]
```

`world.knowledge` separately owns proposition stance.

Current R2.7 realization confirms this owner through `ACTOR_MODEL.md`, `world-actor-state.schema.json`, `world-record.schema.json`, `entity-structures.json` and `test_r2_7_wp04_actor_asset_conformance.py`.

Architecture implication: neither Story nor Dramaturg planning may become the hidden canonical place for an NPC/Actor's real current goal, intention, promise or reconsideration state.

### E18-10 — PC voluntary agency remains player-owned

Controlling owners: R2.2, Step 4, WP-17, current runtime.

Dramaturg planning may prepare pressures/opportunities/conditional responses. It may not author a voluntary PC decision, belief, emotion, loyalty, speech, goal or consent.

---

## 4. Dramaturg planning evidence

### E18-11 — Preparation is provisional and has no entitlement to occur

Controlling owners: Step 4, R2.4, R2.5, `PREP.md`, `RUNTIME.md`, `AI_REASONING.md`.

Preparation may include situations, pressures, Actor refs, likely reactions, clues, opportunities, constraints, assumptions and near-horizon unopposed developments. It is future-facing guidance, not future fact.

Current canon, including accepted player decisions, current Actor decisions, mechanics and native owner transitions, invalidates incompatible preparation.

### E18-12 — `PreparationDraft` is an ephemeral typed handoff, not a durable owner

Controlling owner: R2.4.

Serialization or physical persistence of a TurnEnvelope/control value cannot promote it into independent campaign state.

### E18-13 — Single-player durable planning has no proved baseline consumer

Controlling owners: WP-10 + WP-11 + R2.4.

Single-player preparation can be recomputed from current owners and current context. Loss of ephemeral prep does not lose canon.

Architecture implication: baseline single-player result is `EPHEMERAL ONLY` / `NO DURABLE PLANNING RECORD`.

Reopen trigger: a later measured/accepted consumer must prove that recomputation is insufficient and that retained state has independent lifecycle/recovery value.

### E18-14 — Multiplayer supplies the admitted retained-planning consumer

Controlling owner: R2.5.

Independent participant sessions require durable noncanonical preparation coherence through:

```text
player-local Dramaturg horizon
+
multiplayer-only shared Dramaturg horizon
```

The local horizon may retain player-specific preparation and a shared-generation hint. The shared horizon retains cross-player pressures/threads/directions/convergence/mystery constraints plus source/currentness basis and generation.

Both are noncanonical and must remain independently eligibility-scoped.

### E18-15 — Planning entry semantics are two typed classes

Controlling owner: R2.5.

```text
SOURCE_ANCHORED_CONSTRAINT
PROVISIONAL_DRAMATURGIC_DIRECTION
```

A source-anchored constraint references an authoritative source/basis and must be revalidated; it does not copy authority into planning. A provisional direction remains disposable even if repeated or retained across generations.

### E18-16 — Planning generation is owner-local concurrency metadata

Controlling owners: R2.5 + WP-16.

Shared planning updates require exact-current-generation/base validation and must not use blind merge/LWW. Generation cannot establish fictional chronology, campaign/LIVE currentness or global freshness.

### E18-17 — Planning invalidation is demand-driven and selective

Controlling owners: R2.5 + R2.3 + WP-09.

Before material use/update, relevant source/currentness assumptions are revalidated. Incompatible entries are discarded/rebuilt/rebased. No background whole-campaign scan is required.

### E18-18 — Multiplayer mode controls eligibility, not byte existence

Controlling owners: R2.5 + `MULTIPLAYER.md` + WP-16.

Shared planning is active only while multiplayer is enabled. Disabling multiplayer may leave bytes physically present, but they become semantically inactive. Re-enable requires bounded revalidation/discard/rebuild before use.

---

## 5. Durability, recovery, retention and chronology

### E18-19 — Durable projection does not become canonical world/runtime authority

Controlling owners: Catalog Contracts + WP-13.

Story/Dramaturg retained projections are dedicated noncanonical projection families outside `world.*` and `runtime.*` current authority unless a later approved design explicitly changes the boundary.

### E18-20 — Recovery prefers current native owners

Controlling owner: WP-14.

Story/planning can assist orientation, but cannot reconstruct canon, accepted mechanics, RNG results, Actor current state or accepted fiction when native owner evidence is absent. Lost/stale/corrupt planning is rebuilt or omitted.

### E18-21 — Planning references do not become generic cleanup blockers

Controlling owner: Step 5.13.

No current accepted contract promises that provisional preparation keeps every referenced canonical source alive. If a source disappears/changes legitimately, planning revalidates and invalidates/rebases. This avoids a new GC/retention authority.

### E18-22 — Technical order never becomes fictional chronology

Controlling owners: WP-15 + `CHRONOLOGY.md` + `MULTIPLAYER.md`.

Story IDs, planning generations, Git commits, file sequence and CAS success order may support technical conflict handling only. Fictional causal/temporal order remains owned by native chronology/process/current-state owners.

---

## 6. Host/instruction/runtime evidence

### E18-23 — Role containment is architectural correctness on the current host

Controlling owner: R2.6, realized through WP-08/WP-09.

Physical co-presence cannot grant role eligibility. Dramaturg/Actor/Chronicler outputs reach Narrator only through typed eligible handoffs/fresh rebinding. Same-envelope newly produced Story cannot feed narration/gameplay back into the same envelope.

### E18-24 — R2.6 evaluation is downstream of implementation

WP-18 architecture must define testable behavior obligations now, but production-like integrated host evaluation runs against the implemented MVP later. No parallel MVP or architecture-time acceptance harness is justified.

---

## 7. Current machine/runtime evidence and gaps

### E18-25 — Actor boundary is already machine-realized

Current schema/catalog/test surfaces explicitly enforce the R2.2 Actor continuity owner. WP-18 should reference, not duplicate, this contract.

### E18-26 — Story/planning vocabulary exists, dedicated realization does not yet

Catalog 2.0 already contains roles, typed drafts, Story layer/candidate vocabularies and planning entry classes. Current `GAME/SCHEMA/` contains no dedicated Story/planning schema and `campaign_manifest.schema.yaml` does not yet expose `storage.story_root`.

This is implementation-facing debt for later approved realization, not a Step-2 implementation task.

### E18-27 — current direct runtime consumers preserve the intended boundaries

Fresh reads confirm:

- `RUNTIME.md` — state/mechanics/consequences precede narration; Story emerges from play; no protected ending;
- `AI_REASONING.md` — `PROVISIONAL_PREP` is distinct from canonical/inferred/undefined; state before story; obsolete prep not preserved merely due to context cost;
- `NARRATIVE.md` — narration projects resolved state and may not invent unresolved consequences;
- `INFORMATION.md` / `LORE.md` — truth, belief, knowledge, disclosure and history remain separate; clues/prep cannot retroactively rewrite reality;
- `NPC.md` / `DIALOGUE.md` — NPC action/speech derives from current Actor motives/knowledge, not Story/planning copies;
- `PROCESSES.md` — causal world process advancement is not dramatic scheduling;
- `CAMPAIGN_OPERATIONS.md` — only plausible next-horizon prep retained; unused provisional scenes do not become canon;
- `STORAGE.md` / persistence/recovery modules — native owner state and current frontier control; caches/projections do not;
- `MULTIPLAYER.md` / `LIVE_SCENE.md` — shared-world authorization/currentness is separate from planning;
- `CHRONOLOGY.md` — fictional order is not technical order.

### E18-28 — admission-ledger planning provenance requires later machine alignment

The current catalog admission ledger routes planning-entry vocabulary through provenance that does not fully name the current R2.5 owner even though R2.5 owns the retained-planning class semantics. This does not change architecture, but later machine-alignment work must make ledger traceability point to the accepted WP-18/R2.5 result rather than implying Story/continuity ownership.

This is recorded as evidence, not yet as a Step-6 finding; Step 6 must independently reconstruct whether it rises to a blocking/significant propagation defect.

---

## 8. Negative findings

The investigation found no evidence requiring:

- a global plot graph;
- a universal continuity/memory database;
- a Story scheduler/job queue/background worker;
- a generic planning registry/index;
- independent identity for each planning entry;
- a campaign-wide planning frontier/generation;
- a second fictional chronology owner;
- a single-player durable planning owner;
- planning-based GC retention of canonical sources;
- Story/planning recovery authority;
- a durable Chronicler service-state record;
- reopening R2.2 Actor continuity;
- reopening Step-4/5.10 Story semantics.

These negative findings remain first-class results unless later evidence exposes a concrete unsatisfied consumer.

---

## 9. Architecture draft for Step 3 evaluation

### 9.1 Story realization

Preserve the accepted WP-11 route:

```text
STORY/<layer>/PROJECTION_STATE.yaml
STORY/<layer>/<floor(sequence/1000)>/<story_id>.yaml
```

No global Story index. Any required layer-local editorial/reverse support is stored/derived under that layer and never becomes a competing owner.

Chronicler service state remains derived/ephemeral.

### 9.2 Continuity realization

No new continuity record. Retrieval remains typed/bounded:

```text
Story/history orientation
    -> identify unresolved dependency
    -> bounded current/exact owner retrieval
```

### 9.3 Single-player planning

No durable record. Use ephemeral `PreparationDraft`/working context and rebuild when lost/invalidated.

### 9.4 Multiplayer retained planning

Use a dedicated noncanonical projection root with deterministic direct routes and no registry/index:

```text
DRAMATURG/SHARED.yaml
DRAMATURG/PLAYERS/<player_id>.yaml
```

`player_id` is the stable campaign PLAYER identity, not login/display name.

The shared document is one multiplayer-only current horizon; player-local documents are independently scoped. Planning entries remain embedded typed values.

Each retained horizon carries only metadata required for safe use, conceptually:

```text
scope / owner key
generation
source_basis[] / assumptions[]
entries[]
invalidation cues / applicability hints
shared_generation_hint?   # player-local only
```

No `valid=true` flag is authoritative; current usability is revalidated against current mode/authorization/native sources when material.

### 9.5 Publication / conflict

- campaign-owned retained planning uses ordinary campaign-tree non-force publication;
- shared update requires exact current planning generation/base and current authorization/source revalidation;
- conflict -> fetch current affected horizon/source basis -> re-evaluate/rebase/discard; no blind merge/LWW;
- planning publication does not establish canon or fictional chronology;
- no campaign+LIVE distributed transaction; current native owner evidence wins.

### 9.6 Lifecycle

```text
EPHEMERAL SINGLEPLAYER PREP
    create -> use/revise -> discard/recompute

MULTIPLAYER RETAINED HORIZON
    absent -> create generation
    current compatible -> read/update successor generation
    incompatible -> selective rebase or replace generation
    mode disabled -> inactive regardless of bytes
    stale/corrupt/lost -> discard/rebuild
```

No tombstone/history subsystem is required solely for planning. Git history is audit transport evidence, not runtime planning history authority.

### 9.7 Recovery

Recovery may discover retained planning only after current campaign/mode/PLAYER/native owners are established. If planning cannot be proven compatible, omit/rebuild it. Never recover accepted fiction or mechanics from planning.

---

## 10. Synthesis-completeness check

```text
PRIMARY_SEMANTIC_OWNERS:               COVERED
ACTOR_OWNER_AND_MACHINE_REALIZATION:   COVERED
STORY_DURABILITY/EXACTNESS/DISCLOSURE: COVERED
MULTIPLAYER_PLANNING_CONSUMER:         COVERED
R2_6_APPLICABILITY:                    COVERED
WP08_WP17_BOUNDARIES:                  COVERED
DIRECT_RUNTIME_CONSUMERS:              COVERED FOR MATERIAL CURRENT SUBGRAPH
MACHINE_SCHEMA_CATALOG_TEST_EVIDENCE:  COVERED
NEGATIVE_FINDINGS:                     PRESERVED
DORMANT/CONDITIONAL_STATUS:            PRESERVED
HUMAN_MATERIAL_DECISION_FOUND:         NO
UPSTREAM_REOPEN_TRIGGER_FOUND:         NO
SOURCE_MANIFEST_OPEN_WORLD:            YES
```

Step 2 therefore closes with a bounded architecture draft suitable for Step-3 alternatives/decision work.
