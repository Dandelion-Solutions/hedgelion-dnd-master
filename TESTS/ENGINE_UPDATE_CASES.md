# Engine Update Regression Cases — Archive Runtime

These cases verify release discovery/migration without copying engine trees into campaign storage.

## U01 — Untagged main is not a player release
Public main is ahead of latest tag.
Pass: normal players are not offered main HEAD as a release.

## U02 — New tag discovery is metadata only
Owner finds a newer published tag.
Pass: report availability; do not claim engine is installed until matching release ZIP is available locally.

## U03 — Missing target ZIP
Owner chooses to update but target archive is absent.
Pass: ask user to download/add GitHub Release Source code ZIP; do not clone/pull/blob-copy source.

## U04 — Ask policy choices
Valid newer local target exists and policy is ask.
Pass: offer Update / Not now / Always update automatically.

## U05 — Not now is temporary
Owner declines target T.
Pass: continue exact current campaign engine and do not nag during ordinary turns.

## U06 — Auto needs local package
Policy is auto but target ZIP is not local.
Pass: do not download/reconstruct automatically; request package at next appropriate boundary.

## U07 — No polling
No startup/resume/explicit update/maintenance event occurs.
Pass: no background/per-turn release checks.

## U08 — Guest skips maintenance
Authenticated user is not storage owner.
Pass: no storage baseline write or routine release-discovery prompt.

## U09 — Guest exact-engine requirement
Guest opens campaign pinned to engine A while only archive B is local.
Pass: require matching A archive; do not silently run B and do not migrate owner's campaign.

## U10 — Storage baseline is metadata only
Owner adopts local release B.
Pass: update only `DND_STORAGE.engine.baseline_version`; copy zero engine files.

## U11 — Baseline does not mutate campaigns
Storage baseline becomes B while campaign remains A.
Pass: campaign stays on A until separate migration succeeds.

## U12 — New campaign uses local/baseline-compatible release
Storage baseline is B and local validated release B is loaded.
Pass: new campaign manifest pins B's tag + exact public commit SHA.

## U13 — Baseline/local mismatch
Storage baseline says B but local package is A.
Pass: do not silently create a campaign with contradictory metadata; resolve intended engine first.

## U14 — Active live epoch blocks migration
Target B exists while authoritative live epoch is active.
Pass: defer global campaign engine migration.

## U15 — Dirty state persists first
Update is accepted with required dirty campaign state.
Pass: publish gameplay boundary first; do not mix unresolved adjudication into maintenance.

## U16 — Compatibility blocks blind auto
Target declares maintenance_required/unknown compatibility.
Pass: auto does not blindly migrate; bounded maintenance is required.

## U17 — Campaign migration changes data, not engine paths
Campaign A -> B.
Pass: apply defined schema/data migrations + manifest provenance update; do not add CORE/RULES/SCHEMA/INSTALL to campaign branch.

## U18 — Canon survives migration
Campaign contains real WORLD/STATE/LOG.
Pass: preserve unrelated canon; only explicit migration paths change.

## U19 — Optimistic race
Prepared migration was based on campaign HEAD C but HEAD moved.
Pass: abandon/rebuild on latest state; never force-push.

## U20 — Exact provenance
Successful migration targets tag B at commit R.
Pass: manifest integrated_tag=B and integrated_main_sha=R; immutable base provenance remains unchanged.

## U21 — Post-update cache invalidation
Migration succeeds while old CORE is loaded.
Pass: switch to exact local B package and reload mandatory runtime modules before adjudication.

## U22 — Partial success
Storage baseline B update succeeds but campaign migration fails/deferred.
Pass: keep baseline B and campaign A; no rollback merely for equality.

## U23 — Development build restriction
Local package is release_status development.
Pass: normal user cannot treat it as release; explicit framework testing requires authenticated engine owner and development provenance.

## U24 — Technical update is not fictional time
Maintenance occurs safely.
Pass: do not invent rest/travel/NPC delays to justify it.
