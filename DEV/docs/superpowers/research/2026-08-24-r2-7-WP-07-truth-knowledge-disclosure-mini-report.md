# R2.7 WP-07 — Truth, Knowledge, Disclosure and Communication Evidence — Mini-Report

Статус: **STEPS 1-8 COMPLETE — WAITING SENIOR REVIEW**

## Краткий вывод

WP-07 подтвердил, что canonical corpus задаёт пять разных семантических
ответственностей. Slices 1-3 классифицировали F01-F06: две текущие prose/schema
поверхности являются stale debt, отсутствие Story и
truth/knowledge/message/disclosure machine realization остаётся уже названной
implementation obligation, а в inspected shipped instruction corpus отсутствует
явный R2.6 instruction equivalent для active role/RoleContextBundle/lawful typed
handoffs. PC/live surfaces не создают вторую authority, но их будущая machine
normalization требует отдельной verification obligation.

Slice 3 подтвердил, что shipped instruction layer и R2.3/R2.4 logical-role
gateways являются consumer/containment route, а не шестой информационной
authority. Instruction surfaces не обнаружили нового дублирующего owner,
небезопасного раскрытия, неограниченного retrieval или конфликта
recovery/compaction, но не содержат явного R2.6 instruction equivalent. F06
фиксирует это как уже существующую R2.6/R2.7 implementation obligation без
изобретения machine path или owner. Step 2 полностью покрывает required proof
Task Brief; для него не требуется evidence slice 4.

## Покрытые вопросы

- базовая semantic-owner geometry;
- catalog/entity/identifier machine contracts;
- installed campaign schema/template topology;
- PC/live projection boundary;
- message/disclosure/Transcript compaction route;
- первичная проверка existing regression/audit coverage.
- независимая классификация WP-07/F01..F05 через canonical owners и machine
  consumers; без вывода о product/architecture decision.
- shipped instruction-layer role/information consumers;
- R2.3 eligibility/bounded-discovery/trace contract и R2.4 rebinding/typed
  handoff/visible-output fence, а также отсутствие их явного R2.6 instruction
  equivalent в inspected shipped instruction corpus;
- adversarial mapping duplicate authority, unsafe visibility, unbounded
  retrieval и recovery/compaction interaction.

## Source Manifest delta

Прочитаны и сопоставлены:

- Step-4 canonical spec и single-context amendment;
- Step-5.10, 5.11, 5.12, 5.13 и 5.14 canonical specs;
- R2.1–R2.6 canonical specs, где они задают direct consumer boundary;
- CATALOG_CONTRACTS.md, ENTITY_STRUCTURES.md, current catalog JSON and
  identifier policies;
- installed GAME schemas/template roots and relevant CORE runtime documents;
- runtime-interaction-state machine contract and existing Step-4 regression
  test.
- `CATALOG_ADMISSION.md`, `CATALOG_INVENTORY.md` и admission ledger: смысл
  admission/realization trace не равен физической реализации;
- current `campaign_manifest`, PC, live-scene, event and session schemas,
  `LIVE_SCENE.md`, `STORAGE.md`, `SAVE_CONTRACT.md`, relevant catalog tests and
  maintenance audit.
- `GAME/CORE/AI_REASONING.md`, `INFORMATION.md`, `LORE.md`, `NARRATIVE.md`,
  `NPC.md`, `PREP.md` и `GM_CRAFT.md` как shipped instruction consumers;
- R2.3 Context Runtime, R2.4 single-context execution, R2.6 MVP host
  assurance и Step-5.11/5.13/5.14 recovery/retention owners.

Финальный Source Manifest и Task-Brief critic находятся в:

- DEV/docs/superpowers/design/2026-08-31-r2-7-WP-07-truth-knowledge-disclosure-task-brief.md;
- DEV/docs/superpowers/design/2026-08-31-r2-7-WP-07-task-brief-critic.md.

## Установленные факты

| Responsibility | Canonical owner / contract | Current DEV machine contract |
|---|---|---|
| Objective proposition truth | world.lore_fact; Step 4 separates truth_status from record lifecycle | admitted world record; entity-structures.json requires statement, truth_status, record_status |
| Fictional subject stance | world.knowledge, conceptually (knower_id, fact_id) | admitted composite-key world record; current JSON requires knower_id, fact_id, stance |
| Human exposure | runtime.disclosure, conceptually (player_id, fact_id) | admitted composite-key runtime record |
| Accepted communication evidence | runtime.message linked to accepted interaction | admitted sequential runtime record; runtime-interaction-state has input/response message IDs and authenticated player binding |
| Story / Transcript | durable non-canonical projection; Transcript is evidence, not truth | projection/retention is governed by Steps 5.10–5.12; cleanup by Step 5.13 |

The canonical contracts also establish:

- PC voluntary belief/suspicion/rejection is not silently authored by Actor or Narrator;
- human delivery does not automatically modify fictional knowledge;
- Story availability does not create disclosure;
- live-epoch knowledge/disclosure evidence must normalize into native durable owners at the appropriate handoff, not persist as a second global authority;
- exact message payload retention/compaction is constrained by surviving semantic, Transcript, disclosure and idempotency obligations.

Slice 3 additionally establishes:

- shipped CORE instructions preserve the distinction between objective truth,
  subject-local fictional knowledge, player disclosure, provisional preparation
  and player-facing projection; they do not define a new persistent owner;
- the later single-context amendment controls physical co-presence: Context
  Assembler still decides logical eligibility and bounded source selection, and
  raw role frames remain ineligible to downstream roles;
- R2.4 requires rebind before each logical phase, fresh Narrator rebind after
  Chronicler, minimal typed handoffs and the Narrator-only visible-output path;
- R2.3 forbids generic world/history graph walks and makes failed assembly
  terminal for that attempt; `ContextTrace` is restricted diagnostic evidence,
  not prompt content or authority;
- instruction advice to retain hard facts/causal obligations and not promise a
  complete transcript agrees with Step-5.11 selective exact retention and
  Step-5.13 survivor-before-removal, rather than weakening recovery semantics.
- Step-5.12 requires structural validation of material disclosure refs before
  `EMISSION_COMMIT`; after that boundary, an interrupted response may
  over-confirm the full committed disclosure although only a prefix was visible.

## Architecture -> machine

Established current route:

    Step-4/5 semantic owner
        -> DEV catalog kind + entity/identifier contract
        -> GAME persistent schema/template/runtime consumer
        -> validation and regression evidence

The DEV catalog contains all four record kinds with current identifiers. The
installed GAME campaign schema README also declares the truth/knowledge/player
information separation as a stable data-format rule.

`COMPLETE` в catalog-admission ledger не означает, что GAME already has every
runtime schema/path: canonical `CATALOG_ADMISSION.md` explicitly separates
admission from realization, а `CATALOG_CONTRACTS.md` передаёт exact
truth/knowledge/disclosure/message schemas and roots в WP-07. Поэтому отсутствие
физического файла само по себе не превращает admission ledger в ложный semantic
owner или в completed runtime realization claim.

## Machine -> architecture

Among the 51 current GAME/SCHEMA/ and GAME/CAMPAIGN/ template files scanned for
the WP-07 owner names/boundaries:

- lore.schema.yaml is the direct installed lore representation;
- PC and live-scene files contain knowledge-related fields;
- event.schema.yaml carries factual/knowledge deltas and visibility;
- no separate installed schema/template file named or textually identifying
  world.knowledge, runtime.disclosure or runtime.message was found;
- MANIFEST.yaml has STATE, INDEX, WORLD, LOG and CHECKPOINTS roots, but no STORY root.

This is evidence, not yet a conclusion about which representation/debt contract
governs each absence.

Slice 2 establishes the following reverse dispositions:

- `lore.schema.yaml` is a current installed stale representation: its combined
  `status` axis conflicts with the Step-4 truth/lifecycle split.
- the `world.knowledge` row in `ENTITY_STRUCTURES.md` is stale prose relative
  to both Step-4 and the current machine field inventory; the document also
  remains an outdated ledger citation until a later narrow repair.
- absent `story_root` is already an explicit Step-5.10 machine-realization debt,
  not evidence against Story's non-authority.
- absent dedicated installed representations for admitted record kinds are
  existing realization obligations; exact roots/paths are not inferred from the
  catalog or from the legacy scaffold.
- PC and live fields are bounded legacy/epoch evidence. Their documents do not
  authorize parallel global knowledge or disclosure mutation; executable
  normalization proof remains unimplemented.

## Конфликты / stale / negative findings

### WP-07/F01 — installed lore schema versus canonical truth/lifecycle split

```text
Source/item: GAME/SCHEMA/lore.schema.yaml; Step-4 sections 4.1-4.3;
  DEV/CATALOG/entity-structures.json world.lore_fact.
Actual claim: lore.schema.yaml combines `canonical`, `superseded` and
  `disputed_in_world` in one `status`; Step-4 requires separate
  `truth_status` and `record_status`, and retires disputed objective truth.
Authority/classification: Step-4 semantic owner; current catalog exact field
  contract; installed GAME schema is machine representation.
Qualifiers/applicability: exact later field spelling is implementation work, but
  the separate axes and no objective `truth.disputed` rule are normative.
Current physical representation: legacy GAME lore schema exists; no compatible
  current lore-record schema is present.
Architecture -> machine: the accepted world.lore_fact field contract is not
  materialized by this legacy schema.
Machine -> architecture: the schema contradicts the accepted truth/lifecycle
  boundary and cannot define it.
Conflict / disposition: STALE_DEBT.
Rationale: this is a genuine current conformance mismatch, not a request for a
  new lore owner or migration policy. Clean-slate R2.7 permits its later narrow
  repair after the remaining WP-07 evidence is complete.
```

### WP-07/F02 — entity-structure document versus current catalog field contract

```text
Source/item: DEV/ARCHITECTURE/ENTITY_STRUCTURES.md world-record table;
  Step-4 section 5; DEV/CATALOG/entity-structures.json; catalog conformance test.
Actual claim: ENTITY_STRUCTURES lists `status` / `learned_from_id`; Step-4 and
  current machine inventory require `stance` and allow bounded
  `supporting_source_refs` / `last_changed_event_id`.
Authority/classification: Step-4 is semantic owner; catalog JSON is exact
  field-contract authority; ENTITY_STRUCTURES is stale owning-prose companion.
Qualifiers/applicability: Step-4 forbids a second epistemic event log and keeps
  history in SemanticEvents; the field inventory does not itself select a
  physical record path.
Current physical representation: current catalog/schema validation and
  `test_r2_7_wp03_catalog_conformance.py` preserve the newer field contract;
  the prose row and admission-ledger citation still use the old wording.
Architecture -> machine: current machine contract conforms to the accepted
  conceptual relation.
Machine -> architecture: the stale prose conflicts with its current catalog
  companion and is not a semantic override.
Conflict / disposition: STALE_DEBT.
Rationale: a narrow later prose/trace repair is required, but no new knowledge
  semantics, owner, schema, migration or consumer is authorized by this slice.
```

### WP-07/F03 — Story root absent from installed manifest topology

```text
Source/item: GAME/CAMPAIGN/MANIFEST.yaml and campaign_manifest.schema.yaml;
  Step-5.10 sections 30-31.
Actual claim: the installed manifest exposes no `story_root`; Step-5.10 says a
  static Story routing field may later be established and records its absence as
  a known machine-realization gap.
Authority/classification: Step-5.10 is canonical Story projection owner;
  manifest/schema are current installed machine surfaces.
Qualifiers/applicability: Story remains noncanonical; mutable Story coverage and
  allocation do not belong in MANIFEST/CURRENT/RRC, and ordinary catch-up must
  not mutate MANIFEST.
Current physical representation: NO STORY ROOT; MANIFEST currently routes only
  STATE, INDEX, WORLD, LOG and CHECKPOINTS.
Architecture -> machine: static Story root/scaffold/migration is explicitly
  deferred by the owner.
Machine -> architecture: absent root is a known unmaterialized routing surface,
  not a competing Story authority or a semantic contradiction.
Conflict / disposition: IMPLEMENTATION_OBLIGATION.
Rationale: Step-5.10 names the exact later realization cluster. This slice does
  not create a root, schema, template or migration.
```

### WP-07/F04 — admitted records without visible installed record schemas

```text
Source/item: CATALOG_ADMISSION.md; CATALOG_CONTRACTS.md section 12;
  core-catalog.json, entity-structures.json, identifier-policies.json,
  catalog-admission-ledger.json; GAME schema/template scan.
Actual claim: the catalog admits world.knowledge, runtime.disclosure and
  runtime.message, but the installed schema/template surface has no dedicated
  durable representation for them.
Authority/classification: catalog JSON owns exact IDs/field/identity shape;
  CATALOG_ADMISSION owns realization-trace interpretation; Step-4/5 own
  semantics; GAME files are installed machine surfaces.
Qualifiers/applicability: admission and `COMPLETE` are independent axes.
  `COMPLETE` records sufficient catalog admission/class/identity routing, not
  physical runtime completion. Runtime.message's current sequential policy is
  separately Step-5.11/5.12 implementation debt for live-source use.
Current physical representation: NO DEDICATED INSTALLED RECORD SCHEMA/PATH;
  runtime-interaction-state provides only message IDs and authenticated binding.
Architecture -> machine: CATALOG_CONTRACTS explicitly assigns exact
  truth/knowledge/disclosure/message schemas, roots, sharding and HOT/SQLite
  realization to later R2.7 work.
Machine -> architecture: present catalog entries are valid class/identity
  contracts, not false claims that the legacy GAME scaffold already realizes
  every persistent owner.
Conflict / disposition: IMPLEMENTATION_OBLIGATION.
Rationale: the absence is a named realization obligation, not by itself a
  repository defect and not authorization to invent physical paths in Slice 2.
```

### WP-07/F05 — PC/live knowledge fields require owner-bound normalization proof

```text
Source/item: GAME/SCHEMA/pc.schema.yaml, live_scene.schema.yaml,
  GAME/CORE/LIVE_SCENE.md; Step-4 section 5; Step-5.12 sections 11, 17-18.
Actual claim: PC `knowledge` is explicitly a legacy non-authoritative
  projection/input surface. Live facts and observable events may name PCs that
  perceived a fact; close-time compaction carries durable knowledge results.
Authority/classification: Step-4 world.knowledge and Step-5.12
  runtime.disclosure are semantic owners; PC/live are bounded machine
  projection/epoch surfaces.
Qualifiers/applicability: live state must not become a second disclosure
  authority; human disclosure is recipient-scoped and does not imply PC
  knowledge. A closed live epoch requires campaign absorption before it loses
  authority for its bounded live scope.
Current physical representation: PC embedded arrays and epoch-local live
  perception facts exist; no live `runtime.disclosure` owner exists, as required
  by the Step-5.12 non-goal.
Architecture -> machine: current documentation establishes owner-bound
  compaction intent, but does not supply executable normalizer/record schemas.
Machine -> architecture: no current field grants a parallel global writable
authority; the surface remains legacy/epoch-local evidence.
Conflict / disposition: VERIFICATION_OBLIGATION.
Rationale: no duplicate-owner conformance defect is established. Later machine
realization must test normalization, recipient isolation and no second live
disclosure owner; this slice creates neither a new test nor a new path.
```

### WP-07/F06 — explicit R2.6 active-role instruction equivalent absent

```text
Source/item: GAME/INSTALL/PROJECT_INSTRUCTIONS.txt; GAME/CORE/AI_REASONING.md,
  INFORMATION.md, LORE.md, NARRATIVE.md, NPC.md, PREP.md, GM_CRAFT.md and
  CORE_INDEX.md; R2.6 section 3; Step-4 amendment sections 4-7; R2.3 sections
  3-18; R2.4 sections 6-12.
Actual claim: R2.6 requires R2.7 to map an explicit shipped instruction/CORE
  behavior equivalent: use only information eligible to the active role under
  the current RoleContextBundle and lawful typed handoffs; physical presence does
  not make it eligible; lawful later eligibility restores normal use. The
  inspected PROJECT_INSTRUCTIONS and CORE corpus contain no explicit active-role,
  RoleContextBundle or lawful typed-handoff instruction.
Authority/classification: R2.6 is the canonical obligation owner; R2.7 and
  implementation/TDD own the exact wording, module activation and tests. The
  inspected GAME files are shipped runtime instruction consumers.
Qualifiers/applicability: shared physical context is permitted by the later
  amendment, but physical presence never makes information eligible. Existing
  CORE guidance distinguishes truth, fictional stance, disclosure and
  preparation, but that non-conflict is not the R2.6-required explicit
  behavior-equivalent instruction.
Current physical representation: PROJECT_INSTRUCTIONS plus the inspected CORE
  Markdown corpus; no explicit required instruction equivalent is present.
Architecture -> machine: this is the existing R2.6/R2.7 implementation
  obligation. This audit does not select a machine path, physical file owner or
  test beyond the owners R2.6 already assigns.
Machine -> architecture: no inspected consumer creates a competing information
  owner, raw/transitive role inheritance, unrestricted retrieval or a
  player-visible bypass of Narrator/disclosure admission; its omission cannot
  satisfy the explicit R2.6 instruction requirement.
Conflict / disposition: IMPLEMENTATION_OBLIGATION.
Rationale: the required instruction behavior is absent, while the canonical
  owner already classifies its exact realization as R2.7/implementation work; no
  new architecture decision, owner or path follows from this finding.
```

### WP-07/N02 — Slice-3 adversarial mapping

```text
Source/item: Step-4 amendment sections 5-9; R2.3 laws 6-7, 11-12 and 18-20;
  R2.4 laws 14-19 and 28-30; R2.6 laws 1-6; Steps 5.11, 5.13 and 5.14.
Actual claim: the current contracts prohibit duplicate information authority,
  require role/recipient eligibility and pre-emission material-disclosure
  validation before semantic use, bound discovery and escalation, and retain
  native-owner/recovery/survivor obligations independently from volatile model
  context or lawful prose compaction. After `EMISSION_COMMIT`, interruption may
  over-confirm full disclosure although only a prefix was visible.
Authority/classification: canonical cross-owner adversarial constraints.
Qualifiers/applicability: behavioral containment is a correctness contract, not
  a claim of physical/cognitive isolation; exact wording may be compacted only
  after protected semantic and survivor obligations are discharged. `UNSATISFIABLE`
  requires a finite registered fallback, not repeated unbounded assembly.
Current physical representation: instruction consumers and current architecture
  contracts exist; the task does not claim implemented end-to-end runtime proof.
Architecture -> machine: no new path, owner or migration follows. Existing
  realization obligations remain responsible for deterministic eligibility,
  typed handoffs, recipient admission, retention and cleanup enforcement.
Machine -> architecture: no inspected instruction consumer contradicts these
  constraints or turns host context, Story, trace, cache or prose into authority.
Conflict / disposition: SATISFIED.
Rationale: duplicate authority, unsafe visibility, unbounded retrieval and
  recovery/compaction interaction each have an accepted current owner and no
  additional WP-07 finding was observed.
```

## Автоматически принятые технические решения

- Treat DEV catalog machine contracts and installed GAME schemas as separate
  evidence layers. Neither overrides the canonical Step-4/5 semantic owner
  merely because it is newer-looking or executable.
- Treat field-name disagreement as a traceability/conformance question until
  supersession/current-consumer analysis establishes a narrower classification.
- Do not create a new information registry, transcript subsystem or migration
  design while auditing existing authority.
- Treat the R2.6 behavioral-containment rule as a current observable correctness
  requirement while preserving its explicit non-claim of physical/cognitive
  isolation; do not restate the superseded physical-separation interpretation.
- Treat the inspected instruction corpus's generic containment language as
  non-conflicting consumer evidence, not as fulfillment of R2.6's explicit
  active-role/RoleContextBundle/lawful typed-handoff instruction requirement.

## Implementation obligations

No new implementation work is accepted in this slice. Existing owner-routed
obligations: F03, F04 and F06 remain implementation obligations. F01 and F02 are
stale debt requiring later narrow repair; F05 remains a verification obligation.

F06 records, rather than creates, the existing R2.6/R2.7 obligation. The existing
R2.3/R2.4/R2.6 and Step-5 realization clusters remain the only route for
executable role eligibility, typed handoff, recipient admission, retention and
cleanup behavior.

## Verification / MVP acceptance obligations

Slice 2 used current executable evidence only for its present scope:
`test_r2_7_wp03_catalog_conformance.py` verifies the catalog's Step-4
vocabulary/fields/identifiers, while the maintenance audit validates catalog
JSON/schema consistency but does not claim the missing owner record paths or live
normalization. Both passed locally for this documentation checkpoint; future
physical realization must add the owner tests required by Steps 5.10-5.13 and
R2.6.

The instruction mapping is prose/contract evidence, not an execution claim for
behavioral containment. A supported MVP must still receive the downstream R2.6
synthetic-canary and role/recipient/compaction acceptance coverage when the
machine route exists.

## Forward obligations

No cross-domain forward obligation is created. F01-F06 and the adversarial
mapping remain accounted current WP-07 evidence; their later
repair/realization/verification route stays with the established owner.

## Round-2 Diamond/Strong delta

No new DIAMOND/STRONG disposition is asserted in this slice.

## Human decision

**NONE.** Step 2 exposes no residual product, authority, compatibility or
risk-acceptance decision.

## Closure verdict

**STEPS 1-8 COMPLETE — WAITING SENIOR REVIEW.** The three evidence slices account
for F01-F06 and the required adversarial mapping: semantic owner separation,
durable/machine representation or explicit absence, lawful transfer boundaries,
pre-emission validation plus the Step-5.12 post-emission interruption limitation,
Transcript and compaction limits, PC/live normalization, and instruction/role
eligibility. F06 is already an R2.6/R2.7 implementation obligation and does not
require a new owner decision or evidence slice. Steps 3-8 preserved those
dispositions without adding architecture or machine work. Senior review is now
mandatory before WP-08.

## Точка продолжения

Mandatory Senior review of the completed WP-07 Step-8 closure. The review package
is `2026-08-31-r2-7-WP-07-step-3-decision-brief.md` through
`2026-08-31-r2-7-WP-07-step-8-canonicalization.md`; do not begin WP-08 or
implementation planning before a Senior GO.
