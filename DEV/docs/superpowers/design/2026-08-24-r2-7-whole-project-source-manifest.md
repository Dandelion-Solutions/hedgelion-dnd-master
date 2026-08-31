# R2.7 — Whole-Project Source Manifest / Coverage Ledger

Status: **IN PROGRESS**

Date: 2026-08-24

Purpose: durable source-selection and inspection ledger for the whole-project final audit. This file records evidence coverage; it is not a semantic owner.

Execution protocol:

- `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-execution-protocol.md`

---

## 1. Global bootstrap / process sources

| Source | Authority role | Required scope | Inspection status | Notes |
|---|---|---|---|---|
| `AGENTS.md` | CANONICAL / GOVERNANCE | repository geometry, branch/transport/write rules, fresh-session bootstrap | INSPECTED CURRENT | Active ref fixed; Connector-only remote transport; GAME/DEV ownership geometry; no probe branches |
| `DEV/DESIGN_PROCESS.md` | CANONICAL PROCESS | evidence completeness, decision rights, Source Manifest, deep-work gates | INSPECTED CURRENT | Agent owns evidence/completeness; human owns residual product/material trade-offs |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | CANONICAL HDM PROCESS ADAPTER | HDM evidence roles, item-level accounting, sequencing gate | INSPECTED CURRENT | Whole-project audit must use owner sources, qualifiers and reverse consumers |
| `DEV/PROJECT_MAP.md` | DERIVATIVE LOCATOR | dependency routing across GAME/DEV/runtime/test/release | INSPECTED CURRENT FOR ROUTING | Never substitutes for owners |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | SEQUENCING / SCOPE AUTHORITY | intended R2.7 sequence, scope and dependencies | INSPECTED CURRENT | Global current status/gates belong only to `DEV/CURRENT_PROGRESS.md`; implementation remains blocked |
| `DEV/docs/superpowers/specs/2026-08-24-r2-7-whole-project-final-audit-owner-clarification.md` | OWNER DECISION | whole-project scope and bidirectional proof | INSPECTED CURRENT | Outer scope is not Round-2-only |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md` | ACTIVE TASK BRIEF | 27 domains + exit criteria | INSPECTED CURRENT | Governing final-audit brief |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md` | RESEARCH / SCOPE INVENTORY | WP-01..WP-27 question inventory | INSPECTED FOR CURRENT DOMAIN + GLOBAL ROUTING | Minimum audit horizon |
| `DEV/docs/superpowers/design/2026-08-24-r2-7-audit-execution-protocol.md` | OWNER-APPROVED EXECUTION PROTOCOL | durable cursor, domain loop, stop conditions | INSPECTED CURRENT | Conversation state is not checkpoint |

---

## 2. WP-01 — Product / deployment / repository boundary

### 2.1 Accepted architecture / owner sources

| Source | Authority role | Required scope | Inspection status | Material evidence |
|---|---|---|---|---|
| `DEV/docs/superpowers/specs/2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md` | CANONICAL / OWNING | supported MVP host/deployment profile; Lab boundary; host vs acceptance classification | INSPECTED | ChatGPT Plus; Project-capable ordinary chat; one human per own chat; High recommended; exact model equality not required; fixed Connector; experiments/prototypes/raw fixtures -> Lab; integrated Protocol 4 -> post-implementation acceptance |
| `DEV/docs/superpowers/design/2026-08-24-r2-6-fixed-repository-transport-owner-clarification.md` | OWNER DECISION / SUPERSEDING | fixed repository path + forbidden fallbacks | INSPECTED | Python/core prepares; Connector performs remote GitHub transport; no `gh`, remote git, direct HTTP/API, MCP/backend alternatives, improvised Actions bridge, or transport probing |
| `DEV/docs/superpowers/specs/2026-08-18-game-dev-release-boundary-design.md` | APPROVED DESIGN DIRECTION | GAME/DEV package boundary and runtime self-containment | INSPECTED | GAME contents are exact package source; DEV is development-only; installed package paths are package-root relative |
| `DEV/docs/superpowers/specs/2026-08-18-game-dev-boundary-audit-amendment.md` | DESIGN AMENDMENT / BOUNDARY REVIEW | non-obvious GAME/DEV risks, runtime firewall, release validation | INSPECTED | GAME runtime must not depend on DEV; structural absence stronger than runtime denylist; Project Instructions parity; GitHub Actions separate execution surface |

### 2.2 Current implementation/runtime surfaces

| Source | Authority role | Required scope | Inspection status | Material evidence |
|---|---|---|---|---|
| `GAME/CORE/PLAY_POLICY.md` | SHIPPED RUNTIME CONTRACT | runtime scope firewall | INSPECTED | Explicitly says installed package is self-contained; ENGINE_MAINTENANCE separate; campaign/runtime uses package-local areas only |
| `GAME/CORE/BOOTSTRAP_RUNTIME.md` | SHIPPED RUNTIME CONTRACT | package/runtime/storage bootstrap and Connector policy | INSPECTED | Local validated runtime assets; campaign storage has no engine copy; currently says `Do not first use ...` for alternate Git transports — weaker than R2.6 |
| `GAME/INSTALL/00_DND_BOOTSTRAP.md` | SHIPPED BOOTSTRAP | installation/startup/repository path | INSPECTED | Local runtime packages, no engine clone; Connector policy currently says `Do not try ... first` — weaker than R2.6 |
| `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt` | SHIPPED HOST INSTRUCTION | Project setup + transport guard | INSPECTED | Uses Connector as `default transport` and says do not substitute alternatives `first` — weaker than R2.6; does not state Plus in the copied instruction itself |
| `GAME/INSTALL/README.md` | SHIPPED INSTALL DOC | user-facing prerequisites + canonical Project Instructions copy | INSPECTED | Requires ChatGPT Project + Connector; embedded Project Instructions duplicates same weak `default/first` wording; does not explicitly say supported MVP plan is Plus |
| `GAME/CORE/PERSISTENCE.md` | SHIPPED RUNTIME HOW OWNER | campaign publication transport | INSPECTED | Fixed Git-data tree/commit/non-force-ref transaction; no per-file campaign publication; finite stale-ref recovery |
| `GAME/CORE/NEW_CAMPAIGN_FAST_PATH.md` | SHIPPED RUNTIME CONTRACT | campaign scaffold publication | INSPECTED | Exact local generator; one bulk tree/commit/ref publication; if Python/generator unavailable, fail rather than synthesize fallback |
| `GAME/CORE/RUNTIME.md` | SHIPPED RUNTIME CONTRACT | write routing + gameplay sync | INSPECTED | Persistence delegated to `PERSISTENCE.md`; no clone/full pull/archive as gameplay synchronization |
| `GAME/CORE/ENGINE_UPDATES.md` | SHIPPED RUNTIME CONTRACT | runtime package/update authority | INSPECTED | Gameplay bytes from local runtime assets; GitHub metadata not installation path; campaign storage contains no engine copy |
| `DEV/TOOLS/release_builder.py` | DEVELOPMENT MACHINE CONTRACT | release composition boundary | INSPECTED RELEVANT PORTION | Required runtime roots are under GAME; package composition recursively includes valid GAME files; DEV metadata is build-time validation input, not runtime dependency |

### 2.3 Private Lab evidence/source

| Source | Authority role | Required scope | Inspection status | Material evidence |
|---|---|---|---|---|
| `dkolyada/hedgelion-dnd-master-lab/README.md` | PRIVATE LAB GOVERNANCE / RESEARCH CONTEXT | Lab/public separation | INSPECTED | Lab deliberately independent from production HDM; no production campaign state or engine code; intended for feasibility experiments |

### 2.4 Search/discovery checks

| Check | Status | Interpretation |
|---|---|---|
| public HDM search for `HDM Lab` / laboratory routing | NO PUBLIC RESULT | Public `AGENTS.md` does not currently expose the general experiment->Lab routing rule; R2.6 canonical contains a narrower experiment rule |
| repository search for Connector/Git transport references | ROUTING COMPLETE ENOUGH FOR WP-01 | Relevant active surfaces identified and then read on active ref; default-branch search snippets were not used as correctness evidence |
| repository search for `DEV/` references | ROUTING ONLY | GAME references found are mainly wrapper rejection/install text, while `PLAY_POLICY` explicitly states self-contained runtime firewall; detailed package conformance remains WP-23/WP-26 |

---

## 3. Coverage state after WP-01 slice

```text
WP-01 source discovery: COMPLETE ENOUGH FOR DOMAIN SYNTHESIS
WP-01 owning sources inspected: YES
WP-01 current runtime/install consumers inspected: YES
WP-01 known material gaps: 3 classes
    1) weak transport wording (`default` / `first`) in shipped bootstrap/instructions
    2) supported Plus plan omitted from user-facing install prerequisites
    3) general public-HDМ -> private-Lab experiment routing absent from public AGENTS
owner decision required: NO
```

Detailed findings/dispositions live in the WP-01 mini-report and global forward-obligation accounting.

---

## 4. WP-09 — Context loading, retrieval and resource-bounded operation

| Source | Authority role | Required scope | Inspection status | Material evidence |
|---|---|---|---|---|
| `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md`; `2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md`; `2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md` | CANONICAL / OWNING | bounded discovery/closure/currentness/eligibility/floors/outcomes; phase fallback; no hidden telemetry | INSPECTED FOR WP-09 | Existing semantic owners retained; no new product or provider policy |
| `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-history-canonical-spec.md`; Step-4 amendment; Step-5.14 final | CANONICAL NEIGHBOR | material source escalation, role eligibility, source basis/currentness | INSPECTED FOR WP-09 | continuity/history orientation remains finite and cannot preload |
| `DEV/docs/superpowers/specs/2026-08-31-r2-7-WP-08-llm-role-context-instruction-realization-canonical-spec.md` | CLOSED UPSTREAM INPUT | runtime-local role context and MechanicalContext boundary | INSPECTED FOR WP-09 | WP-08 not reopened |
| `GAME/CORE/PLAY_POLICY.md`; `GAME/CORE/RUNTIME.md`; `GAME/CORE/STORAGE.md` | SHIPPED RUNTIME CONSUMER | CORE cache versus lazy campaign working set; targeted hot-path retrieval | INSPECTED FOR WP-09 | compatible support, not context authority |
| CURRENT/scene/location/index schemas and template index files | SHIPPED SCHEMA/TEMPLATE CONSUMER | compact routing/discovery support | INSPECTED FOR WP-09 | no closed-world/completeness inference |
| `DEV/CATALOG/core-catalog.json`; focused runtime/latency/performance and MechanicalContext tests | DEV MACHINE/VERIFICATION CONSUMER | vocabulary and partial current regression coverage | INSPECTED FOR WP-09 | behavioral realization proof remains forward obligation |
| `DEV/docs/superpowers/specs/2026-08-31-r2-7-WP-09-context-loading-resource-bounds-realization-canonical-spec.md` | WP-09 CANONICAL REALIZATION ALLOCATION | cache/routing/profile/allocation/fallback/verification boundaries | PUBLISHED — PENDING SENIOR AUDIT | no implementation, schema, catalog or physical topology change |

```text
WP-09 source discovery/evidence: COMPLETE
WP-09 owner decision required: NONE
WP-09 forward obligations: F01–F06 recorded in WP-09 canonical spec and mini-report
WP-09 gate: MANDATORY SENIOR AUDIT
```
