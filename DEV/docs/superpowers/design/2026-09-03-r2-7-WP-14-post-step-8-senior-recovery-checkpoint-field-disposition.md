# R2.7 WP-14 — Post-Step-8 Senior Recovery — SR14-04 Checkpoint Field Disposition

Status: **POST-STEP-8 SENIOR RECOVERY COMPLETE — SR14-04 CLOSED / MANDATORY FINAL SENIOR RE-AUDIT REQUIRED**

Date: 2026-09-03

Finding:

> **SR14-04 — SIGNIFICANT — incomplete checkpoint field-by-field disposition**

Affected completed WP-14 chain:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-step-2-evidence-extraction.md`;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-step-8-canonicalization.md`;
- `DEV/docs/superpowers/specs/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-canonical-spec.md`.

Current machine surfaces inspected at the pre-repair public state:

- `GAME/SCHEMA/checkpoint.schema.yaml`;
- `GAME/CAMPAIGN/CHECKPOINTS/_TEMPLATE.yaml`.

Controlling accepted owner:

- `DEV/docs/superpowers/specs/2026-08-20-step-5-7-checkpoint-recovery-protocol-canonical-spec.md`, especially LAWS 5.7-27..32 and section 17 minimum checkpoint semantic contract.

This recovery does **not** rewrite historical Step-6 findings F01-F08. SR14-04 was found only by the mandatory final Senior audit after Step 8.

---

## 1. Root cause

WP-14 Step 1 required Step 2 to map every current checkpoint/session/recovery field and behavior to an owner/disposition. Step 2 correctly captured the main authority-sensitive checkpoint fields but grouped several current schema members under broad summaries such as “engine/runtime data” and “active lists”. It did not record an auditable leaf-by-leaf disposition for every current `checkpoint.schema.yaml` member.

The omission affected completeness accounting, not the selected architecture. Step 5.7 already provides enough accepted authority to repair the accounting mechanically.

No contradiction, new product semantic, material trade-off or upstream insufficiency is introduced.

---

## 2. Exhaustive current checkpoint field disposition

Role vocabulary used by this recovery:

```text
REQUIRED_DESCRIPTOR_IDENTITY_ASSOCIATION
OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT
RETIRED
SCHEMA_FORMAT_METADATA_ONLY
```

The table covers every current field admitted by `GAME/SCHEMA/checkpoint.schema.yaml` and notes the corresponding current template representation.

| Current schema field | Current template | Binding role | Auditable disposition / authority boundary |
|---|---|---|---|
| `schema_version` | `schema_version: 2` | `SCHEMA_FORMAT_METADATA_ONLY` | Retain equivalent format/version identity only as required by the checkpoint wire/schema contract. It does not establish recovery/currentness/chronology authority. |
| `id` | `id: null` | `REQUIRED_DESCRIPTOR_IDENTITY_ASSOCIATION` | Stable immutable checkpoint descriptor identity. Identity alone grants no gameplay/currentness authority. |
| `campaign_id` | `campaign_id: null` | `REQUIRED_DESCRIPTOR_IDENTITY_ASSOCIATION` | Associates the descriptor with one campaign and participates in descriptor validation. It is not a source selector or recovery frontier. |
| `created_at` | `created_at: null` | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Diagnostic/provenance timestamp only. Never chronology, freshness, currentness or “latest checkpoint” authority. |
| `valid_through_event_id` | `null` | `RETIRED` | Retired as generic checkpoint recovery-completeness/frontier semantics. No event-ID fallback may replace current native routing/currentness. |
| `expected_commit_sha` | `null` | `RETIRED` | Retired. A checkpoint stored inside content-addressed Git cannot depend on embedding the identity of its own containing commit. Revision context/provenance must remain external/non-self-referential where needed. |
| `world_time` | `null` | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Not part of the minimum checkpoint contract. If retained later, it is domain-typed diagnostic/presentation observation only; never chronology, due/not-due or currentness authority. |
| `state` container | present | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Structural grouping of non-authoritative layout/root observations only. The container itself is not a checkpoint-owned state snapshot or authority object. |
| `state.current_state_path` | `STATE/CURRENT.yaml` | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Non-authoritative layout hint only if actual layout indirection needs it. **It is not a checkpoint-owned current-state selector, recovery frontier, root-completeness proof, currentness authority, SAVE/handoff proof or fallback source.** Current native routing/owners still select current state. |
| `state.active_pc_ids` | `[]` | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Optional non-exhaustive positive observation only if proven useful. Omission never proves no active PC/root and cannot establish root completeness. |
| `state.active_thread_ids` | `[]` | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Optional non-exhaustive positive observation only if proven useful. Omission never proves no active thread/root and cannot establish root completeness. |
| `state.active_scene_ids` | `[]` | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Optional non-exhaustive positive observation only if proven useful. Omission never proves no active scene/root and cannot establish root completeness. |
| `recovery_notes` | `[]` | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Diagnostic/support notes only. They cannot supply missing native authority, accepted interpretation, exact evidence or hidden recovery state. |
| `engine` container | present | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Optional runtime provenance observation only. **Checkpoint engine projection is not current runtime authority and does not replace accepted interpretation dependencies of open execution.** |
| `engine.version` | `null` | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Runtime-version provenance observation only; current campaign/runtime owner and open-work interpretation contracts govern actual execution compatibility. |
| `engine.package_id` | `null` | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Package-identity provenance observation only; not runtime-selection/currentness authority. |
| `engine.source_commit_sha` | `null` | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Optional source provenance observation only; not current campaign/ref/runtime authority. |
| `engine.package_sha256` | `null` | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Optional package provenance/integrity observation only; cannot by itself select current runtime or reinterpret accepted work. |
| `engine.adopted_at` | `null` | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Diagnostic adoption-time observation only; no ordering/currentness/chronology semantics. |
| `ruleset` container | **absent from current template** | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Schema-admitted non-authoritative ruleset provenance projection. Current template omission is current machine/template alignment debt; this recovery does not change implementation. |
| `ruleset.ruleset_set_sha256` | **absent from current template** | `OPTIONAL_DIAGNOSTIC_PROVENANCE_HINT` | Optional ruleset-set provenance/integrity observation only. **It is not current ruleset authority, does not select a replacement ruleset set, and does not replace accepted rules/catalog/invocation interpretation dependencies of open execution.** |
| `schema_data_version` | `schema_data_version: 2` | `SCHEMA_FORMAT_METADATA_ONLY` | Retain only if checkpoint format/migration ownership needs it. It does not establish gameplay/recovery/currentness semantics. |

Template-specific observation:

- current `_TEMPLATE.yaml` materializes all schema members above except the optional `ruleset` container / `ruleset.ruleset_set_sha256`;
- that mismatch is an implementation/template-alignment obligation for later authorized realization, not authority evidence and not authorization to edit GAME now.

---

## 3. Authority closure

The exhaustive table preserves these non-negotiable boundaries:

1. checkpoint remains optional immutable descriptor/evidence and ordinary healthy recovery may read zero checkpoints;
2. no checkpoint field becomes current gameplay authority, a RecoveryCut, universal frontier, source/root completeness manifest, session lease, SAVE proof or handoff proof;
3. `state.current_state_path` is only a possible layout hint and never selects current semantic state;
4. active PC/thread/scene lists remain non-exhaustive hints and cannot prove absence/completeness;
5. engine/ruleset projections are provenance only; current runtime/ruleset authority comes from current owners, while still-significant accepted execution recovers its own compatible pinned interpretation dependencies;
6. retired fields remain retired rather than reinterpreted to preserve the current schema by inertia;
7. schema/format metadata is not semantic authority;
8. no new checkpoint source/root manifest, RecoveryCut, frontier field or replacement completeness structure is introduced;
9. checkpoint remains non-mandatory and `MANIFEST.last_checkpoint_id = null` remains healthy.

---

## 4. Repair propagation

SR14-04 requires only documentation/canonical-accounting repair:

- Step-2 evidence extraction receives the exhaustive field table and corrected completeness claim;
- Step-8 self-review records the post-Step-8 Senior recovery and truthful field-coverage closure;
- final WP-14 canonical specification receives the same binding field-by-field disposition/authority fences;
- global/task-local cursors remain on mandatory final Senior audit, narrowed to **mandatory final Senior re-audit after SR14-04**.

No `GAME/`, schema, template, runtime, catalog, test or tooling implementation is changed.

Historical Step-6 F01-F08 and Step-7 dispositions remain unchanged.

---

## 5. Disposition

```text
SR14-04:                  CLOSED
SEVERITY:                 SIGNIFICANT
MECHANICALLY_RESOLVABLE:  YES
UPSTREAM_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED:  NO
UNRESOLVED_BLOCKING:      0
UNRESOLVED_SIGNIFICANT:   0
NEXT_GATE:                MANDATORY FINAL SENIOR RE-AUDIT
```
