# Engine Update Regression Cases — Runtime Release Asset

These are architecture-level regression/acceptance cases. Executable realization remains deferred to approved implementation planning.

## U01 — Untagged main is not player release
Pass: normal players are never offered public main HEAD as a released runtime.

## U02 — New tag discovery is metadata only
Pass: report release availability only as discovery; matching validated local runtime Release Asset is still required.

## U03 — Missing target runtime asset
Pass: request matching supported `hedgelion-dnd-master-runtime-v<version>.zip`; no clone/pull/source copy and no substitution with GitHub-generated source archives.

## U04 — Ask choices
Pass: creator receives current configured update choices (Update now / Remind later / Do not remind about this version) without persisting reminder preference into campaign/storage canon.

## U05 — No polling
Pass: no per-turn/background release checks.

## U06 — Guest skips owner maintenance
Pass: guest does not update storage baseline/storage format or creator-owned campaign engine/ruleset identity.

## U07 — Guest exact package
Guest campaign needs exact adopted A, only unrelated B is local.
Pass: do not silently use B. Use B only if exact-target compatibility is affirmatively proven `DIRECT_COMPATIBLE` without creator-owned mutation; otherwise require a supported current/compatible artifact.

## U08 — Baseline metadata only
Storage owner adopts baseline B for New Game.
Pass: only `DND_STORAGE.engine.baseline` changes in the storage-default transaction; zero engine files and zero existing-campaign mutation.

## U09 — Baseline does not mutate campaigns
Pass: campaign A stays A until a separate creator-authorized direct-compatible use/adoption/migration path applies.

## U10 — Published new campaign provenance
Baseline/local published B is selected for New Game.
Pass: new campaign manifest receives exact package provenance/digest and exact resolved ruleset-set identity from the validated package under WP-19; storage baseline remains only a New Game default.

## U11 — Development package provenance
Local package `release_status: development` and authenticated user is engine owner.
Pass: explicit framework testing may use development identity under development-package rules. Do not query/pin current public main merely to manufacture artifact provenance.

## U12 — Development package forbidden to normal user
Pass: development package cannot be treated as a normal released player package.

## U13 — Active live epoch blocks migration
Pass: defer campaign migration until affected LIVE mutable authority is closed and reconciled.

## U14 — Dirty state persists first
Pass: establish the owner-required clean/recovery-safe durable frontier before maintenance/migration.

## U15 — Coarse compatibility blocks blind auto
`campaign_update.compatibility` says maintenance required/unknown.
Pass: run bounded exact-target compatibility evaluation; coarse metadata alone never authorizes auto-adoption or migration.

## U16 — Migration changes declared campaign data only
Pass: apply only explicit edge-declared campaign schema/native transformations plus allowed current-identity projections; never copy engine files into campaign storage.

## U17 — Released layout preservation
A released v1.0+ campaign on source layout A adopts target B.
Pass: migration preserves source layout unless an applicable explicit migration edge declares a layout transformation. This case does not imply compatibility with pre-release/v0.8 layouts.

## U18 — Canon survives migration
Pass: unrelated WORLD/STATE/LOG/native authority, stable IDs, chronology/history and owner semantics are preserved.

## U19 — Optimistic race
Campaign HEAD moves after migration preparation.
Pass: prepared basis is stale; rebuild/re-evaluate from current authority. Never force-push or silently merge prepared migration onto the moved head.

## U20 — Post-update full CORE cache rebuild
Campaign successfully adopts/migrates engine A -> B.
Pass: only after confirmed campaign publication bind exact local package B, invalidate the whole old engine instruction/runtime cache, then preload/rebuild the complete B runtime context required by current bootstrap rules before further adjudication. Campaign data not required by the active working set remains lazy.

## U21 — Separate-authority partial success
Storage baseline/storage-format operation succeeds, campaign migration is deferred/rejected.
Pass: storage result remains its own authoritative result; campaign remains on its current authoritative state. Neither transaction silently rolls back or authorizes the other.

## U22 — Technical update is not fictional time
Pass: do not invent rest/travel/NPC delay or other fictional events for maintenance.

## U23 — No mixed engine context
After successful migration/adoption to B, old-A CORE text remains cached while new-B files are available.
Pass: invalidate old engine instruction/runtime cache and rebuild B context before gameplay; never adjudicate with mixed package instructions.

## U24 — GitHub source archive is not a runtime package
A GitHub-generated repository source ZIP contains nested `GAME/ENGINE_VERSION.yaml` plus development material.
Pass: package validation rejects it; the user must provide the custom runtime Release Asset.

## U25 — Multi-axis equality is not compatibility proof
Campaign and target happen to have equal `campaign_contract_generation`, local schema versions and ruleset compatibility generation.
Pass: equality alone does not yield `DIRECT_COMPATIBLE`; exact target support must affirm the relevant source envelope.

## U26 — Version order does not create migration path
Campaign engine A is semantically older than target B, but target B ships no applicable explicit migration edge and does not affirm direct compatibility.
Pass: `UNSUPPORTED_INCOMPATIBLE`; never infer an A->B transform from engine-version/generation order.

## U27 — Same-version descendant is provenance, not released compatibility
Released campaign accepted package A. Different released package bytes B have the same engine version/package ID and B's source commit descends from A.
Pass: ancestry alone does not authorize silent use. Exact target B must affirm direct compatibility or an explicit migration/maintenance relation.

## U28 — Ambiguous migration paths
Two distinct valid edge compositions from source S to exact target T remain and T declares no canonical path/order.
Pass: `INDETERMINATE`; do not choose shortest/newest/lexical path.

## U29 — Unsupported newer persistent contract
Older runtime encounters a newer campaign/schema/ruleset/storage contract that it does not explicitly support.
Pass: fail closed. Parse success or numeric decrement is not compatibility and no guessed reverse edge is selected.

## U30 — CLOSED LIVE awaiting absorption blocks migration
No LIVE epoch is active, but a CLOSED epoch still has required state awaiting branch absorption/reconciliation.
Pass: migration is blocked until absorption/current branch authority is complete.

## U31 — Accepted resumable work incompatible with target
Campaign records parse under target B, but a current accepted Resolution/Continuation freezes ruleset/package/RNG/causal evidence B cannot safely interpret.
Pass: migration/adoption blocks. Do not ambient-rebind, reroll, discard the accepted closure or reconstruct hidden reasoning.

## U32 — Publication rejection is not migration success
Migration transforms and validates locally, but campaign ref CAS is rejected because HEAD moved.
Pass: current ref remains authority; prepared objects have no campaign authority; no success is reported.

## U33 — Ambiguous publication uses read-back
Migration ref update returns an unknown/ambiguous transport result.
Pass: bounded authoritative ref read-back determines accepted/rejected/indeterminate. Never blind-retry the authority-changing publication.

## U34 — Reverse requires explicit edge
Campaign successfully migrated A -> B. User later requests B -> A.
Pass: old ref/checkpoint is not generic rollback authority. Downgrade is possible only with a separately supported explicit reverse edge/path and publishes as a new forward creator-authorized transaction.

## U35 — Derived versus HOT rebuild timing
Target migration changes native authority used by a branch-persistent index and a local HOT/SQLite cache.
Pass: rebuild target-required branch-persistent derived/index projection from prepared migrated authority before campaign publication when its owner requires it; rebuild/invalidate local HOT cache only after confirmed authoritative success.

## U36 — Migration evidence is not publication authority
Prepared migration evidence says validation succeeded, but ref publication fails or remains indeterminate.
Pass: evidence does not make the migration current. Campaign ref/CAS/read-back remains authority; no self-contained “migration succeeded” marker overrides it.

## U37 — Missing immutable edge artifact
Target metadata names a migration edge but the exact immutable transform/support artifact required by that edge is absent or invalid.
Pass: path is unusable; classify unsupported/indeterminate according to whether absence or evidence uncertainty is proven. Never fetch mutable latest/main as a substitute.

## U38 — Storage prerequisite does not confer campaign authority
Storage owner successfully migrates storage format required by target B but is not the creator of campaign C.
Pass: storage prerequisite is satisfied; storage owner still cannot transform/adopt campaign C. Creator authorization remains required.

## U39 — Pre-release compatibility is absent
A v0.8/pre-release campaign/scaffold is presented to the released-v1.0+ migration evaluator.
Pass: no compatibility/migration obligation is inferred from historical docs or old examples. Current WP-20 released compatibility horizon starts at v1.0.
