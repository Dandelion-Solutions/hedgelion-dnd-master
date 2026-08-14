# Engine Update Regression Cases

These cases verify tagged release discovery and safe campaign integration without adding polling to ordinary gameplay.

## U01 — Untagged main commits are invisible
`main` contains many commits newer than the campaign's integrated release, but no newer valid engine tag exists.
Pass: report no campaign engine update. Do not offer or integrate `main` HEAD.

## U02 — New tagged release discovered at startup
Campaign integrated release is `v0.1-beta`; a valid later release tag exists.
Pass: creator startup performs one release-tag discovery opportunity and identifies the tagged release without polling `main` during later ordinary turns.

## U03 — Ask policy presents three choices
A newer tagged release is available and manifest policy is `ask`.
Pass: creator is offered `Update`, `Not now`, and `Always update automatically`. No campaign-wide update choice is asked of a non-owner multiplayer participant.

## U04 — Not now is temporary
Creator chooses `Not now` for target tag T.
Pass: continue on current engine; do not repeatedly ask about T during ordinary turns in the same continuous gameplay session. Offer T again at a later startup/resume or explicit update/maintenance opportunity.

## U05 — Always auto persists policy
Creator chooses `Always update automatically`.
Pass: persist campaign engine `update_policy: auto` at a safe boundary. Future compatible tagged releases may integrate automatically when safety preconditions pass.

## U06 — Auto does not run on a timer
Campaign is active for hours with no startup/resume, explicit update request, maintenance opportunity or rollover.
Pass: no background/wall-clock release polling occurs. Current tagged engine remains valid until a later update opportunity.

## U07 — Active live epoch blocks global update
A newer compatible tag exists while any authoritative live epoch in the campaign remains `active`.
Pass: do not integrate the engine release. Defer to a later safe opportunity; never let simultaneous live epochs use different campaign engine versions because one session updated mid-epoch.

## U08 — Rollover can expose an update opportunity
Creator closes/compacts the relevant live epoch and no other active live epoch remains. Shared scene still needs a successor epoch.
Pass: tagged update discovery/integration may occur after durable compaction and before opening the successor. If update succeeds, successor opens from the updated campaign HEAD.

## U09 — Dirty gameplay state is persisted first
A tagged update is accepted while current campaign state has a required dirty durable batch.
Pass: establish a clean durable campaign frontier before engine integration; do not mix unresolved gameplay adjudication into the engine maintenance commit.

## U10 — Exact tag, never arbitrary main
Target release is tag T at commit R; `main` has additional commits after R.
Pass: integration takes engine content from exact R/T only. No post-tag main content enters the campaign.

## U11 — Campaign data survives tagged integration
Target release contains the normal empty/template `CAMPAIGN/` skeleton while the campaign branch contains real PCs, NPCs, state and logs.
Pass: preserve populated campaign data. Do not overwrite it from the release skeleton. Modify campaign records only for explicit safe engine metadata or a defined migration.

## U12 — Engine-path local customization blocks blind auto
Campaign branch independently modified an engine-owned path also changed between installed release and target tag.
Pass: automatic integration stops and enters bounded maintenance/conflict resolution. Do not overwrite the local engine customization silently.

## U13 — Compatibility marker blocks unsafe auto
Target tagged `ENGINE_VERSION.yaml` declares `campaign_update.compatibility: maintenance_required`, or the marker is absent/unknown.
Pass: `auto` does not blindly install it. Ask creator/perform bounded migration at a safe boundary.

## U14 — Optimistic publish race
Update tree was prepared from campaign HEAD C, but another authorized campaign commit moves HEAD before publication.
Pass: non-force ref update is rejected/abandoned; refresh relevant state and re-evaluate. Never force-push the prepared update.

## U15 — Successful update records provenance
Campaign updates from tag A to tag B.
Pass: one coherent merge-style maintenance commit records B in `engine.integrated_tag`, B's exact source commit in `engine.integrated_main_sha`, keeps immutable `base_tag/base_sha`, and uses the tagged release commit as merge provenance.

## U16 — Post-update engine cache invalidated
A tagged update succeeds while the current chat already loaded old CORE modules.
Pass: repin campaign HEAD; reload bootstrap/core runtime modules required before next adjudication. Do not continue using cached old engine rules.

## U17 — Older manifest defaults safely
An existing campaign lacks `integrated_tag` and `update_policy`.
Pass: policy defaults to `ask`. Derive installed tag only from an unambiguous existing release-tag/SHA relation; otherwise require one maintenance adoption and never guess/auto-update.

## U18 — Non-owner multiplayer session does not govern engine
A bound multiplayer participant who is not campaign creator starts play while a newer release exists.
Pass: continue using campaign-integrated engine; do not ask that player to choose campaign-wide update policy and do not publish engine integration from that session.

## U19 — Auto failure does not fabricate success
Auto update preparation creates temporary blobs/tree/commit but final campaign ref update fails.
Pass: campaign remains on old engine; temporary unattached Git objects are non-authoritative; Master does not claim the update succeeded.

## U20 — Automatic maintenance is not fictional time
A safe engine update occurs during a maintenance opportunity.
Pass: do not invent rest, night, travel, NPC delay or off-screen events merely to justify technical work. Successful silent auto-update need not interrupt narration; material blocking/failure may be stated briefly outside fiction.
