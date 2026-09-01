# R2.7 WP-11 Step 7 — Resolution Gate

Status: **COMPLETE — ALL STEP-6 FINDINGS RESOLVED**

| Issue | Severity | Agree | Resolution and consequence | Human decision |
|---|---|---|---|---|
| AR-01 | BLOCKING | YES | Replaced PC/NPC route families with one `world.actor` family at `WORLD/ACTORS`. PC/NPC remain discovery classifications only, so a canonical Actor ID computes one route. | NO |
| AR-02 | BLOCKING | YES | Added exact physical dispositions for all omitted admitted world/runtime kinds. No missing catalog kind is inferred absent from a current template. | NO |
| AR-03 | BLOCKING | YES | Clarified that the route consumes, rather than allocates, the canonical ID. Live source-native epoch-qualified ID materialization is a typed WP-16 forward obligation; no campaign allocator fallback is admitted. | NO |
| AR-04 | SIGNIFICANT | YES | Selected static `sessions_root` and `story_root` MANIFEST fields alongside the existing root selectors. Schema/template/bootstrap/migration realization remains under WP-19/WP-20. | NO |
| AR-05 | SIGNIFICANT | YES | Restored the accepted Story record path directly below the layer sequence bucket; only projection state remains at the layer root. | NO |
| AR-06 | SIGNIFICANT | YES | Hash now chooses only the two-level bucket. A chunked unpadded Base32hex encoding of the full framed route input supplies an injective, deterministic filename path, avoiding hash uniqueness authority. | NO |
| AR-07 | SIGNIFICANT | YES | Selected `scene_id`-only active-scene entries. Stored paths are removed by downstream migration and are derived/rebuilt from the stable Scene route. | NO |
| RR-01 | SIGNIFICANT | YES | Preserved the current `event_log_root` MANIFEST selector rather than silently renaming it to `log_root`; only new static selectors require downstream schema/template work. | NO |

The repairs introduce no new semantic owner, chronology source, publication
authority or downstream implementation decision. The candidate remains within
WP-11; its forward obligations name, but do not begin, WP-12--WP-24 work.
