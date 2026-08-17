# HDM Development Agent Instructions

## Scope

This file governs **development work on the HDM engine repository**.

It is not part of the HDM game runtime, campaign runtime, player-facing
bootstrap, campaign storage protocol, or release behavior.

Gameplay must not depend on this file and must not load it as part of the HDM
runtime instruction set. Gameplay transport and persistence rules are defined
by the dedicated game Project Instructions and bootstrap.

## GitHub transport policy

For HDM development in ChatGPT Work / Codex environments with connected GitHub
Connector access:

```text
NATIVE_GIT_REMOTE = NATIVE_GIT_UNAVAILABLE
GITHUB_REMOTE_TRANSPORT = CONNECTOR_REQUIRED
```

This is a repository-level capability decision based on completed environment
diagnostics. It is not a transient failure and MUST NOT be re-tested during
ordinary development tasks.

### Mandatory rule

Use the connected **GitHub Connector** for all communication with the remote
GitHub repository, including:

- reading remote refs and branch HEADs;
- reading commits, trees, blobs, and repository files;
- comparing remote commits or refs;
- creating or updating branches;
- creating blobs, trees, and commits;
- updating remote refs;
- creating or updating repository files;
- pull-request and issue operations.

Do not use native Git or GitHub CLI as an alternative remote transport.

## Prohibited remote operations

In this environment class, do **not** use commands such as:

```text
git clone
git fetch
git pull
git push
git ls-remote
git remote update
gh ...
```

Do not use `curl`, Python HTTP clients, credential injection, temporary tokens,
credential helpers, SSH setup, or other mechanisms to bypass the Connector for
GitHub repository transport.

Do not probe native Git authentication before using the Connector.

Do not retry native Git after a Connector failure.

If the Connector cannot perform a required repository operation, report the
specific Connector capability gap instead of falling back to another GitHub
transport.

## Local Git is allowed

The prohibition applies to **remote GitHub transport**, not to Git itself.

When a valid local checkout is available, local Git operations are permitted
and should be used when useful, including operations such as:

```text
git status
git diff
git diff --cached
git log
git show
git rev-parse
git branch
git merge-base
git merge
git rebase
git cherry-pick
git add
git restore
git checkout
git commit
```

These operations may be used for local inspection, conflict analysis,
conflict resolution, patch preparation, history analysis, staging, local
commits, and other work that does not communicate with GitHub.

A local Git command MUST NOT implicitly contact a remote repository.

When an operation may contact a remote depending on configuration, do not use
it unless it is explicitly constrained to local data.

## Conflict-resolution workflow

For merge or rebase conflict work:

1. obtain authoritative remote refs, commits, and required file content through
   the GitHub Connector;
2. use local Git and filesystem tools freely to inspect and resolve conflicts in
   the working tree;
3. verify the resulting local tree and diff locally;
4. publish the resulting repository objects through the GitHub Connector.

Do not perform `git fetch`, `git pull`, or `git push` as part of conflict
resolution.

## Remote state is authoritative

Do not assume that a local checkout represents the current remote state.

Before any operation whose correctness depends on the current branch HEAD,
verify the relevant remote ref through the GitHub Connector.

For remote writes:

1. read the current target ref through the Connector;
2. construct the intended commit from the expected parent;
3. update the ref through the Connector without force unless an explicit task
   requires otherwise;
4. verify the resulting remote ref through the Connector before claiming that
   publication succeeded.

A successful local commit is not proof that the remote repository changed.

## Connector publication pattern

When a multi-file change must be published and an ordinary file-update API is
not sufficient, use the GitHub Connector Git-data workflow:

```text
read current ref
-> create blobs
-> create tree based on the current tree
-> create commit with the expected parent
-> update ref
-> read ref again for verification
```

Use Connector-native higher-level operations when they provide the required
semantics more directly.

## Capability cache

The following result is considered cached for this environment class:

```text
environment:
  ChatGPT Work / Codex
github_authentication:
  connector-backed
native_git_remote:
  NATIVE_GIT_UNAVAILABLE
remote_transport:
  GitHub Connector
retry_native_git:
  false
```

A new chat, new task, new branch, new checkout, or new repository operation does
**not** invalidate this decision.

Re-evaluate native Git remote capability only when at least one of these is
true:

1. the user explicitly requests a new native-Git investigation;
2. the execution surface materially changes away from the diagnosed ChatGPT
   Work / Codex connector-backed environment;
3. native Git credentials are explicitly provisioned through a supported
   mechanism;
4. the environment explicitly provides a supported authenticated Git remote
   transport and the user authorizes its verification.

Until one of these conditions occurs, do not spend tool calls or execution time
testing native Git remote access.

## Maintenance audit

For explicit HDM engine development/release maintenance, the canonical audit
entry point is:

```text
TOOLS/run_maintenance_audit
```

Use that command instead of manually selecting a virtualenv, installing
maintenance packages, or invoking `TOOLS/audit_engine.py` directly. The launcher
owns the isolated `.hdm-maintenance/` cache and reads dependencies from
`TOOLS/requirements-maintenance.txt`.

Do not install maintenance dependencies into the system Python. Do not make the
gameplay runtime depend on the maintenance environment.

## Development versus gameplay

This file defines **development tooling policy only**.

Do not copy these development instructions into HDM gameplay prompts or runtime
CORE context.

Do not modify the gameplay Project Instructions or gameplay bootstrap merely to
mirror changes in this file.

The game runtime has its own transport and persistence contract and remains
independent from this development-agent policy.
