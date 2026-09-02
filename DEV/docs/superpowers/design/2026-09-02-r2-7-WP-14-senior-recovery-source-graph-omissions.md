# R2.7 WP-14 — Step-1 Senior Recovery — Source-Graph Omissions

Status: **SENIOR REPAIR COMPLETE — MANDATORY SENIOR REVIEW PENDING**

Date: 2026-09-02

Target branch: `v1/engine-rearchitecture`

Pre-repair public HEAD:

```text
8f0666b5a4316137dcc3359d57a7d4b01d8cf00a
```

Owning Step-1 artifacts:

- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-14-recovery-checkpoints-session-repair-task-brief.md`;
- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-14-recovery-checkpoints-session-repair-source-manifest.md`;
- historical whole-project critic: `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-14-recovery-checkpoints-session-repair-task-brief-critic.md`.

This is a **separate post-critic Senior recovery record**. It does not rewrite the historical C01-C11 critic as though that critic had discovered the omissions below.

---

## 1. Recovery scope

Senior review identified three additional SIGNIFICANT source-graph omissions after the original Step-1 package was published.

All three are mechanically resolvable source/evidence-perimeter defects. They do not establish:

- an upstream contradiction;
- a new human-owned product decision;
- a new recovery owner;
- permission to reopen closed Step-5/WP-10/WP-11/WP-12/WP-13 architecture;
- permission to begin Step 2, WP-15 or implementation planning.

No runtime/schema/template/catalog/test/tool implementation is changed by this repair.

---

## 2. Findings and resolutions

### SR14-01 — SIGNIFICANT — R2.6 host-memory and fixed gameplay repository transport authorities were omitted from the WP-14 source graph

**Finding.** The initial WP-14 Source Manifest did not explicitly include:

- `DEV/docs/superpowers/specs/2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md`;
- `DEV/docs/superpowers/design/2026-08-24-r2-6-fixed-repository-transport-owner-clarification.md`.

That omission could allow Step 2 to under-account two binding recovery constraints:

1. ambient Project/chat/model memory is not campaign/currentness/recovery authority;
2. supported gameplay/runtime repository transport is already fixed and may not silently probe or fall back to another remote path during recovery.

**Resolution.** Both sources are now explicit mandatory Step-2 sources with distinct authority classification:

- the MVP host-assurance document is **CANONICAL / OWNING** for supported-host assurance, including ambient-host-context non-authority and fixed-Connector acceptance obligations;
- the repository transport clarification is **OWNER-APPROVED CLARIFICATION / OWNING** for closed gameplay/runtime transport selection and supersedes broader older transport-selection language.

Step 2 must preserve:

- chat history, Project memory and ambient model/host context are not campaign canon/currentness/recovery authority;
- fixed gameplay path `deterministic Python/core -> GitHub Connector -> authoritative non-force ref transition`;
- no runtime recovery probe/fallback through `gh`, native remote Git, private HTTP/API/token paths, alternate App/MCP/backend write transport, GitHub Actions gameplay bridge, transparent local-commit push assumptions or equivalent alternatives;
- missing required Connector capability is a supported-profile capability failure;
- exact pinned-ref/currentness/CAS/conflict/ambiguous-failure evidence on the fixed Connector path belongs in recovery evidence extraction.

The repaired Source Manifest explicitly separates these gameplay/runtime authorities from development-agent Connector discipline in `AGENTS.md` and `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md`.

**Disposition:** CLOSED.

### SR14-02 — SIGNIFICANT — `DEV/ARCHITECTURE/MAINTENANCE_COMMANDS.md` was omitted as a direct current recovery/repair/support consumer

**Finding.** The initial source graph did not include the current maintenance-command surface even though it directly consumes checkpoint/recovery/repair semantics.

Current file status is exactly:

> **INTERNAL CONTROL CONTRACT / PROPOSAL**

Therefore this surface is a real current support/recovery/repair consumer, but it is not allowed to override canonical Step-5.7 or WP-10 ownership.

**Resolution.** The Source Manifest now classifies it as **CURRENT SUPPORT / MAINTENANCE CONTRACT / PROPOSAL** and makes the following Step-2 reconciliation mandatory:

- `HDM_EXPORT_CHECKPOINT_LOG`;
- `HDM_RESET_LAST_CHECKPOINT`;
- checkpoint-based local reconstruction;
- `runtime.maintenance_audit`;
- Connector/diagnostic evidence boundaries.

The reconciliation must be against Step-5.7 current-authority-first / checkpoint-optional / no-silent-fallback architecture and WP-10 record-family allocation.

Step 1 deliberately does **not** decide whether those commands are retained, removed, renamed or redesigned. It only closes the evidence-perimeter omission.

**Disposition:** CLOSED.

### SR14-03 — SIGNIFICANT — Current `MANIFEST.last_checkpoint_id` machine surfaces were omitted

**Finding.** The initial source graph named the accepted narrow pointer semantics but did not include the two actual current machine surfaces carrying the pointer:

- `GAME/SCHEMA/campaign_manifest.schema.yaml`;
- `GAME/CAMPAIGN/MANIFEST.yaml`.

The schema currently states that `MANIFEST.last_checkpoint_id` is the sole latest-checkpoint pointer and separately states that current chronology frontier and semantic-log cursor belong to `STATE/CURRENT`.

**Resolution.** Both surfaces are now explicit **IMPLEMENTATION / MACHINE CONTRACT** Step-2 sources. Step 2 must inspect:

- exact pointer semantics;
- all actual consumers;
- lifecycle/update behavior;
- scaffold/generator impact;
- stale tests/prose coupled to the pointer.

The accepted Step-5.7 meaning remains unchanged:

> `MANIFEST.last_checkpoint_id` is a narrow checkpoint-descriptor pointer, not recovery frontier/currentness/SAVE/handoff authority and not a reason to make checkpoint creation mandatory.

**Disposition:** CLOSED.

---

## 3. Historical critic preservation

The original Task-Brief critic remains historical evidence exactly as published:

```text
C01-C11
STEP_1_CRITIC_BLOCKING:    3
STEP_1_CRITIC_SIGNIFICANT: 8
```

This Senior recovery does not edit that critic or retroactively attribute SR14-01..03 to it.

---

## 4. Reopen and decision analysis

```text
UPSTREAM_CONTRADICTION:          NO
NEW_UNSATISFIED_CONSUMER:        NO
MATERIAL_UPSTREAM_INSUFFICIENCY: NO
UPSTREAM_REOPEN_REQUIRED:        NO
HUMAN_DECISION_REQUIRED:         NO
```

The three findings are source-graph/evidence-perimeter omissions only.

---

## 5. Recovery gate

```text
SR14-01: CLOSED
SR14-02: CLOSED
SR14-03: CLOSED
UNRESOLVED_BLOCKING:    0
UNRESOLVED_SIGNIFICANT: 0
HUMAN_DECISION_REQUIRED: NO
```

Next gate:

> **MANDATORY SENIOR REVIEW OF WP-14 STEP 1 + SENIOR REPAIR**

Step 2, WP-15 and implementation planning remain blocked pending explicit Senior GO.