# R2.7 WP-11 Step 6 — Independent Adversarial Critic

Status: **COMPLETE — CANDIDATE REQUIRES STEP-7 REPAIR**

The reviewer independently reconstructed the WP-11 graph through the project
map and inspected the canonical identity, persistence/recovery/live/chronology,
Story and WP-10 owners, plus GAME schemas/templates/consumers and DEV catalogs,
machine schemas and regression cases. The candidate was reviewed as a new
physical contract, not as authority.

| ID | Attack mechanism and route | Severity | Evidence and consequence | Disposition | Human decision |
|---|---|---|---|---|---|
| AR-01 | `core-catalog`/identifier policy `world.actor` → Actor references → candidate PC/NPC `family_key` | BLOCKING | Actor has one canonical `actor-*` namespace, but `world.actor.pc` and `.npc` would make known-ID route calculation ambiguous. Promotion/category changes could produce competing paths or force index lookup. | Use one `world.actor` family route; treat PC/NPC only as discovery classification. | NO |
| AR-02 | Admitted catalog/identifier kinds → candidate native matrix → recovery/publication/bootstrap | BLOCKING | ActorGroup, Connection, Zone, Organization, Contract, Mission, Encounter, Hazard, MaintenanceAudit and CatalogGapReport have neither route nor no-record disposition. | Account for each kind by exact route or explicit non-campaign classification. | NO |
| AR-03 | message identifier policy → live identity laws → candidate message route | BLOCKING | Campaign-sequential message allocation cannot create the epoch-qualified source-native live identity required for independent live writers. The route accepts an ID but cannot select a conflicting allocator policy. | Make the route consume the owner-supplied canonical ID and record source-native live ID materialization as a WP-16 forward obligation; do not select its syntax in WP-11. | NO |
| AR-04 | candidate MANIFEST selection rule → manifest schema/template → storage/bootstrap | SIGNIFICANT | `SESSIONS` and Story roots have no current MANIFEST selector, so recovery/bootstrap could choose route authority differently. | Select explicit static `sessions_root` and `story_root` fields and record schema/template/bootstrap/migration obligations. | NO |
| AR-05 | candidate Story path → Step-4/5.10 Story route/publication/cleanup | SIGNIFICANT | The inserted `RECORDS` segment contradicts the accepted Story record route beneath the layer shard. | Conform to `STORY/<layer>/<floor(sequence/1000)>/<story_id>.yaml`; retain layer metadata at the layer root. | NO |
| AR-06 | SHA path mapping → identifier/composite policy → integrity/recovery | SIGNIFICANT | A sole hash filename detects but cannot represent a collision, turning a valid second identity into permanent denial. | Use hash only for fixed shard selection and an injective encoded route-input path component for the record filename. | NO |
| AR-07 | deterministic Scene route → `CURRENT.active_scenes[].path` → session/recovery | SIGNIFICANT | Mutable stored Scene path can disagree with the stable-ID route and become a competing route carrier. | Final CURRENT holds `scene_id` only; path is derived/rebuilt and migration/publication removes stale stored paths. | NO |

## Negative results

- Length-framed composite input itself avoids delimiter ambiguity.
- The candidate's general eligibility and non-secret index rules reject index
  authority, secret leakage and index-absence proof.
- Two-level sharding, Story's accepted sequence grouping and measured-only index
  partitioning do not introduce a directory-growth defect.
- The LIVE exception preserves fixed-claim exact-source CAS and does not create a
  campaign index.
- Embedded values and Context Runtime controls are not incorrectly promoted to
  native record families.

All findings are mechanically resolvable within the accepted WP-11 mandate.
The critic found no product, semantic-authority, compatibility-policy or risk
acceptance decision requiring the human architect.
