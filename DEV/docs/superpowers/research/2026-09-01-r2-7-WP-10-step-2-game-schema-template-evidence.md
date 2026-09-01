# R2.7 WP-10 — Step 2 Evidence B: Current GAME Schema and Template Families

Status: **STEP-2 EVIDENCE SLICE B — COMPLETE CURRENT GAME FAMILY COVERAGE**

All 20 current schemas and all 20 local campaign template files named by the
WP-10 Source Manifest were read on the Step-2 public ref. A template is generator
input only: it is neither campaign-branch proof nor semantic authority.

## Schema/template family ledger

| Family | Exact schema | Exact template evidence | Native role / result |
|---|---|---|---|
| Campaign identity/routing | `GAME/SCHEMA/campaign_manifest.schema.yaml` | `GAME/CAMPAIGN/MANIFEST.yaml` | mapped native campaign metadata; roots STATE/INDEX/WORLD/LOG/CHECKPOINTS only route data |
| Campaign preferences | `GAME/SCHEMA/campaign_config.schema.yaml` | `GAME/CAMPAIGN/CONFIG.yaml` | mapped campaign configuration; not current world truth |
| Compact card | `GAME/SCHEMA/campaign_card.schema.yaml` | `GAME/CAMPAIGN/CAMPAIGN_CARD.yaml` | mapped derived display projection |
| Current route/frontier | `GAME/SCHEMA/current_state.schema.yaml` | `GAME/CAMPAIGN/STATE/CURRENT.yaml` | mapped compact routing/frontier only |
| Checkpoint | `GAME/SCHEMA/checkpoint.schema.yaml` | `GAME/CAMPAIGN/CHECKPOINTS/_TEMPLATE.yaml` | mapped immutable descriptor/projection only |
| Event/history | `GAME/SCHEMA/event.schema.yaml` | `GAME/CAMPAIGN/LOG/_TEMPLATE.yaml`, `GAME/CAMPAIGN/INDEX/EVENT_INDEX.yaml` | partial: semantic-event format/index, not mechanical-event/message/chronology replacement |
| Session | `GAME/SCHEMA/session.schema.yaml` | `GAME/CAMPAIGN/SESSIONS/_TEMPLATE.yaml` | mapped bounded coordination only |
| House Rules | `GAME/SCHEMA/house_rules_policy.schema.yaml` | `GAME/CAMPAIGN/RULES/HOUSE_RULES.yaml`, `GAME/CAMPAIGN/RULES/HOUSE_RULES.md` | mapped narrow policy identity/currentness; prose and sidecar remain distinct |
| Generic index | `GAME/SCHEMA/index.schema.yaml` | all ten `GAME/CAMPAIGN/INDEX/*_INDEX.yaml` files | mapped derived routing only; no duplicate entity database |
| PC / Player | `GAME/SCHEMA/pc.schema.yaml`; `GAME/SCHEMA/player.schema.yaml` | `PC_INDEX.yaml`; `PLAYER_INDEX.yaml` | partial Actor/Player evidence; PC legacy knowledge/relationship/mechanics projections are explicitly non-authoritative |
| NPC / Faction / Location / Lore / Item / Scene / Thread | respective `npc`, `faction`, `location`, `lore`, `item`, `scene`, `thread` schemas | corresponding exact INDEX templates | current natural-world record evidence; their indexes remain routing only |
| Live state | `GAME/SCHEMA/live_scene.schema.yaml` | no local seed required | current live overlay evidence; base+live route preserves native owner, and no missing template proves no record |
| Storage repository default | `GAME/SCHEMA/dnd_storage.schema.yaml` | no engine-local campaign template | storage-discovery/default metadata, not existing-campaign authority |

## Completeness and negative evidence

1. Every named schema/template family is accounted for above, including the
event index corrected during Senior-HOLD repair.
2. No template exists for an independently named Actor-continuity, knowledge,
effect/application, Step-3 runtime, disclosure/message/Story, temporal-binding,
allocator, collaboration or Dramaturg record family. This is absence of current
template evidence, not permission to assign those concerns to MANIFEST, CURRENT,
SESSION, CHECKPOINT, LOG or INDEX.
3. The current schemas themselves reject the false-authority shortcuts: card is
projection; manifest excludes frontier; current excludes generic pending work;
checkpoint excludes snapshot/current authority; index excludes entity ownership;
session excludes chat history; live state does not become a mega-owner.
4. Template omission is not an automatic schema/root insufficiency where the
record is demand-created (for example LIVE) or where the primary owner declares
no durable representation (WP-09 controls).

## Consumer route evidence

`GAME/TOOLS/init_campaign.py` copies the local `GAME/CAMPAIGN/` template into
a campaign branch; `GAME/CORE/NEW_CAMPAIGN_FAST_PATH.md` and
`GAME/CORE/STORAGE.md` distinguish that source from the selected campaign root.
`GAME/CORE/PERSISTENCE.md`, `SAVE_CONTRACT.md`, `DURABILITY_GUARD.md`,
`SESSION.md`, `LIVE_SCENE.md` and `CHRONOLOGY.md` preserve the same
currentness/projection restrictions. Therefore a template cannot satisfy a
record-family finding by itself.

## Step-2 slice-B finding

**F10-B1 — the current GAME family covers the established campaign metadata,
compact routing/projection, natural-world and selected operational records, but
does not by name or contract provide exact native families for the unmapped
owners recorded in evidence A.** The finding remains a record-family audit input.
It does not select paths, partitions, migration, generator changes or bootstrap
order.

Next: Step-2 evidence C — runtime/DEV contract and test-consumer reverse audit,
then the required complete Step-2 synthesis.