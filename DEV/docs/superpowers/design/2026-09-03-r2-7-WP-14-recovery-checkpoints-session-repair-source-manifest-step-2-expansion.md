# R2.7 WP-14 — Recovery / Checkpoints / Session / Repair — Step-2 Source-Manifest Expansion

Status: **STEP 2 COMPLETE — OPEN-WORLD MANIFEST EXPANSION CLOSED FOR SYNTHESIS**

Date: 2026-09-03

Base Step-1 manifest:

- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-14-recovery-checkpoints-session-repair-source-manifest.md`

Step-2 evidence ledger:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-step-2-evidence-extraction.md`

This document does not replace the Step-1 Source Manifest. It records the open-world additions/promotions discovered during direct Step-2 evidence extraction.

---

## 1. New direct consumers/evidence surfaces

| Source | Classification | Why it entered the WP-14 graph | Disposition |
|---|---|---|---|
| `DEV/ARCHITECTURE/CATALOG_INVENTORY.md` | DERIVATIVE MACHINE/DESIGN REGISTRY | Registers `runtime.session`, `runtime.checkpoint`, `runtime.maintenance_audit` and recovery outcome concepts. Confirms maintenance audit is a narrow support/runtime object rather than recovery authority. | INSPECTED; consumer/evidence only. |
| `DEV/CATALOG/identifier-policies.json` | IMPLEMENTATION / IDENTITY CONTRACT | Allocates campaign-scoped identity policies for checkpoint (`rev-*`), session (`session-*`) and maintenance audit (`audit-*`). Identity allocation does not grant authority. | INSPECTED; required downstream identity consistency. |
| `DEV/TOOLS/run_maintenance_audit.py` | DEVELOPMENT TOOL / NEGATIVE-SCOPE EVIDENCE | Name overlap could be confused with `runtime.maintenance_audit`; direct inspection shows this is a developer audit/test launcher, not shipped gameplay recovery state or the runtime record owner. | INSPECTED; explicitly excluded from runtime authority graph. |

No dedicated active-branch `runtime.maintenance_audit` wire schema was found during Step-2 discovery. WP-10/WP-11/identifier-policy allocation is sufficient to establish family/route/identity ownership for architecture synthesis; final wire fields remain later machine-realization work.

---

## 2. Promoted previously conditional/current consumers

| Source | Previous role | Step-2 evidence result | New disposition |
|---|---|---|---|
| `GAME/CORE/CHRONOLOGY.md` | conditional machine consumer | Recovery/checkpoint fields include time/order observations; Step 5.9 requires exact chronology separation. | REQUIRED synthesis input; no checkpoint/Git/session order as fictional chronology. |
| `GAME/CORE/ENGINE_UPDATES.md` | conditional machine consumer | Still-significant accepted work may span runtime refresh/recovery and must retain compatible interpretation context. | REQUIRED synthesis input for interpretation closure. |
| `GAME/TOOLS/init_campaign.py` | conditional scaffold consumer | Confirms scaffold does not create a checkpoint and merely carries nullable `last_checkpoint_id`; no startup checkpoint requirement. | REQUIRED scaffold-impact evidence. |
| `DEV/TESTS/EXPLICIT_SAVE_CASES.md` | conditional test consumer | Confirms checkpoint is not inherently required by explicit save; other campaign-only SAVE debt remains WP-13-owned. | REQUIRED non-conflation evidence. |

---

## 3. Promoted canonical route: explicit historical maintenance

The following active Step-5.7 laws are mandatory for WP-14 synthesis because `HDM_RESET_LAST_CHECKPOINT` is a current direct support consumer:

- LAW 5.7-17 — checkpoint may support explicit historical maintenance only as optional evidence when exact dependencies remain retained;
- LAW 5.7-31 — `last_checkpoint_id` is narrow descriptor pointer and not guaranteed rewind slot;
- LAW 5.7-52 — no guaranteed historical rewind; every required historical native source/revision/interpretation dependency must still be resolvable and compatible;
- LAW 5.7-53 — historical maintenance is distinct from ordinary current recovery;
- LAW 5.7-54 — approved historical restore/repair becomes current only through normal forward publication, never force/ref rewind;
- LAW 5.7-55 — current recovery correctness does not depend on old checkpoint retention.

This route was implicit in the base manifest through the primary Step-5.7 owner, but Step 2 promotes it to explicit mandatory evidence because SR14-02 makes the maintenance reset command a direct reconciliation target.

---

## 4. Confirmed Senior-repair routes

### SR14-01 — host memory + fixed gameplay repository transport

Mandatory synthesis evidence remains:

- `DEV/docs/superpowers/specs/2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md` — CANONICAL/OWNING for ambient host-context non-authority and supported-host assurance;
- `DEV/docs/superpowers/design/2026-08-24-r2-6-fixed-repository-transport-owner-clarification.md` — OWNER-APPROVED CLARIFICATION/OWNING for closed runtime transport selection.

These stay distinct from `AGENTS.md` and `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md`, which govern development-agent transport.

### SR14-02 — maintenance support consumer

`DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md` remains **CURRENT SUPPORT / MAINTENANCE CONTRACT / PROPOSAL**, not recovery authority.

Synthesis must reconcile:

- checkpoint export as read-only diagnostic projection;
- reset as explicit historical maintenance, not ordinary recovery rollback;
- all required historical native dependencies before local replacement;
- typed maintenance unavailability if retention is insufficient;
- `runtime.maintenance_audit` narrow support record;
- normal application authorization/currentness/native-owner durability for any mutation;
- forward non-force publication if approved restored state is to become current durable authority;
- no alternate runtime transport.

### SR14-03 — `MANIFEST.last_checkpoint_id`

Mandatory machine surfaces remain:

- `GAME/SCHEMA/campaign_manifest.schema.yaml`;
- `GAME/CAMPAIGN/MANIFEST.yaml`;
- `GAME/TOOLS/init_campaign.py` as scaffold consumer.

Synthesis must preserve a nullable narrow descriptor pointer only. Null remains a valid healthy campaign state.

---

## 5. Explicit non-owners retained as evidence only

The following current surfaces may contain useful recovery words/fields but do not gain semantic authority:

- checkpoint/session/current-state schemas/templates;
- `BOOTSTRAP_RUNTIME.md`, `RUNTIME.md`, `SESSION.md`, `INTEGRITY.md`, `STORAGE.md`, `PERSISTENCE.md`, `SAVE_CONTRACT.md` where they lag canonical owners;
- maintenance exports and support diagnostics;
- `runtime.maintenance_audit` records;
- cached session/campaign HEADs;
- surviving SQLite;
- ambient Project/chat/model memory;
- Story/transcript unless a separately owning exact evidence dependency remains live;
- test expectations;
- catalog/identifier registries;
- developer maintenance-audit launcher.

---

## 6. Open-world completeness result

Additional search/discovery performed for:

- checkpoint/session/currentness fields;
- `last_checkpoint_id` consumers and scaffold behavior;
- maintenance reset/export/audit consumers;
- maintenance-audit identity/route/schema evidence;
- chronology and engine-update recovery consumers;
- explicit-save/checkpoint interaction.

Result:

```text
NEW_SEMANTIC_OWNER_DISCOVERED:       NO
NEW_REAL_CONSUMERS_DISCOVERED:       YES
MANIFEST_EXPANDED:                   YES
SR14_01_ROUTE_COMPLETE:              YES
SR14_02_ROUTE_COMPLETE:              YES
SR14_03_ROUTE_COMPLETE:              YES
UNRESOLVED_SOURCE_GRAPH_GAPS:        0
UNRESOLVED_EVIDENCE_GAPS:            0
UPSTREAM_REOPEN_REQUIRED:            NO
HUMAN_DECISION_REQUIRED:             NO
STEP_3_SYNTHESIS_ALLOWED:            YES
```

The Source Manifest remains conceptually open-world for later Steps: if Step 3–6 exposes another real owner/consumer required to support a canonical claim, it must be added before that claim is finalized.