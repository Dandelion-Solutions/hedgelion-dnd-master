# R2.6 Owner Clarification — Fixed Gameplay Repository Transport

Status: **OWNER-APPROVED CLARIFICATION / SUPERSEDES R2.6 TRANSPORT-SELECTION LANGUAGE**

Date: 2026-08-24

Applies to:

- `DEV/docs/superpowers/design/2026-08-24-r2-6-chatgpt-plus-assurance-task-brief.md`;
- prior repository-transport feasibility research where it is broader than the current product decision;
- later R2.6 evidence, probes, Decision Briefs and assurance classification;
- R2.7 runtime/instruction/test mapping.

This clarification does not implement runtime code or change gameplay persistence semantics. It narrows the assurance question to the already-selected transport path.

---

## 1. Owner clarification

R2.6 SHALL NOT reopen repository-transport selection.

The supported gameplay path is fixed:

```text
DETERMINISTIC PYTHON / CORE
    prepare/freeze publication state
    compute/validate exact semantic delta
    own transaction semantics/currentness/retry decision
        |
        v
CHATGPT GITHUB CONNECTOR
    perform the defined remote GitHub transport operations only
        |
        v
AUTHORITATIVE NON-FORCE REF TRANSITION
```

For ordinary campaign publication the existing runtime transport profile remains:

```text
create_tree(base pinned tree, dirty delta)
-> ref check
-> create_commit(parent pinned HEAD)
-> update_ref(force=false)
```

`GAME/CORE/PERSISTENCE.md` remains the runtime HOW owner for this sequence.

---

## 2. Forbidden gameplay/runtime transport experiments

During gameplay, setup, save, recovery, multiplayer synchronization or assurance probes for the supported profile, HDM SHALL NOT try, probe, or fall back to:

- shell/native remote `git`;
- `gh` / GitHub CLI;
- `git clone`, `pull`, `fetch`, `push`, `ls-remote` or remote SSH Git;
- direct private-repository HTTP/GitHub API calls from Python/container;
- credential/token workarounds;
- ad-hoc GitHub App/MCP/custom write-service alternatives;
- GitHub Actions as an improvised gameplay persistence bridge;
- local-commit-to-transparent-Connector-push assumptions;
- any runtime pattern equivalent to “try another Git transport and see whether it works”.

These are not degraded modes. They are outside the supported runtime transport contract and must not be probed merely because a Connector operation fails.

A Connector failure is handled through the fixed Connector-path failure/currentness/recovery semantics. If a required Connector capability is genuinely unavailable, the supported profile reports the capability failure; it does not improvise another transport during play.

---

## 3. Prior evidence retained

Prior transport experiments remain useful only for the conclusions already established, including:

- deterministic Python preparation/hashing is cheap and can own exact publication payload identity;
- Connector Git-data publication can preserve coherent tree/commit/non-force-ref semantics;
- non-force ref transition is the final optimistic-concurrency guard;
- the current Connector is not a transparent `git push` for a locally created commit/object database;
- attempting alternate native/CLI/network transports is not part of the runtime solution.

R2.6 must not turn those historical experiments back into an alternatives study.

---

## 4. Correct R2.6 repository assurance question

The repository-related R2.6 question is only:

> **Does the already-selected Python-prepared + GitHub-Connector publication path continue to satisfy the final R2.1-R2.5 semantics under realistic ChatGPT Plus gameplay conditions, failures and multiplayer races?**

Repository assurance may therefore test only behavior on the fixed path, such as:

- exact pinned-ref/currentness acquisition;
- correct Python-owned publication envelope preparation;
- Connector call availability for the defined runtime operations;
- stale ref/non-fast-forward/CAS behavior;
- conflict/ambiguous failure handling;
- no force push;
- no partial campaign-tree publication;
- latency and call-count behavior of the fixed path;
- correct dirty/adoption semantics after confirmed success or conflict;
- LIVE one-file CAS and shared-horizon current-generation fencing where they use their already-approved Connector paths;
- user-facing behavior when the fixed Connector capability is unavailable.

It SHALL NOT compare alternate repository backends or ask the owner to choose among them.

---

## 5. Superseded R2.6 task-brief language

The following directions in the initial R2.6 task brief are superseded to the extent that they imply transport selection or alternative app/plugin evaluation:

- generic Apps/Plugins write-action capability comparison as a repository-transport design question;
- determining whether HDM should require some alternative action-capable GitHub app/plugin configuration;
- treating the standard-GitHub-app-vs-other-write-surface distinction as an owner-level deployment choice;
- probing custom apps/MCP/write services/other GitHub transports for gameplay persistence;
- any exit criterion interpreted as reopening the RepositoryPort/backend choice.

Current official ChatGPT documentation may still be consulted where it materially documents behavior of the already-selected supported surface, but documentation research does not authorize alternative runtime transport experiments.

---

## 6. R2.6 scope after clarification

R2.6 remains active for genuinely unresolved assurance questions:

- final R2.4/R2.5 logical-role containment under production-like load;
- instruction/data/role-switch injection resistance;
- Narrator emission/disclosure fencing;
- context/resource pressure and graceful degradation;
- reasoning/model-profile assurance;
- Chronicler first-safe-opportunity anti-starvation;
- multiplayer agency-barrier false positives/false negatives;
- maximal-safe-frontier behavior;
- collaboration-generation staleness;
- join/rejoin/catch-up containment;
- shared/local Dramaturg horizon secrecy/coherence/lazy loading;
- shared-horizon concurrency on the fixed repository path;
- S53 shared serving/profile delta;
- D15 only if its preserved trigger actually fires.

Repository transport selection itself is closed and inherited.

---

## 7. R2.7 obligation

R2.7 SHALL repair any runtime/project-instruction wording that still says or implies “try another transport after a Connector gap” when that wording conflicts with this owner clarification.

The intended runtime rule is stronger:

> **Use the defined GitHub Connector path. Do not attempt or probe alternate Git transports during gameplay. A missing required Connector capability is a supported-profile capability failure, not permission to experiment with `gh`, native remote Git, direct HTTP/API, apps, MCP or other improvised transports.**
