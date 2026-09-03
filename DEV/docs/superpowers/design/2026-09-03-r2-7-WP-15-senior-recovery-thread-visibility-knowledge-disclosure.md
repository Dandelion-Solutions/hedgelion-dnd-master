# R2.7 WP-15 — Post-Step-1 Senior Recovery — Thread Visibility / Knowledge / Disclosure

Status: **SR15-03 CLOSED — STEP 1 + SENIOR REPAIR COMPLETE / MANDATORY SENIOR REVIEW REQUIRED**

Date: 2026-09-03

Domain: **WP-15 — temporal owners / processes / chronology**

Finding: **SR15-03 — SIGNIFICANT — thread visibility fields were not routed to the accepted truth / knowledge / disclosure owner graph**

This record is a separate post-critic Senior-recovery artifact. It does not rewrite the historical WP-15 Task-Brief critic `C01–C12` and does not amend the earlier `SR15-01` / `SR15-02` recovery artifact as though those findings had already covered this omission.

---

## 1. Defect

After `GAME/SCHEMA/thread.schema.yaml` became a mandatory Step-2 input under `SR15-01`, the Step-1 package still did not provide an auditable owner route for:

```text
visibility.known_by_pc_ids
visibility.public
```

That omission is significant because the fields sit next to durable `world.thread` process state and can otherwise be misread as a second durable PC-knowledge owner, PLAYER-delivery evidence, or an information-eligibility shortcut.

The defect is source-graph/framing incompleteness only. No new product semantic, architecture owner, compatibility policy or human risk decision is required.

---

## 2. Mandatory accepted owners / upstream constraints

Step 2, if later authorized, must consume at minimum:

- `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md` — canonical truth / fictional knowledge separation; `world.knowledge` is the durable fictional subject-stance owner keyed conceptually by `(knower_id, fact_id)`;
- `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md` — canonical PLAYER-delivery boundary; `runtime.disclosure` is recipient-scoped delivery evidence and is not fictional knowledge;
- `GAME/CORE/INFORMATION.md` — current shipped information consumer requiring reconciliation with the accepted owner split;
- `DEV/CATALOG/entity-structures.json` — current machine/catalog field contract for `world.knowledge` (`knower_id`, `fact_id`, `stance`, bounded provenance fields);
- `DEV/CATALOG/identifier-policies.json` — current machine identity policies for `world.knowledge` `(knower_id, fact_id)` and `runtime.disclosure` `(player_id, fact_id)`;
- applicable closed WP-07 truth/knowledge/disclosure/message-evidence artifacts, including:
  - `DEV/docs/superpowers/research/2026-08-24-r2-7-WP-07-truth-knowledge-disclosure-mini-report.md`;
  - `DEV/docs/superpowers/design/2026-08-31-r2-7-WP-07-truth-knowledge-disclosure-task-brief.md`;
  - `DEV/docs/superpowers/design/2026-08-31-r2-7-WP-07-step-3-decision-brief.md`;
  - `DEV/docs/superpowers/design/2026-08-31-r2-7-WP-07-step-5-candidate-spec.md`;
  - `DEV/docs/superpowers/design/2026-08-31-r2-7-WP-07-step-6-adversarial-review.md`;
  - `DEV/docs/superpowers/design/2026-08-31-r2-7-WP-07-step-7-resolution-gate.md`;
  - `DEV/docs/superpowers/design/2026-08-31-r2-7-WP-07-step-8-canonicalization.md`.

WP-07 remains a closed audit constraint. These artifacts do not supersede the Step-4 / Step-5.12 semantic owners; they preserve the already-accepted realization/debt/negative-case routes and explicitly reject parallel knowledge/disclosure authority in current PC/live-style machine surfaces.

The Step-2 Source Manifest remains open-world: owner-graph traversal must add any additional current realization, routing, storage, schema, normalization, recovery, publication, retention or test surface for `world.knowledge` / `runtime.disclosure` that is actually discovered. Absence of a dedicated current GAME schema/path must be recorded as evidence/debt, not filled by invention during Step 1.

---

## 3. Required Step-2 disposition

Step 2 must disposition **each field separately**:

### `thread.visibility.known_by_pc_ids`

Establish from evidence whether the current field is retained, derived, cached, a bounded hint/projection, denormalized, retired, or otherwise constrained by the accepted machine realization.

Until that evidence synthesis occurs:

- it is **not** a second durable `world.knowledge` owner;
- membership does not by itself assert the complete durable PC knowledge relation;
- physical presence/readability of the thread record does not make the information eligible to a PC or role;
- it cannot replace source/provenance and accepted knowledge-update rules.

### `thread.visibility.public`

Establish from evidence whether the current field is retained, derived, cached, a bounded hint/projection, denormalized, retired, or otherwise constrained by the accepted machine realization.

Until that evidence synthesis occurs:

- `public=true` does **not** itself establish PC knowledge;
- `public=true` does **not** prove PLAYER delivery;
- `public=true` does **not** replace information-eligibility / role-context rules;
- record existence, file readability or host visibility do not imply semantic disclosure.

No final machine shape for either field is selected in Step 1.

---

## 4. Preserved authority boundaries

The repaired Step-1 package binds the following for later evidence extraction:

```text
objective truth / current world owner
    != world.knowledge fictional subject stance
    != runtime.disclosure PLAYER-delivery evidence
    != runtime.message accepted communication evidence
    != thread visibility projection/field
```

Therefore:

1. `world.thread` does not become a second durable PC-knowledge owner.
2. PC knowledge and PLAYER delivery remain different responsibilities.
3. `runtime.disclosure` remains delivery evidence, not fictional knowledge.
4. `public`, physical readability or mere record existence do not establish PC knowledge, PLAYER delivery or information eligibility.
5. A temporal/process reverse audit must not infer knowledge/disclosure authority merely because visibility fields are colocated with process state.
6. Any later normalization/retirement/derivation decision must preserve current accepted truth/knowledge/disclosure/message-evidence ownership and bounded eligibility rules.

---

## 5. Non-decisions / scope guard

This repair does **not**:

- choose whether either `thread.visibility.*` field is retained/derived/cache/hint/denormalized/retired;
- add a new knowledge/disclosure owner;
- add a new schema, root, outbox, transcript or information graph;
- change `GAME/**`, runtime, schema, template, catalog or tests;
- reopen WP-07, Step 4 or Step 5.12;
- begin WP-15 Step 2, WP-16 or implementation planning.

---

## 6. Closure

```text
SR15-03:                         CLOSED BY SENIOR REPAIR
CLASSIFICATION:                  SIGNIFICANT
SOURCE_GRAPH_ROUTE_ADDED:        YES
FIELD_DISPOSITION_DEFERRED:      YES — REQUIRED IN STEP 2 IF AUTHORIZED
SOURCE_MANIFEST_OPEN_WORLD:      YES
UPSTREAM_CONTRADICTION:          NO
NEW_UNSATISFIED_CONSUMER:        NO
MATERIAL_UPSTREAM_INSUFFICIENCY: NO
UPSTREAM_REOPEN_REQUIRED:        NO
UNRESOLVED_BLOCKING:             0
UNRESOLVED_SIGNIFICANT:          0
HUMAN_DECISION_REQUIRED:         NO
STEP_2_AUTHORIZED:               NO
NEXT_GATE:                       MANDATORY SENIOR REVIEW
```
