# HDM Architecture Round 2 — Active Roadmap

Status: **ACTIVE PROGRAM ROADMAP — R2.7 PAUSED / HOUSE RULES CLOSED / S6D NEXT BUT NOT STARTED**

Date: 2026-08-25

This file is the sequencing/status authority for Architecture Round 2 and the inserted pre-resume architecture workstreams.

Canonical process:

- `DEV/DESIGN_PROCESS.md`
- `DEV/ARCHITECTURE/DESIGN_PROCESS.md`

Primary program decisions:

- `DEV/docs/superpowers/specs/2026-08-23-round-1-step-6-closure-round-2-rebaseline-owner-decision.md`
- `DEV/docs/superpowers/specs/2026-08-23-step-4-single-context-role-containment-canonical-amendment.md`
- `DEV/docs/superpowers/specs/2026-08-24-round-2-roadmap-owner-decision.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-7-whole-project-final-audit-owner-clarification.md`
- `DEV/docs/superpowers/specs/2026-08-24-step-6-residual-rules-seed-debt-closure-owner-decision.md`
- `DEV/docs/superpowers/specs/2026-08-24-house-rules-then-s6d-eight-step-sequencing-owner-decision.md`

Evidence/accounting:

- `DEV/docs/superpowers/research/2026-08-24-round-2-evidence-disposition-ledger.md`
- `DEV/docs/superpowers/research/2026-08-24-r2-7-audit-status.md`

Detailed architecture belongs to owning specifications. This roadmap is a routing/status authority and should not be used as a substitute for those sources.

---

# 1. Program baseline

```text
primary AI host              ChatGPT
plan                         ChatGPT Plus
player-facing surface        ordinary public chat
physical LLM topology        one LLM / one physical chat context
ordinary gameplay execution  one user request / one assistant turn
private HDM hosting          OUT OF CURRENT SCOPE
direct model API calls       OUT OF CURRENT SCOPE
mandatory paid inference     OUT OF CURRENT SCOPE
future provider migration    compatibility concern only
```

Single-context role law:

> Physical availability of information does not make it logically eligible for the active HDM role.

Broad implementation remains blocked until final architecture closure and explicit implementation planning.

---

# 2. Round-1 preservation rule

A closed Round-1 topic becomes active only when current work:

1. materially extends the accepted contract;
2. exposes a contradiction or invalid assumption;
3. introduces a new consumer the accepted contract cannot satisfy; or
4. makes the accepted decision insufficient for a current requirement.

Independent confirmation or thematic overlap is evidence, not a new stage.

The former Round-1 Step 6 remains **closed as a separate physical-LLM stage**. Its retired mandatory physical-isolation topology is not revived by S6D.

---

# 3. Operating rules

- At most one numbered Round-2 stage may be `IN PROGRESS`.
- Owner-approved inserted architecture work may temporarily pause that stage when explicitly represented here.
- Before a Decision Brief, candidate specification, coverage claim or closure, Source Manifest/evidence/synthesis-completeness gates must pass.
- Owning sources beat roadmaps, indexes, summaries and remembered state.
- YAGNI applies aggressively: no new authority, registry, scheduler, generic graph, plugin/agent framework or subsystem without a current requirement.
- Clean-slate pre-release structural canonicalization is authorized: no current user campaign requires backward-compatible migration from the present scaffold.
- Future released-campaign evolution/migration policy remains a separate R2.7 responsibility.
- Normal gameplay smoothness remains a cross-project invariant: ordinary-turn correctness should be local/bounded and must not gain unnecessary network/repository/extra-LLM round trips.
- House Rules and every numbered S6D task/domain use the full eight-step deep-design loop from `DEV/DESIGN_PROCESS.md`; the existing S6D plan is decomposition/coverage guidance, not permission for direct checklist execution.
- House Rules is now closed. Do not reopen it merely because S6D overlaps its subject matter; apply the Round-1-style preservation test above and reopen only for a concrete contradiction, material extension, new unsatisfied consumer or demonstrated insufficiency.

---

# 4. Stage registry

| Stage | Status | Scope | Exit result |
|---|---|---|---|
| R2.0 | **COMPLETE / EVIDENCE-REBASELINED** | evidence rebaseline/scope reconstruction | 82/82 DIAMOND/STRONG accounted; dependency graph owner-approved |
| R2.1 | **COMPLETE / ARCHITECTURE CLOSED** | continuity/history-aligned derived state | reuse-first continuity; Story remains nonauthoritative |
| R2.2 | **COMPLETE / ARCHITECTURE CLOSED** | Actor continuity/cognition/relationships | source-Actor-owned sparse continuity; directed relationships |
| R2.3 | **COMPLETE / ARCHITECTURE CLOSED** | Context Runtime/retrieval/allocation | bounded discovery; typed closure; packet-first allocation; storage/index boundaries |
| R2.4 | **COMPLETE / ARCHITECTURE CLOSED** | single-context LLM execution/instructions | TurnEnvelope; role rebinding; deterministic authority; Chronicler service policy |
| R2.5 | **COMPLETE / ARCHITECTURE CLOSED** | collaboration/multiplayer | agency-safe collaboration; maximal safe frontier; two-level noncanonical Dramaturg planning |
| R2.6 | **COMPLETE / ARCHITECTURE CLOSED** | ChatGPT-Plus assurance/security/degradation | behavioral-containment MVP; fixed Connector transport; post-MVP integrated acceptance |
| House Rules | **COMPLETE / ARCHITECTURE CLOSED** | campaign rulings, house rules, LLM semantic adjudication boundary | canonical semantic gameplay-policy architecture; deterministic handoff; inherited publication/currentness/recovery |
| S6D | **NEXT / PREPARED / NOT STARTED** | residual rules/seed/catalog debt historically deferred to Step 6 | each numbered task/domain canonicalized by its own eight-step loop; integrated S6D closure |
| R2.7 | **PAUSED AT WP-06** | whole-project final architecture & machine-realization audit | final architecture↔machine conformance and implementation-planning entry gate |

---

# 5. Current dependency graph

```text
R2.0
 -> R2.1
 -> R2.2
 -> R2.3
 -> R2.4
 -> R2.5
 -> R2.6
 -> R2.7 WP-01..WP-05 CLOSED
 -> R2.7 WP-06 PARTIAL / PAUSED
 -> HOUSE RULES Steps 1..8 COMPLETE / CANONICAL
 -> CURRENT OWNER STOP BEFORE S6D
 -> S6D Task/Domain 1 full 8-step loop       [NEXT / NOT STARTED]
 -> S6D Task/Domain 2 full 8-step loop
 -> ... each numbered S6D task/domain independently ...
 -> S6D integrated closure / resolution gate
 -> R2.7 WP-06 RESUME
 -> R2.7 WP-07..WP-27
 -> R2.7 final reconciliation
 -> Implementation Planning
```

House Rules Step 8 has satisfied the architectural prerequisite for S6D. The current cursor nevertheless stops **before S6D** by explicit owner instruction. No S6D task/domain is active.

---

# 6. Closed Round-2 results

## R2.0

Evidence rebaseline complete; all 82 DIAMOND/STRONG candidates individually accounted; active/inherited/dormant work separated.

## R2.1

No generic memory authority; Story is durable/noncanonical orientation; exact/current questions remain with native owners.

## R2.2

Actor owns current non-epistemic private continuity; `world.knowledge` remains epistemic authority; directed relationship facets belong to source Actor.

## R2.3

Context Runtime performs bounded typed discovery/closure/allocation; indexes/caches are routing/acceleration, not authority; exact physical root/HOT mapping remains final-audit work.

## R2.4

One physical chat/turn can sequence logical roles through explicit rebinding and typed handoffs; accepted mechanics/RNG do not replay after downstream LLM failure; Narrator is the ordinary visible phase; Chronicler yields to current-turn correctness/latency.

## R2.5

Multiplayer uses independent participant TurnEnvelopes over one canon; player agency is fenced; collaboration obligations collect only; shared/local Dramaturg horizons are noncanonical and canon may invalidate preparation without plot restoration.

## R2.6

MVP secrecy correctness is observable behavioral containment, not physical isolation. Existing feasibility evidence is sufficient pre-implementation; production-like Protocol-4 scenarios move to implemented-MVP acceptance. Repository transport remains deterministic Python/core preparation + GitHub Connector with no alternate transport fallback/probing.

Owning artifacts for each stage remain under dated `DEV/docs/superpowers/specs/` and `DEV/docs/superpowers/research/` paths.

---

# 7. House Rules Architecture — COMPLETE / CANONICAL

Primary canonical owner:

- `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md`

Runtime-facing campaign policy surface:

- `GAME/CAMPAIGN/RULES/HOUSE_RULES.md`

Navigation addendum:

- `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX_HOUSE_RULES_ADDENDUM.md`

Eight-step design cycle:

1. `DEV/docs/superpowers/specs/2026-08-24-campaign-rulings-house-rules-architecture-task-brief.md`
2. `DEV/docs/superpowers/research/2026-08-25-campaign-house-rules-step-2-research-architecture-draft.md`
3. `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-3-decision-brief.md`
4. `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-4-collaborative-review.md`
5. `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-5-candidate-spec.md`
6. `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-6-adversarial-review.md`
7. `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-7-resolution-gate.md`
8. `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-8-canonicalization.md`

Canonical result:

- House Rules / established Rulings are campaign-persistent **LLM-interpreted semantic gameplay policy**;
- LLM semantic applicability remains above existing typed deterministic execution and never becomes direct state/RNG authority;
- House Rule, established Ruling and one-off live adjudication have distinct adoption/lifecycle meanings without requiring separate rule engines;
- decision-specific information eligibility reuses Step-4 + R2.3 logical containment;
- campaign policy is scoped data below R2.4 constitutional/instruction authority;
- bounded discovery/currentness reuses R2.3;
- publication/recovery/multiplayer currentness reuse Step-5.6/5.7/5.8 and R2.5;
- no House-Rules-specific global synchronization/frontier exists;
- new affected Resolutions use current policy, while already accepted policy-dependent inputs remain historically stable across later publication;
- mechanically material realization crosses existing admitted capabilities only; missing realization is a finite catalog/policy-realization gap;
- promotion into structured mechanics is optional and must not create duplicate mechanical ownership.

House Rules Step-6 adversarial review closed with `0 BLOCKER`, `0 SIGNIFICANT`, and one nonblocking pre-existing R2.3 navigation/documentation MINOR.

House Rules implementation has **not** started.

---

# 8. S6D — Step-6 Residual Rules/Seed Debt Closure — NEXT / PREPARED / NOT STARTED

Owning/decomposition artifacts:

- `DEV/docs/superpowers/specs/2026-08-24-step-6-residual-rules-seed-debt-closure-owner-decision.md`
- `DEV/docs/superpowers/specs/2026-08-24-step-6-residual-rules-seed-debt-closure-task-brief.md`
- `DEV/docs/superpowers/plans/2026-08-24-step-6-residual-rules-seed-debt-closure-plan.md`

Purpose:

Close still-applicable rules/catalog/seed obligations explicitly deferred by accepted Steps 1–2 to later Step 6 and proven unresolved by R2.7 WP-06.

S6D owns, where still unsatisfied:

- ruleset/package/catalog snapshot identity required for deterministic `ResolvedCatalogContext` reconstruction;
- full supported D&D seed/catalog-gap coverage;
- complete selector/accessor/input/dependency machine metadata;
- exact supported Activity protocol value and primitive-operation contracts;
- stable character advancement/choice-slot seed sufficient for READY_PC;
- concrete HP/LifeState/Resource/Effect/Condition/Duration/Recovery seed closure;
- proven scheduled-trigger/invocation-fact extensions only where real supported cases require them;
- whole supported rules-seed coverage/adversarial audit;
- integration of the canonical House Rules mechanical boundary.

**Execution override:** the existing numbered S6D plan is a decomposition/coverage index only. Every numbered task/domain must itself run the complete eight-step deep-design loop before closure. If a task exposes multiple independently material architecture sub-blocks, split them and run separate cycles rather than forcing them into one reasoning run.

**Current stop:** the House Rules start gate is satisfied, but S6D remains **NOT STARTED**. A subsequent explicit continuation begins the next S6D Task/Domain at **Step 1 — Architecture Task Brief**, not by executing Tasks 1–12 directly as a checklist.

S6D does **not** reopen retired physical role-isolation architecture and does not build backward compatibility for nonexistent current campaigns.

---

# 9. R2.7 — Whole-Project Final Architecture & Machine Audit — PAUSED AT WP-06

Scope owners:

- `DEV/docs/superpowers/specs/2026-08-24-r2-7-whole-project-final-audit-owner-clarification.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-7-whole-project-final-audit-task-brief-v2.md`
- `DEV/docs/superpowers/research/2026-08-24-r2-7-whole-project-final-audit-scope-discovery.md`
- `DEV/docs/superpowers/specs/2026-08-24-r2-7-audit-execution-protocol.md`
- `DEV/docs/superpowers/research/2026-08-24-r2-7-audit-status.md`

R2.7 is a whole-project bidirectional proof, not a Round-2-only mapping:

```text
ARCHITECTURE -> MACHINE
    every accepted semantic responsibility has a concrete destination
    or explicit no-representation disposition

MACHINE -> ARCHITECTURE
    every material machine/runtime responsibility has an accepted owner
    or explicit derived / implementation-only / stale / debt / historical / out-of-scope disposition
```

Current progress:

```text
WP-01 CLOSED
WP-02 CLOSED
WP-03 CLOSED
WP-04 CLOSED
WP-05 CLOSED
WP-06 IN PROGRESS / PAUSED
WP-07..WP-27 NOT STARTED
```

The immutable pre-pause R2.7 status/forward-obligation set is preserved by blob SHA recorded in the active audit status file.

R2.7 remains paused. It resumes only after S6D integrated closure.

---

# 10. Explicitly removed mandatory stages / dormant work

Round 2 has no mandatory standalone Narrative Dynamics stage. R2.5's narrow S14 activation remains owned by multiplayer collaboration and does not activate generic authored-plot machinery.

Round 2 has no generic optional-capability gate. Extensions, spectator/replay, solo forks, spatial sidecars, mixed AI/human controllers and cache-specific optimization remain dormant until their own triggers occur.

The former physical-LLM Step 6 remains historical; S6D is a distinct residual debt-closure workstream.

---

# 11. Current continuation point

```text
R2.0  COMPLETE / EVIDENCE-REBASELINED
R2.1  COMPLETE / ARCHITECTURE CLOSED
R2.2  COMPLETE / ARCHITECTURE CLOSED
R2.3  COMPLETE / ARCHITECTURE CLOSED
R2.4  COMPLETE / ARCHITECTURE CLOSED
R2.5  COMPLETE / ARCHITECTURE CLOSED
R2.6  COMPLETE / ARCHITECTURE CLOSED
R2.7  PAUSED AT WP-06
HOUSE RULES  COMPLETE / CANONICAL / IMPLEMENTATION NOT STARTED
S6D   NEXT / PREPARED / NOT STARTED

CURRENT STOP:
    immediately after House Rules Step 8 canonicalization
    before any S6D Task/Domain Step 1 work

NEXT EXPLICIT CONTINUATION:
    bootstrap repository
    -> read current audit status + roadmap + House Rules canonical owner
    -> read S6D owner/task brief/plan as routing/decomposition evidence
    -> begin the next S6D Task/Domain at Step 1 — Architecture Task Brief
    -> run that Task/Domain through all eight design steps
    -> continue each numbered S6D task/domain independently
    -> S6D integrated closure
    -> only then resume R2.7 WP-06

Broad implementation: BLOCKED.
```
