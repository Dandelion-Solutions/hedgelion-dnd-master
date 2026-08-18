# Runtime selection and storage baseline amendment

Date: 2026-08-18
Status: user-reviewed design amendment, implementation not started
Amends: `2026-08-18-multi-runtime-cache-and-maintenance-continuity-design.md`
Related: `2026-08-18-runtime-package-provenance-amendment.md`

## 1. Purpose

This amendment refines package selection after campaign choice, separates true semantic-version upgrades from silent same-version runtime refreshes, adds ephemeral update-reminder preferences, and replaces the old storage `baseline_version` scalar with portable runtime identity.

Where this amendment conflicts with the parent design, this amendment is authoritative.

## 2. Storage baseline identity

The storage default branch MUST NOT store an environment-specific `current_runtime_root` path.

The storage marker stores portable default runtime identity for NEW campaigns only:

```yaml
storage_format_version: 3
repository_role: campaign_storage
engine:
  baseline:
    version: "0.8"
    package_id: "v0.8"
    source_commit_sha: "<sha|null>"
    package_sha256: "<sha256>"
    adopted_at: "<timestamp>"
```

Meaning:

- `engine.baseline` is the storage owner's accepted default runtime identity for creating new campaigns;
- it does not select or mutate the runtime of an existing campaign;
- `source_commit_sha` and `package_sha256` are provenance of the last baseline artifact recorded in storage metadata;
- `adopted_at` is audit metadata, not ordering authority;
- only the authenticated storage owner may persist changes to `DND_STORAGE.yaml -> engine.baseline`.

An existing campaign always resolves from `MANIFEST.engine.current`, never from storage baseline.

Storage baseline and campaign runtime identity remain independent authorities.

## 3. Three runtime identity layers

The system deliberately keeps three different layers:

```text
DND_STORAGE.engine.baseline
    portable default runtime for NEW campaigns

MANIFEST.engine.current
    portable runtime identity/provenance for THIS campaign

current_runtime_root
    ephemeral local extracted package path for THIS chat/environment
```

`current_runtime_root` is derived from a validated ZIP and never persisted in Git.

## 4. Newer semantic version discovery

When opening an existing campaign, bootstrap first reads `MANIFEST.engine.current.version` and cheaply indexes available supported runtime ZIP metadata.

For the purpose of deciding whether to OFFER a semantic-version update, comparing semantic engine versions is sufficient. The runtime MUST NOT perform source-SHA archaeology merely to decide that an available `0.8` is a newer semantic version than a campaign on `0.7`.

A semantic-version update prompt is shown only when:

- the authenticated user is the creator of the selected campaign branch;
- a supported runtime ZIP with a newer semantic `engine_version` is available in Project Sources/current-chat attachments;
- the target version is not currently suppressed by the ephemeral prompt state described below;
- normal maintenance timing allows asking the question without interrupting an unresolved higher-priority operation.

A non-creator is never offered authority to update another creator's campaign.

## 5. Creator update prompt

For a creator opening an older-version campaign while a newer semantic runtime version is available, offer the update without treating the old campaign as broken.

The choices are:

1. **Update now** — perform the normal authorized campaign engine update to the offered target version.
2. **Remind later** — do not offer this same target version again for 24 hours in the current environment.
3. **Do not remind about this version** — suppress this target semantic version for this campaign for the lifetime of the current environment.

The prompt preference is ephemeral convenience state only. It MUST NOT be written to campaign Git, storage metadata, ChatGPT Memory, or engine files.

Recommended logical key:

```text
(campaign_identity, target_engine_version)
```

Recommended values:

```text
remind_after = <timestamp>
suppress_for_environment = true
```

If the environment/cache disappears, this preference may disappear too. The same question may then be shown again; this is acceptable.

`Remind later` is not a background automation. The runtime simply suppresses the prompt until at least 24 hours have elapsed and re-evaluates at the next natural startup/maintenance opportunity.

A different newer semantic version is a different prompt key. For example, suppressing `0.8` does not suppress a later `0.9` offer.

## 6. If the semantic-version update is not taken

Declining, postponing, or suppressing a newer-version offer leaves the campaign on its current semantic version.

The runtime then resolves that current version normally:

- if a usable package for the current version is available, reuse/extract it and continue;
- if the required current-version package is not available, ask the user to add the matching runtime ZIP;
- for a creator, the availability of a newer ZIP does not remove the option to restore the older runtime and keep the campaign unchanged;
- for a non-creator, restoring the matching current-version package remains the only valid mismatch recovery path.

The player must not be told only that the campaign cannot continue when one of these valid alternatives exists.

## 7. Same-version runtime refresh is silent

A runtime artifact whose semantic `engine_version` and `package_id` match `MANIFEST.engine.current` is NOT a semantic-version upgrade.

Within one semantic version, compatible forward package revisions are treated as cosmetic/maintenance refreshes and are expected to remain file/schema compatible under this design.

No player update prompt is required for a proven forward same-version refresh.

Given recorded campaign source commit A and candidate package source commit B:

- A == B and digest matches -> same exact artifact;
- A == B and digest differs -> suspicious non-deterministic/repacked artifact; do not silently replace;
- A is ancestor of B -> forward same-version refresh; silently prefer B;
- B is ancestor of A -> downgrade candidate; do not silently use B;
- A and B diverged -> no total ordering; do not arbitrarily call either one newer;
- ancestry unavailable because provenance SHA is null -> no automatic forward classification unless exact digest matches.

"Newer SHA" means a descendant commit proven by one bounded server-side compare/ancestry operation. SHA text values and timestamps are never ordered directly.

No commit-history enumeration is required.

## 8. Candidate preference within the same version

The parent design's rule "exact digest wins" is refined as follows.

For candidates matching the campaign's current `version` + `package_id`:

1. validate package shape and provenance metadata;
2. identify exact-digest candidate, if present;
3. identify candidates whose `source_commit_sha` is a proven descendant of recorded `MANIFEST.engine.current.source_commit_sha`;
4. if one candidate is the unambiguous newest descendant/tip among the usable same-version candidates, prefer that forward candidate even when the old exact-digest ZIP is also present;
5. otherwise use the exact accepted digest when available;
6. never silently choose an ancestor/downgrade;
7. never silently choose between diverged forward candidates when no unique newest descendant exists.

This prevents an obsolete exact ZIP from permanently pinning a campaign to an older cosmetic build of the same semantic version.

## 9. MANIFEST refresh behavior

When a forward same-version candidate is selected, the runtime may immediately use it because same-version forward refresh is considered compatible.

If the authenticated user is the campaign creator and a normal coherent campaign write opportunity exists, silently refresh:

```yaml
MANIFEST.engine.current.source_commit_sha
MANIFEST.engine.current.package_sha256
MANIFEST.engine.current.adopted_at
```

No separate player confirmation is required for this metadata refresh.

The MANIFEST update MUST NOT create a special standalone commit merely to record cosmetic package provenance if there is no otherwise valid persistence boundary. It should join the next allowed coherent campaign transaction.

If the current user is not the campaign creator, the same-version forward runtime may still be used, but campaign MANIFEST remains unchanged because the user lacks authority to persist that branch-level engine identity update.

A later creator session may then refresh the stale MANIFEST provenance when appropriate.

## 10. Storage baseline same-version refresh

The same forward-versus-downgrade classification may be applied when resolving `DND_STORAGE.engine.baseline` for New Game.

A newer descendant artifact within the same semantic baseline version may be used for New Game without treating it as a new semantic-version migration.

Only the storage owner may persist updated `engine.baseline.source_commit_sha`, `package_sha256`, and `adopted_at` to the storage default branch.

A non-owner may not rewrite storage baseline metadata merely because a fresher same-version ZIP is available.

## 11. Package provenance source

Candidate source SHA MUST come from the candidate ZIP's builder-generated `RUNTIME_PACKAGE.yaml`, not from resolving a mutable tag name at the current moment.

`RUNTIME_PACKAGE.yaml` is generated as an in-memory ZIP entry and never persisted as a worktree file.

This allows an old `v0.8` ZIP and a refreshed `v0.8` ZIP to coexist and be classified by the source commits that actually produced their bytes.

## 12. Player-facing examples

### 12.1 Creator, campaign 0.7, runtime 0.8 available

Offer succinctly:

```text
Для этой игры используется движок 0.7, а в проекте уже доступен 0.8.
Обновить игру до 0.8?

1. Да, обновить
2. Напомнить позже
3. Не напоминать про 0.8
```

If the creator chooses 2 or 3, continue on 0.7 if its package is available. If it is absent, request the 0.7 runtime ZIP after recording the ephemeral prompt preference.

### 12.2 Non-creator, campaign 0.7, only runtime 0.8 available

Do not offer migration. Ask for the matching 0.7 runtime ZIP.

### 12.3 Campaign recorded old 0.8/A, ZIP 0.8/B available and A is ancestor of B

Silently use B. If the user is campaign creator, refresh MANIFEST provenance at the next allowed coherent write boundary. Do not interrupt gameplay with a cosmetic same-version update question.

### 12.4 Campaign recorded 0.8/B, candidate 0.8/A and A is ancestor of B

Candidate is a downgrade. Do not silently switch to A.

## 13. Validation requirements added by this amendment

Implementation must cover at least:

1. storage marker uses portable `engine.baseline` object rather than only `baseline_version`;
2. existing campaigns resolve only from `MANIFEST.engine.current`, not storage baseline;
3. creator on older semantic version is offered Update now / Remind later / Do not remind about this version;
4. non-creator is not offered campaign migration;
5. `Remind later` suppresses the same `(campaign, target_version)` prompt for 24 hours in current environment;
6. `Do not remind` suppresses only that campaign + target semantic version for current environment;
7. prompt state is never persisted to Git/Memory;
8. environment loss safely permits the prompt to reappear;
9. same-version proven descendant is silently preferred over an older exact-digest package;
10. same-version forward refresh does not prompt the player;
11. creator MANIFEST provenance refresh joins an allowed coherent write rather than forcing a standalone cosmetic commit;
12. non-creator may use a compatible forward same-version runtime but cannot persist MANIFEST refresh;
13. ancestor candidate is never silently used as downgrade;
14. diverged candidates are not arbitrarily ordered;
15. source SHA is read from candidate `RUNTIME_PACKAGE.yaml`, not inferred from current mutable tag position.
