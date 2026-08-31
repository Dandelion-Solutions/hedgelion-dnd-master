# R2.7 WP-07 — Truth, Knowledge, Disclosure and Communication Evidence — Mini-Report

Статус: **IN PROGRESS — Step 2, evidence slice 1**

## Краткий вывод

WP-07 подтвердил, что canonical corpus задаёт пять разных семантических
ответственностей. DEV catalog contracts уже содержат их актуальные identifiers и
минимальные field contracts. В installed GAME schema/template surface обнаружены
несколько несовпадающих или неполных представлений. Их классификация ещё не
закрыта: необходимо отличить stale material от явно сохранённой
implementation/verification obligation.

## Покрытые вопросы

- базовая semantic-owner geometry;
- catalog/entity/identifier machine contracts;
- installed campaign schema/template topology;
- PC/live projection boundary;
- message/disclosure/Transcript compaction route;
- первичная проверка existing regression/audit coverage.

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

## Architecture -> machine

Established current route:

    Step-4/5 semantic owner
        -> DEV catalog kind + entity/identifier contract
        -> GAME persistent schema/template/runtime consumer
        -> validation and regression evidence

The DEV catalog contains all four record kinds with current identifiers. The
installed GAME campaign schema README also declares the truth/knowledge/player
information separation as a stable data-format rule.

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

## Конфликты / stale / negative findings

### WP-07/F01 — installed lore schema versus canonical truth/lifecycle split

GAME/SCHEMA/lore.schema.yaml has a single status field with canonical,
superseded, disputed_in_world. Canonical Step-4 and the current catalog
distinguish truth_status (undetermined / established / disproven) from
lifecycle/record status and place in-world disagreement under subject knowledge.

Disposition: **OPEN — candidate STALE_DEBT or implementation conformance gap**.

### WP-07/F02 — entity-structure document versus current catalog field contract

DEV/ARCHITECTURE/ENTITY_STRUCTURES.md describes world.knowledge with status and
learned_from_id; current DEV/CATALOG/entity-structures.json requires stance and
names supporting_source_refs / last_changed_event_id.

Disposition: **OPEN — candidate stale documentation**. Verify supersession and
all consumers before repair/classification.

### WP-07/F03 — Story root absent from installed manifest topology

Step-4 specifies that the campaign manifest shall eventually expose a story_root;
the current installed manifest/schema lists no such root.

Disposition: **OPEN — candidate implementation obligation or stale machine-facing contract**.

### WP-07/F04 — admitted records without visible installed record schemas

The current DEV catalog admits world.knowledge, runtime.disclosure and
runtime.message; the installed schema/template scan did not find their dedicated
durable representation.

Disposition: **OPEN — must distinguish an explicit deferred realization from a
false COMPLETE/current-machine claim**.

### WP-07/F05 — PC/live knowledge fields require owner-bound normalization proof

pc.schema.yaml labels its knowledge shape non-authoritative. live_scene contains
known_by_pc_ids and observable perception evidence while declaring truth and
per-PC knowledge/disclosure distinct. The audit must verify that the current
compaction/migration route preserves those boundaries.

Disposition: **OPEN — candidate verification obligation; no duplicate-owner
finding yet**.

## Автоматически принятые технические решения

- Treat DEV catalog machine contracts and installed GAME schemas as separate
  evidence layers. Neither overrides the canonical Step-4/5 semantic owner
  merely because it is newer-looking or executable.
- Treat field-name disagreement as a traceability/conformance question until
  supersession/current-consumer analysis establishes a narrower classification.
- Do not create a new information registry, transcript subsystem or migration
  design while auditing existing authority.

## Implementation obligations

None accepted in this slice. F01–F04 require classification first.

## Verification / MVP acceptance obligations

No local test was run in this ChatGPT session. Existing tests were inspected only
as source evidence. Any later implementation-facing conclusion must identify
local VPS verification appropriate to the changed contract.

## Forward obligations

None created. WP-07 retains its own open findings.

## Round-2 Diamond/Strong delta

No new DIAMOND/STRONG disposition is asserted in this slice.

## Human decision

**NONE.** No residual product or architecture choice is established yet.

## Closure verdict

**IN PROGRESS.** No WP-07 closure claim.

## Точка продолжения

Step 2, evidence slice 2:

1. reconcile the meaning of catalog realization_state COMPLETE with actual
   installed GAME representation;
2. trace lore.schema.yaml, ENTITY_STRUCTURES.md, PC/live fields and manifest
   topology through current validators/tests/maintenance audit;
3. classify F01–F05 using explicit supersession, migration and consumer evidence;
4. then perform the remaining instruction/role-context and adversarial mappings.
