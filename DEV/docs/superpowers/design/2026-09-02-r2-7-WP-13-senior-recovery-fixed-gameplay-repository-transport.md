# R2.7 WP-13 — Step-1 Senior Recovery — Fixed Gameplay Repository Transport

Status: **SENIOR REPAIR COMPLETE — MANDATORY SENIOR REVIEW PENDING**

Date: 2026-09-02

Scope: **WP-13 Step 1 only**

This record is a post-critic Senior recovery artifact. It does not rewrite the historical whole-project Task-Brief critic and does not claim that critic findings C01–C10 originally discovered the issue below.

Owning Step-1 artifacts:

- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-task-brief.md`;
- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-source-manifest.md`;
- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-task-brief-critic.md`.

---

## SR13-01 — accepted R2.6 fixed gameplay repository transport omitted from Step-1 framing

Severity: **SIGNIFICANT**

Disposition: **CLOSED BY SENIOR REPAIR**

### Finding

The original WP-13 Step-1 Task Brief and Source Manifest correctly recovered Step-5.5/5.6 publication semantics, current `GAME/CORE/PERSISTENCE.md`, access/currentness constraints and the development-agent GitHub-Connector discipline in `AGENTS.md` / `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md`.

They omitted two current accepted R2.6 sources that independently own the **shipped gameplay/runtime repository-transport selection**:

- `DEV/docs/superpowers/specs/2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md`;
- `DEV/docs/superpowers/design/2026-08-24-r2-6-fixed-repository-transport-owner-clarification.md`.

That omission was material because development-agent transport discipline is not a substitute for shipped gameplay/runtime architecture.

### Controlling R2.6 contract

The accepted gameplay repository path is fixed as:

```text
deterministic Python/core preparation
-> GitHub Connector Git-data/ref operations
-> authoritative non-force ref transition
```

Transport selection is closed. The supported gameplay/runtime profile does not probe, compare or fall back to:

- `gh` / GitHub CLI;
- shell/native remote Git, including clone/fetch/pull/push/ls-remote/SSH Git;
- direct private HTTP/GitHub API/token workarounds from Python/container;
- alternate GitHub App/MCP/custom backend/write-service transports;
- GitHub Actions as a gameplay persistence bridge;
- transparent local-commit push assumptions;
- equivalent "try another transport" runtime behavior.

A missing required GitHub Connector capability is a **supported-profile capability failure**. It is not authorization to improvise another gameplay transport.

`GAME/CORE/PERSISTENCE.md` remains the runtime HOW owner for the concrete publication sequence where applicable; R2.6 fixes the allowed remote transport path underneath/alongside that runtime contract.

### R2.7 / WP-13 consequence

R2.6 already requires R2.7 to map the actual publication envelope and preserve integrated acceptance coverage for Connector:

- exact pinned-ref/currentness acquisition;
- Python-owned publication envelope preparation;
- required Connector operation/capability availability;
- stale-ref / non-fast-forward / CAS behavior;
- conflict and ambiguous-failure handling;
- no force push;
- no partial campaign-tree publication;
- correct generation/dirty adoption after confirmed success or conflict;
- fixed-Connector currentness/CAS/conflict/failure regression coverage;
- supported behavior when a required Connector capability is unavailable.

WP-13 therefore consumes this as a closed cross-stage authority input. It does not reopen repository transport selection.

---

## Repair applied

The narrow repair:

1. adds both R2.6 sources to the WP-13 Source Manifest as current accepted cross-stage authority / owner clarification;
2. makes both sources mandatory Step-2 evidence inputs;
3. explicitly distinguishes R2.6 shipped gameplay/runtime architecture from `AGENTS.md` / `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md`, which govern development-agent remote work;
4. updates the Task Brief to preserve the fixed gameplay transport path and closed selection;
5. extends the future Step-2 evidence route to extract the R2.6 publication-envelope/currentness/CAS/conflict/failure obligations;
6. prohibits transport-alternative research unless evidence first exposes a concrete feasibility uncertainty **inside the already selected Connector path**;
7. preserves Step-5.5/5.6, WP-11 and WP-12 as the existing durability/publication/route/generation authorities they already are.

No runtime, schema, catalog or test implementation is changed by this recovery.

No Step 2–8 work is performed.

---

## Historical critic preservation

The original whole-project critic remains the historical record of C01–C10:

```text
C01-C10: unchanged historical critic findings
SR13-01: separate post-critic Senior finding
```

The recovery does not rewrite C01–C10 as if the critic had found SR13-01.

---

## Step-2 route added by recovery

If and only if mandatory Senior review later authorizes Step 2, evidence extraction must include, before synthesis:

```text
R2.6 MVP Host Assurance fixed transport law
+ R2.6 fixed-repository-transport owner clarification
        |
        v
fixed supported gameplay path
Python/core -> GitHub Connector -> non-force ref transition
        |
        +-> exact publication-envelope mapping
        +-> Connector operation/capability availability
        +-> currentness / CAS / stale-ref behavior
        +-> conflict / ambiguous-failure classification
        +-> no-force / no-partial-publication invariants
        +-> generation-specific success/conflict adoption
        +-> supported-profile capability-failure behavior
        |
        v
reconcile with Step-5.6 + WP-11 + WP-12 + current PERSISTENCE machine
```

No alternate transport comparison belongs in that route unless a concrete feasibility uncertainty is first demonstrated inside the selected Connector path and cannot be resolved from current accepted evidence.

---

## Recovery gate

```text
SENIOR_FINDING:          SR13-01
INITIAL_SEVERITY:        SIGNIFICANT
DISPOSITION:             CLOSED BY SENIOR REPAIR
UNRESOLVED_BLOCKING:     0
UNRESOLVED_SIGNIFICANT:  0
HUMAN_DECISION_REQUIRED: NO
STEP_2_AUTHORIZED:       NO
```

Mandatory Senior review of the repaired Step-1 package is required before Step 2.

WP-14 and implementation planning remain blocked.