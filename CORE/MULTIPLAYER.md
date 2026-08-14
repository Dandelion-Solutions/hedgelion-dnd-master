# Shared-World Multiplayer

framework_module_version: 0.1.6
load_when: CAMPAIGN/MANIFEST mode == multiplayer OR explicit multiplayer management

## Mode and ownership

Multiplayer is enabled or disabled only explicitly by the campaign creator.

The creator is determined from Git history: `author.login` of the first campaign-specific initialization commit after branch creation from the engine release. Before changing mode, compare that login with the currently authenticated GitHub user. If they differ, deny the mode change.

`singleplayer` means only that creator may publish gameplay commits to the campaign branch. Other collaborators may observe/read the campaign but must not alter game state.

`multiplayer` permits bound players to publish gameplay commits according to the rules below. Multiple chats/players share one campaign branch and objective world, while each PC/player has separate knowledge.

Repository collaborator access alone is not an existing player binding. The campaign's `players.join_policy` controls whether an eligible collaborator may create a new binding for themselves.

Changing `players.join_policy` is creator-only. If the field is absent in an older campaign, treat it as `invite_only`.

## Authenticated player binding

Before normal multiplayer gameplay writes, resolve the currently authenticated GitHub account and map its stable GitHub user ID to exactly one active `PLAYER_` record. The session `player_id` and controlled `pc_id` must come from that binding, not from self-identification in chat.

Use the stable campaign `PLAYER_` ID inside campaign state and semantic events. GitHub login is a mutable authorization/audit label only and must not be used as the gameplay actor ID.

If repository permission exists but no valid active player binding matches the authenticated GitHub user, normal gameplay writes are not authorized. Apply the joining/rejoining policy below before concluding whether the user may create or reactivate a binding.

## Joining policy

`CAMPAIGN/MANIFEST.yaml -> players.join_policy` is one of:
- `invite_only` — safe default. A new participant may join only when an active `PLAYER_` binding for that GitHub user has already been explicitly created/authorized by the campaign creator. The binding itself is the invitation; no separate invitation table is required.
- `open_contributors` — a currently authenticated repository collaborator with verified write/push access may self-enroll by creating one new `PLAYER_` binding for their own stable GitHub user ID.

`open_contributors` does not mean public anonymous access. A GitHub account that cannot be verified as an eligible current repository collaborator with sufficient write access may not self-enroll. If that eligibility cannot be established reliably, deny self-enrollment rather than guessing.

The open-world self-enrollment exception is intentionally narrow. Before the binding exists, the unbound collaborator may publish only the minimal coherent onboarding batch needed to establish their own `PLAYER_` identity and required index entry. After that write succeeds, ordinary multiplayer authority derives from the new active binding.

Self-enrollment must never:
- claim or modify another player's binding;
- take control of an existing PC;
- change campaign mode, join policy, engine policy or other creator-only state;
- modify unrelated world/gameplay state as part of the authorization exception.

A newly joined player creates or accepts their own PC through normal character setup after identity binding. Existing PC control may change only through an explicit authorized persistent event; joining policy never implies inheritance of an unowned or inactive PC.

The creator may change `invite_only <-> open_contributors` explicitly at any safe persistence boundary. Changing the policy does not revoke existing active player bindings. To remove a participant's gameplay authority, deactivate that player's binding through the membership rules below.

When switching a campaign into multiplayer and no join policy is explicitly chosen, initialize `invite_only`. Do not silently open the campaign merely because repository collaborators exist.

## Leaving, removal and rejoining

Do not physically delete a canonical `PLAYER_` record merely because a participant leaves or is removed. Historical events, PC control history, preferences and provenance may still reference that stable `player_id`.

Membership uses the existing binding `status`:
- `active` — normal multiplayer authority may be granted after authenticated binding validation;
- `inactive` — no normal gameplay authority. Keep the same `PLAYER_` record, GitHub binding and `controlled_pc_ids` unless a separate explicit controller-change event changes them.

Use optional `deactivated_by` to distinguish how an inactive binding was produced:
- `self` — the non-owner participant voluntarily left;
- `creator` — the campaign creator explicitly removed the participant.

If an older inactive binding has no `deactivated_by`, treat it conservatively as creator-deactivated for rejoining purposes.

A bound non-owner player may voluntarily leave by setting only their own binding to `inactive` with `deactivated_by: self`. They may not deactivate another player.

The campaign creator may deactivate any non-owner participant with `deactivated_by: creator`. The creator must not deactivate their own campaign-player binding through this flow. If the creator wants to stop multiplayer participation, use the normal owner-controlled campaign/mode management instead of self-removal.

A membership deactivation is a `HARD` access-control persistence boundary. It becomes effective only after the campaign write succeeds. Do not delete the player from indexes or erase PC/provenance records.

### Rejoining

Always look for an existing `PLAYER_` record bound to the authenticated stable GitHub user ID before considering creation of a new player identity.

If an inactive binding has `deactivated_by: self`, that same authenticated user may reactivate the same binding in either `invite_only` or `open_contributors`. This is a narrow membership write, not new-player enrollment.

If an inactive binding has `deactivated_by: creator` (or legacy/unknown deactivation), only the campaign creator may reactivate it. `open_contributors` does not let a previously creator-removed player bypass that removal by self-enrolling again.

Reactivation sets the existing binding back to `active` and clears `deactivated_by`. Reuse the same `player_id`, `controlled_pc_ids`, preferences, knowledge/provenance links and existing character records. Do not create a replacement PLAYER or a new PC merely because the human returned.

If PC control was explicitly reassigned while the player was inactive, rejoining respects the current canonical controller assignment; it does not silently reclaim a transferred PC. Otherwise the returning player resumes their existing controlled PC(s).

### Deactivation while a live epoch is active

If the target player's controlled PC participates in an authoritative active live epoch, do not leave that epoch writable while revoking membership.

1. Freeze the affected live epoch through the normal `active -> closed` protocol.
2. Compact its durable state.
3. Persist the binding deactivation at the campaign frontier.
4. If the remaining active players still require shared-scene live mode, open/adopt the successor epoch from the new campaign HEAD without the deactivated player as an authorized participant.

Do not delete or teleport the removed player's PC as a technical side effect. The PC remains a canonical world entity in whatever fictional state/location was established; later fictional handling must follow normal agency/world rules.

A stale chat cannot receive an autonomous push notification. Outside live mode, revocation is therefore discovered on the next required campaign synchronization/write boundary. Once the deactivation commit is canonical, a stale session must not successfully publish further gameplay state under the inactive binding. Do not add per-message background polling solely for membership revocation.

## Action provenance

For a durable transition directly initiated by a player, the semantic event records `player_intent.player_id` and the acting `pc_id` when applicable. This is selective causal provenance, not per-turn telemetry.

Example: if a PC takes a unique amulet from a chest, the transfer event records the stable `PLAYER_` ID and PC ID; the item record points to the event through its normal event reference. Do not copy GitHub usernames or player display names into every changed entity file.

If later consequences materially derive from that action, link them through `caused_by_event_ids`. Do not mark unrelated NPC/world/maintenance changes as player-authored merely because the same player's Git commit persisted them.

Git commit authorship is independent audit evidence for who published the batch; semantic event `player_id` is the canonical gameplay attribution.

## Reduce conflicts by structure

Keep independently changing environments in separate records. Each active scene has its own scene file and normally references one location plus the PCs/NPCs/items/processes currently relevant there. Separate players in separate scenes should usually touch different files.

Do not update a global `CURRENT` record for every local movement/action if the scene/entity record is sufficient.

## Shared-scene live frontier

When differently controlled PCs share one actionable scene, use `LIVE_SCENE.md`.

Do not let separate Masters independently improvise mutable versions of the same shared environment. The durable campaign scene opens one temporary live epoch/branch. While that pointer is active, the live state is the authoritative operational frontier for that scene's mutable state and per-PC observed information.

The framework does not depend on detecting online presence: differently controlled PCs sharing the same actionable scene are enough to require live mode.

The live branch uses one runtime-mutated file and a special fast path. Ordinary live synchronization is a live-branch ref probe; if changed, fetch only `CAMPAIGN/LIVE/LIVE_STATE.yaml`. Do not perform campaign compare/history reads for every shared-scene turn.

Campaign branch writes for live-owned scene/entity state are deferred to close-time compaction. Shared live mutations are instead published immediately to the live frontier before narration when another player could observe/use the changed fact.

## Lightweight campaign synchronization reads

Outside an active live-scene hot path, each multiplayer session keeps a cached working-set base HEAD SHA for the campaign branch.

A campaign synchronization probe must be cheap:
1. read only the active campaign branch ref;
2. if HEAD is unchanged, stop — no content or history fetch is needed;
3. if HEAD changed, use server-side `base..HEAD` compare to obtain changed paths;
4. if none of those paths can affect the session's loaded scene/entities, local dirty set, access/mode metadata, or the action being resolved, move the cached base HEAD forward without reloading files;
5. if relevant paths changed, fetch only the exact affected/required records at the new HEAD and refresh the local working set.

All files in one campaign refresh must be pinned to one exact HEAD SHA. Never assemble a shared-world view from multiple branch-relative reads that could observe different commits.

Do not clone/pull the repository or request broad commit history to synchronize ordinary multiplayer play. History is read only for a bounded provenance/conflict/audit reason.

## Synchronization policy

Do not poll the campaign HEAD before every harmless sentence or roll.

Campaign HEAD must be checked:
- before publishing a normal campaign persistence batch;
- before adjudicating an action that targets a known race-sensitive shared object/process not owned by the current live epoch when the local campaign HEAD may be stale;
- after an explicit campaign resync request;
- after any campaign write conflict;
- while opening/closing/compacting a live epoch as required by `LIVE_SCENE.md`;
- before accepting a membership-management write, and again before publishing if the prepared campaign HEAD moved.

When a changed-path refresh touches the current user's `PLAYER_` binding, join policy, mode or other access metadata, revalidate authorization before publishing further gameplay state.

An active shared scene has its own more frequent but cheaper live ref probe defined in `LIVE_SCENE.md`; do not replace that probe with a full campaign refresh.

## When campaign HEAD changed

Compare external changes since the working-set base HEAD with the local dirty set.

If they are independent, incorporate the new HEAD and keep the local outcome.

If they touch the same shared file but independent data, merge structurally.

If they touch the same world entity or mutually dependent environment, fetch the latest state and evaluate logical compatibility.

Never resolve a semantic conflict by blind text merge.

## Logical conflicts

If two actions cannot both be true, already-published canon constrains the later resolution when chronology supports that ordering.

Example: a unique item is removed from a chest by one player's published action. Another player later tries to take it based on stale local state. After resync, resolve the second action from the fact that the chest no longer contains the item; do not overwrite ownership.

If the PC can observe the consequence, narrate it naturally. Identify another character only if the PC has an in-world basis to know who acted; Git author/session metadata is DM evidence, not automatic character knowledge.

If two actions are fictionally simultaneous and commit order alone would arbitrarily decide a contested outcome, adjudicate under game rules/world timing rather than letting Git order decide the fiction.

## Publish boundaries

Private/local changes may be batched until a natural persistence boundary.

Outside a live epoch, publish race-sensitive shared changes promptly after logical completion: unique object ownership/destruction, persistent shared-location changes, shared NPC relocation/death, global process advancement, access/lock/door state, scarce shared resource consumption, etc.

Inside an active live epoch, use the live-state publication rules instead: the shared operational change is written to the live branch before narration and later compacted into one durable campaign batch.

This is a visibility requirement for the shared world, not a requirement to commit every non-shared turn.

## World chronology

Use `CHRONOLOGY.md` when relative order between scenes/events/processes materially affects a ruling or reconciliation.

Do not force all players/scenes onto one minute-by-minute clock. Separate scenes may advance along independent local chronology frontiers while they are causally independent. Their relative order may remain undefined.

Synchronize/reconcile chronology only when it becomes material, for example when:
- an event/process in one scene causes or enables something in another;
- information, an NPC, item, message, spell effect, pursuit, deadline or other state crosses scene boundaries;
- two scenes converge or participants try to meet/intercept each other;
- a global/shared process constrains both scenes;
- persisted event order would otherwise violate causality or established lore.

When reconciling, establish the minimum relative ordering necessary. Cause must precede effect; a required entity/fact must exist before use; knowledge must follow a valid source. Independent events need not receive artificial timestamps or a total order.

Git commit order is not automatically fictional chronology. If actions are genuinely simultaneous/contested, adjudicate under rules/world logic. If exact elapsed time is not a material stake, ordinary travel/scene duration may remain approximate and should not trigger minute-level accounting.

`CURRENT.world_time.frontier` represents only compact globally reconciled chronology, not a requirement that every active scene share one exact timestamp. Local scene frontiers remain local until a cross-scene dependency makes them relevant.

A cross-scene event that materially touches more than one active live epoch is an exceptional synchronization boundary; follow `LIVE_SCENE.md` and `CHRONOLOGY.md` rather than adding distributed multi-branch transaction overhead to normal play.

## Privacy

DM may load private facts required to resolve objective world state, but player-facing narration must respect PC/player knowledge boundaries.

A live scene stores objective shared truth separately from which PCs actually perceived/learned each relevant fact. Repository visibility is not character knowledge.

## Joining players

Joining is governed by `players.join_policy` plus authenticated GitHub identity and persistent `PLAYER_` binding state.

Before treating somebody as a new player, search the player index for an existing binding to the same stable GitHub user ID. An inactive existing binding follows the rejoining rules above and must not produce a duplicate PLAYER/PC.

In `invite_only`, a never-bound collaborator remains an observer until the creator has explicitly established their binding. In `open_contributors`, an eligible never-bound collaborator may establish only their own binding through the narrow onboarding exception above.

Adding a genuinely new player never implies control of an existing PC. After binding, create/assign a PC explicitly through normal character setup.

If a newly joined/resumed PC enters a scene with an active live epoch, load/adopt that live frontier before presenting current actionable state.
