# Engine Update Regression Cases — Runtime Release Asset

## U01 — Untagged main is not player release
Pass: normal players are never offered public main HEAD as release.

## U02 — New tag discovery is metadata only
Pass: report tag availability; matching local runtime Release Asset is still required.

## U03 — Missing target runtime asset
Pass: request matching `hedgelion-dnd-master-runtime-v<version>.zip`; no clone/pull/source copy and no substitution with GitHub-generated source archives.

## U04 — Ask choices
Pass: Update / Not now / Always update automatically.

## U05 — No polling
Pass: no per-turn/background release checks.

## U06 — Guest skips maintenance
Pass: guest does not update storage baseline/campaign engine.

## U07 — Guest exact package
Guest campaign needs A, only B local.
Pass: require A; no silent B runtime/migration.

## U08 — Baseline metadata only
Owner adopts B.
Pass: only DND_STORAGE.engine.baseline_version changes; zero engine files.

## U09 — Baseline does not mutate campaigns
Pass: campaign A stays A until separate migration.

## U10 — Published new campaign provenance
Baseline/local published B.
Pass: manifest pins tag B + exact public tag commit SHA.

## U11 — Development package provenance
Local package release_status development and authenticated user is engine owner.
Pass: explicit test may use dev-v<version> and null SHA. Do not query/pin current public main merely to manufacture SHA.

## U12 — Development package forbidden to normal user
Pass: development package cannot be treated as a normal release.

## U13 — Active live epoch blocks migration
Pass: defer campaign engine migration.

## U14 — Dirty state persists first
Pass: establish clean durable frontier before maintenance.

## U15 — Compatibility blocks blind auto
Pass: maintenance_required/unknown requires bounded maintenance.

## U16 — Migration changes campaign data only
Pass: apply schema/data migration + manifest provenance, never engine files.

## U17 — Layout preservation
Legacy CAMPAIGN/ campaign migrates engine.
Pass: migration uses resolved legacy roots and does not relocate layout unless an explicit layout migration says so.

## U18 — Canon survives migration
Pass: unrelated WORLD/STATE/LOG preserved.

## U19 — Optimistic race
Campaign HEAD moved after preparation.
Pass: rebuild/re-evaluate; never force push.

## U20 — Post-update full CORE cache rebuild
Campaign successfully migrates engine A -> B.
Pass: switch to exact local package B, invalidate the whole old engine instruction cache, then preload the complete B `CORE/*.md` plus `RULES/INDEX.md` and `RULES/README.md` once before further adjudication. Do not reload only a small mandatory-module subset. Campaign data not touched by migration remains lazy.

## U21 — Partial success
Baseline B succeeds, campaign migration deferred/fails.
Pass: baseline stays B, campaign stays A.

## U22 — Technical update is not fictional time
Pass: do not invent rest/travel/NPC delay for maintenance.

## U23 — No mixed engine context
After successful migration to B, some old-A CORE text remains cached while new-B files are available.
Pass: invalidate old engine instruction cache and rebuild the complete B CORE cache before gameplay; never adjudicate with mixed package instructions.

## U24 — GitHub source archive is not a runtime package
A GitHub-generated repository source ZIP contains nested `GAME/ENGINE_VERSION.yaml` plus development material.
Pass: package validation rejects it because `ENGINE_VERSION.yaml` is not directly at the package root with the required sibling runtime directories; the user must provide the custom runtime Release Asset.
