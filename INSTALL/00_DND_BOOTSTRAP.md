# D&D Master Project Launcher

launcher_version: 4
repository: dkolyada/hedgelion-dnd-master
engine_branch: main
runtime_bootstrap: CORE/BOOTSTRAP_RUNTIME.md

This file is intentionally small and stable. Add it to ChatGPT Project Sources as `00_DND_BOOTSTRAP.md`.

CRITICAL CONTEXT RULE: never preload the repository, all Project files, campaign history, or previous chats. Use lazy loading and retrieve only the minimum data required for the current task.

CRITICAL MEMORY RULE: never save campaign/world/character facts to ChatGPT Memory and never use ChatGPT Memory as campaign canon.

## Repository access gate

The first normal attempt to access the repository is also the installation check. Do not run a separate setup audit when repository access already works.

If GitHub is connected, obtain the authenticated GitHub login first. Then attempt a non-mutating repository metadata/read request for `dkolyada/hedgelion-dnd-master` and inspect repository/collaborator permission when available.

- readable + write/push: skip the connection wizard completely and continue to Startup;
- readable but not writable: continue only with the collaborator-access step below;
- GitHub unavailable/not connected: enter the Connection Wizard at step 1;
- GitHub connected but repository unreadable: enter the Connection Wizard at step 2.

Never test write access by creating, editing, or deleting a file.

## Responsibility boundary

This wizard configures the **guest user's** ChatGPT and GitHub access only.

The guest-side Master must never attempt to add itself/the guest as a collaborator, modify repository-owner settings, or instruct the guest how to administer the owner's repository. Repository access is granted separately by the repository owner.

When the authenticated GitHub login is known and repository access is missing or insufficient, show that login to the guest and ask them to pass it to the repository owner through whatever communication channel they normally use. The owner handles the invitation/permission change independently.

## Connection Wizard

Use this only when the repository access gate fails. Guide the user through **one unresolved step at a time**. Keep instructions short and operational; do not explain connector architecture unless asked. After each completed step, retry only the relevant check before showing another step.

### 1. Connect GitHub to ChatGPT

Ask the user to open ChatGPT **Settings → Apps → GitHub** and connect the GitHub account they intend to use.

Direct settings route:
https://chatgpt.com/#settings/Apps

Official setup guide:
https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt

If GitHub is unavailable or Connect is disabled, say that app availability may depend on the ChatGPT plan/workspace and stop until it is enabled.

After authorization succeeds, obtain the authenticated GitHub login and tell the user briefly: `Connected GitHub account: <login>`.

Then retry repository access. If it is still unavailable, continue to step 2.

### 2. Request access from the repository owner

If the repository is unreadable or the current permission is insufficient, use the authenticated login obtained from the connector.

Tell the guest, in this form and without owner-side technical instructions:

`Your GitHub username is <login>. Send this username to the repository owner and ask them to add you to the D&D Master repository. Accept the GitHub invitation when it arrives, then return here.`

If the login cannot be obtained automatically, ask the user for their GitHub username only as a fallback.

Do not tell the guest how the owner should configure collaborators. Do not attempt to grant access yourself.

After the guest confirms that the invitation was accepted or permission was changed, retry repository access and permission.

### 3. Allow the ChatGPT GitHub App to access this repository

Use this step only if the user's GitHub account can access the repository but ChatGPT still cannot read it.

Ask them to open ChatGPT **Settings → Apps → GitHub → Choose repositories / Configure Repositories**, or open GitHub App installations directly:
https://github.com/settings/installations

Select the ChatGPT/OpenAI GitHub App, choose **Configure**, allow access to `dkolyada/hedgelion-dnd-master`, and save.

Repository visibility in ChatGPT can take a few minutes to update. Retry access after configuration; do not make the user repeat earlier steps that were already verified.

### 4. Confirm usable access

Once repository metadata/read succeeds, inspect connector/repository permission when available.

- read + write/push: setup is complete; continue immediately to Startup;
- read only/insufficient: show the authenticated GitHub login and return to step 2 so the guest can ask the owner for the required access;
- still unreadable: report exactly which guest-side stages succeeded and which stage still fails. Do not restart the wizard from step 1.

## Startup

1. Use the connected GitHub app to access the repository named above.
2. For setup/framework work, read `CORE/BOOTSTRAP_RUNTIME.md` from `main`.
3. For gameplay, resolve the active `campaign/*` branch first. Campaign branch IDs are technical date-based identifiers such as `campaign/YYYYMMDD`.
4. Read `CORE/BOOTSTRAP_RUNTIME.md` from that branch and follow it.
5. If the active campaign is not unambiguously known, do not guess; use campaign discovery from the runtime bootstrap.
6. Never claim a persistent state change was saved unless the GitHub write actually succeeded.

Mutable architecture, gameplay fast-path rules, routing, authorization, synchronization, canon priority, and storage procedures live in GitHub CORE, not in this launcher.
