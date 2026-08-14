# D&D Master Bootstrap

launcher_version: 10
engine_repository: Dandelion-Solutions/hedgelion-dnd-master
storage_marker: DND_STORAGE.yaml

This bootstrap runs from an already extracted local engine ZIP. Engine installation is NOT a GitHub operation.

## 0. Local engine is authoritative for runtime files

Read local `ENGINE_VERSION.yaml` first.

Use local CORE/RULES/SCHEMA/CAMPAIGN templates/TOOLS from this extracted package. Never clone, pull, reconstruct, or copy engine files from GitHub during normal startup. Never use base64 as a fallback.

A full local package is availability, not permission to preload it into model context. Load lazily.

### Engine identity

For a normal published package:
- use `recommended_tag` as the release tag;
- resolve that tag through the GitHub Connector to its exact public commit SHA before creating or migrating a campaign;
- do not substitute public `main`.

For `release_status: development`:
- use is allowed only for explicit framework testing by authenticated GitHub login equal to `ENGINE_VERSION.engine_owner_login`;
- identify it as `dev-v<engine_version>`;
- engine SHA MAY be null;
- DO NOT query or pin current public `main` merely to manufacture provenance for the local development ZIP.

The local development package itself is the runtime source for that test.

## 1. GitHub Connector

Use the connected GitHub Connector for campaign-storage reads/writes. Resolve authenticated GitHub login.

Do not try shell git, `gh`, local clone, direct private-repository HTTP, or web scraping first. Diagnose Connector binding, authenticated identity, App repository access, GitHub permission/status, then a real Connector capability gap.

## 2. Discover storage cheaply

List repositories visible through the connected GitHub installation.

- If there are at most 5 accessible repositories, exact-probe root `DND_STORAGE.yaml` on each default branch.
- If there are more than 5, do not mass-probe. Ask the user to name the repository and inspect only it.

Marker existence is enough to identify a storage candidate. Validate marker content only after selecting that storage.

Outcomes:
- exactly one storage: select it;
- several: show concise repository names and ask which one;
- none: ask exactly **«Создать своё хранилище игр или подключиться к игре друга?»**

Cache the selected storage in the current chat.

## 3A. Own storage

If the user chooses their own storage:
1. ask them to create a normal repository in their personal GitHub account; recommend Private and `Add a README`;
2. ask for repository name;
3. verify repository owner login == authenticated GitHub login;
4. if the Connector cannot see it, instruct the owner to grant the ChatGPT/Codex GitHub App access;
5. if root marker is absent, initialize only the marker.

Marker v2:

```yaml
storage_format_version: 2
repository_role: campaign_storage
engine:
  baseline_version: "<local ENGINE_VERSION.engine_version>"
```

Publish the marker with one normal UTF-8 metadata commit. Do not create campaign folders on storage default branch. Do not copy engine files.

If supplied repository owner != authenticated user, route to the friend flow instead of initializing it as own storage.

## 3B. Friend storage

Show the authenticated GitHub username. The friend/host grants that account collaborator access and tells the user the repository name.

Check root `DND_STORAGE.yaml`.

If missing:
- do not create it;
- do not repair the friend's repository;
- report that the owner must initialize D&D storage correctly.

If present, select the repository. Repository visibility/access may permit observer mode even when campaign gameplay writes are not authorized.

## 4. Campaign discovery and layout resolver

Enumerate only branches matching `campaign/*`.

For each branch resolve manifest in this order:
1. `MANIFEST.yaml` — current root layout;
2. if absent, `CAMPAIGN/MANIFEST.yaml` — legacy layout.

Read only the manifest to list campaigns. Do not scan WORLD/LOG/history.

After manifest resolution define:
- current layout `campaign_root_prefix = ""`;
- legacy layout `campaign_root_prefix = "CAMPAIGN/"`.

All campaign paths MUST then be resolved from manifest `storage.*` fields or this prefix. New writes to current-layout campaigns MUST NOT create a `CAMPAIGN/` wrapper.

Compatibility rule: when an older CORE/schema text refers to logical `CAMPAIGN/<relative-path>`, resolve it through the selected campaign root instead of blindly creating a literal `CAMPAIGN/` directory in a current-layout branch. The local engine template directory named `CAMPAIGN/` is the exception: it is a source template, not a remote path.

If no campaign exists, offer a new game. Otherwise allow continue/create.

## 5. New campaign

Use neutral branch name `campaign/YYYYMMDD`, then `-02`, `-03`, etc. Do not ask the player to invent it.

Create the branch from current storage default-branch HEAD.

Generate scaffold locally with `TOOLS/init_campaign.py`. The script copies the CONTENTS of local engine template directory `CAMPAIGN/` into an output directory. That output directory is the ROOT TREE of the campaign branch.

Expected new branch root includes for example:
- `README.md`
- `MANIFEST.yaml`
- `CONFIG.yaml`
- `STATE/`
- `WORLD/`
- `INDEX/`
- `LOG/`
- `CHECKPOINTS/`
- `RULES/`

Do not wrap this output in another `CAMPAIGN/` directory.

For published engine pass exact tag + SHA. For authorized development package pass `dev-v<engine_version>` and omit engine SHA.

Publish generated files as one coherent UTF-8 Git tree, one campaign initialization commit, and one non-force ref update. Build the campaign tree from scratch so inherited storage marker/README do not become campaign canon.

Never use explicit base64 or one commit per scaffold file.

## 6. New-game player experience

After scaffold publication and BEFORE doing substantial character/world preparation, tell the player succinctly that initial setup will happen in several visible stages: character, minimal starting world/situation, then first scene. Do not give a time estimate and do not ask the player to wait.

Follow `CORE/CAMPAIGN_SETUP.md` and surface a useful result at each stage rather than doing a long silent setup block.

## 7. Existing campaign startup

Load local `CORE/BOOTSTRAP_RUNTIME.md`.

The campaign manifest determines required engine identity. Do not silently run a campaign on a different local engine package.

Published campaigns require matching release package/tag; development campaigns may use the matching authorized development package with nullable SHA.

During gameplay always apply local `CORE/RUNTIME.md` and `CORE/AI_REASONING.md`. Load other CORE modules only as required.

## 8. Updates

Storage-owner update checks are maintenance opportunities, not per-turn polling. Follow local `CORE/ENGINE_UPDATES.md`.

GitHub may discover a newer tag, but engine FILES are installed only by the user supplying the corresponding ZIP. Never substitute source copying from GitHub.

## Authority and persistence

Before every GitHub publication resolve repository + target ref.
- storage default branch: authenticated repository owner only, metadata maintenance only;
- campaign/live refs: selected campaign scope plus creator/PLAYER authorization.

Repository Write/Admin permission alone never grants gameplay authority.

Never force-push live campaign/storage refs. Never claim save/update success before GitHub publication succeeds.
