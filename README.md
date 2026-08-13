# Hedgelion D&D Master

Persistent AI Dungeon Master runtime for long-running D&D campaigns in ChatGPT Projects.

The repository is used as persistent read/write storage for the DM framework, campaign state, world entities, indexes, event logs and checkpoints. ChatGPT Project Sources contain only the small bootstrap needed to locate and load this repository. Campaign facts must not be stored in ChatGPT Memory.

## Installation / setup

### 1. Create a ChatGPT Project

Create a dedicated Project for the campaign. The Project is the container for game chats and the small startup configuration.

### 2. Add the Project Instructions

Copy the complete contents of `INSTALL/PROJECT_INSTRUCTIONS.txt` into the Project Instructions field.

These instructions enforce the core runtime rules: no campaign data in ChatGPT Memory, lazy context loading, canonical source priority, and `00_DND_BOOTSTRAP.md` as the only initial entry point.

### 3. Add the bootstrap to Project Sources

Download `00_DND_BOOTSTRAP.md` from this repository and add it to the ChatGPT Project Sources.

Do not add the entire repository to Project Sources. The point of the bootstrap is to keep Project context small and let the agent retrieve only the files needed for the current scene.

### 4. Connect GitHub to ChatGPT

Connect the GitHub app in ChatGPT. Then grant the ChatGPT GitHub App access to this repository.

GitHub installation settings:
https://github.com/settings/installations/

Open the ChatGPT/OpenAI installation, choose **Configure**, and under **Repository access** either select all repositories or explicitly add the campaign repository.

The repository must be available with read/write content access. The agent needs to be able to read, create and update files; otherwise campaign state cannot be maintained automatically.

Never send GitHub passwords, personal access tokens or SSH private keys in the chat.

### 5. Start or move campaign chats into the Project

All campaign sessions should live inside the same ChatGPT Project. At the beginning of a new game chat, the agent must read `00_DND_BOOTSTRAP.md` first, then load only the minimal runtime and current state referenced by it.

## Runtime model

Conceptually:

```
Project Instructions
        |
        v
00_DND_BOOTSTRAP.md       (Project Source)
        |
        v
GitHub repository         (persistent storage)
   |       |       |
 CORE    STATE    INDEX -> WORLD
   |       |             LOG / CHECKPOINTS
   +-------+--------------+
           |
           v
     current working set
```

Project Sources are treated as small, stable startup configuration. GitHub is the persistent database/versioned filesystem. The model context is temporary working memory.

The working context should grow with the complexity of the current scene, not with the age of the campaign.

## Repository layout

The bootstrap defines the authoritative layout. Expected top-level areas are:

- `CORE/` — modular AI Dungeon Master framework.
- `STATE/` — compact current campaign/player/active state.
- `INDEX/` — small lookup indexes for entity IDs and storage paths.
- `WORLD/` — persistent NPC, location, faction, item, lore and secret records.
- `LOG/` — append-only significant event history, segmented into bounded files.
- `CHECKPOINTS/` — canonical campaign checkpoints.
- `INSTALL/` — human-facing setup files.

Do not load all of these directories at startup. Follow the lazy-loading rules in the Project Instructions and bootstrap.

## Canon and persistence

GitHub is the persistent source of campaign data. Significant state changes should be written back to the repository by the agent using the storage protocol defined by the framework.

Git history also provides an audit trail if a later session needs to determine when a fact changed.

Previous ChatGPT conversations are supporting evidence, not the campaign database. If a fact cannot be recovered from canonical storage, the agent must not invent it.

## Current status

The storage architecture is being bootstrapped and the Dungeon Master framework is still under development. Until the initial campaign checkpoint is explicitly marked canonical, exploratory scenes from setup/testing chats should not automatically become campaign canon.
