# Spell execution architecture — Step 1 task brief

Status: COMPLETE FRAMING CANDIDATE — awaiting independent whole-project critic and Senior Review Stop 1. Not implementation authorization or canonical architecture.

Date: 2026-10-04. Verified source baseline: `05576261665280c3f424d791c19d8c4080343c6a`.

## Assignment and explicit product intent

The Product Owner authorizes architecture design for efficient support of the complete 339-spell SRD 5.2.1 corpus. Preserve D&D rules and hide their complexity from players. Product runtime responsiveness is the objective; development effort may be substantial. GAME operates as one chat with logical LLM roles, without subagents. Rules and required supporting content must be locally available; ordinary casting must not browse for rules or consult external help. No measured latency target is supplied.

This replaces the conversational suggestion to simplify rules or rely on a generic LLM mechanical fallback. Neither suggestion was accepted architecture. A larger corpus is a content/admission extension; accepted owners, identities and execution/durability laws remain controlling unless an actual insufficiency is proved and explicitly reviewed.

Question: what bounded additions to existing HDM architecture permit complete spell support with accurate mechanics, finite local execution and a prompt/IO path proportional to the current decision rather than the whole catalog/campaign? Do not assume a new spell engine, a new state family, a fixed taxonomy of executors, or arbitrary scripting is necessary.

## Goals and exit criteria

1. Reconcile current Activity, Rule Element, Actor, Asset, Effect, Procedure, chronology, information and canonical promotion owners. Explain reuse, required extension and current proof limits separately.
2. Define local content resolution, compile/load/cache, invocation binding, cost commitment, target resolution, bounded evaluation, reactions/continuations, owner mutations, receipts, persistence/recovery and presentation.
3. Account for all 339 inventory entries and every exceptional mode by a lawful requirement/owner/consumer/dependency/failure/recovery/presentation route. A primary group label or design coverage is not semantic/executable closure. Preserve casting prerequisites, components/costs, scaling, temporal behavior, interactions, exceptional modes, stat-block support and subjective adjudication requirements. Eventual package availability does not prove all-class acquisition/progression or current production readiness.
4. Provide explicit handling of open-world choices without arbitrary LLM-authored mutation, unchecked JSON patches, forged mechanical facts, unbounded universal simulation or external rule lookup.
5. Define structural performance acceptance: no dedicated spell LLM invocation, no deterministic-step model calls, bounded current working set, no whole-catalog prompt or per-turn compile, indexed due processing. One local orchestration call is the normal sufficient-local-path target until completion, typed failure or genuine choice/adjudication/currentness suspension. It is not a universal cross-LIVE write/commit count; required Step-3/WP-16 multi-owner and publication obligations remain preserved.
6. Define target-environment measurement and regression fixtures, distinguishing cold/warm paths, serial model depth, calls, prompt bytes/tokens, IO and tool compute from end-to-end wall time. No fabricated millisecond SLA or claimed measured speed.
7. Provide implementation-facing capability contracts, dependency phases, admission obligations and meaningful tests without implementing production or executable schemas during this assignment.
8. Complete independent framing critic and Review Stop 1 GO before Step 2. Complete the Step 2-7 evidence/alternative/challenge/candidate/review/repair cycle and publish a review-ready candidate package. After any required concrete PO decision, finish Step 8 owner/status/traceability/verification/publication/read-back/propagation, then obtain independent Senior Review Stop 2. Unaccepted proposals remain candidates and are not canonicalized. Persist the exact continuation at each boundary. Final human approval applies to the concrete decision summary, not proofreading the corpus.

## Non-goals

- Production code, campaign play/bootstrap, release ZIP inspection, implementation-plan execution or package activation.
- New microservices, model/provider integrations, subagent gameplay, general DSL, plugin marketplace, arbitrary homebrew interpreter or tactical 3D engine.
- Revisiting closed Story/Commentator architecture or activating Story/T07/T08/W06.
- Rewriting all accepted architecture because current spell consumers are narrow.
- Advertising universal commercial D&D coverage, complete character-class progression or all monster/item abilities merely because spell coverage is complete.
- Universal low-latency promises for unbounded targets or world changes; published spell semantics and host bounds must be reconciled rather than truncated.

## Current evidence and uncertainty

- Corpus inventory:339 exact SRD spell descriptions; 13 dominant indexing groups; per-spell cross-cutting dependency rows. Research grouping/complexity is provisional, not implementation authority or exhaustive exception proof.
- Current package: six exact seed spells; five intersect this SRD inventory. Thunderclap is an extra admitted seed entry requiring content provenance reconciliation, not automatic removal or a seventh-corpus claim.
- Registry:31 names, eleven exact admitted rows, twenty quarantined. Admission is exact-consumer/dependency/failure/recovery-bound; registered names cannot become executable from this brief.
- The current Activity design already calls for cached compiled recipes, bounded hydration, one host operation and no LLM calls between deterministic steps. GAME production closure must be traced separately; DEV conformance functions are not production consumers.
- Generic concentration, periodic Effects, reactions, zones and entity transformations cannot be presumed active from accepted shapes.
- Telekinesis fine-manipulation continuation remains source-qualified in the research inventory. Resolve against the licensed primary source before claiming semantic closure of its exceptional path.
- Unknown: precise production binder/evaluator/owner-write closure, necessary new closed transition variants, complete casting acquisition/discovery channel, content storage/import shape, target-environment latency calibration and all supporting stat-block/item prerequisites.

## Dependency subgraph and invariants

Product corpus/selection promises -> package manifest/snapshot/resolved-set identity -> catalog admission -> Activity/Rule Element/selector/accessor/fact/value contracts -> pinned MechanicalContext and engine-bound prerequisites -> fixed RNG and finite evaluation -> native semantic owners -> ExecutionSegment/MechanicalEvent/receipt -> HOT/durability/publication/LIVE -> role-safe Narrator/context/emission.

Side routes: Effect support and temporal boundaries; PC agency/control/access; knowledge/disclosure/illusion versus world truth; Actor archetype/Asset placement/location/plane; House Rules exact policy basis; release/license/version/sizing owners; encounter/loot/scroll/advancement consumers; historical basis and no-extra-serial laws.

Preserve stable Actor identity; Conditions derived from Effects; native location distinct from tactical micro-position; no arbitrary world query; no independent StateDelta/Signal lifecycle; accepted outcomes survive downstream trace failure; no reroll/reapply on retry; no authority from stale cache or physical data presence; required evidence cannot be discarded for a latency target.

## Source Manifest and discovery route

All repository sources use the pinned baseline. Canonical owners outrank derivative maps and research. This manifest identifies bounded roles; source qualifications and exact evidence extracts belong in Step 2.

| Route | Sources and authority role |
|---|---|
| Process/currentness | `AGENTS.md`; `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md`; `SKILL_SCOPE.md`; `DEV/DESIGN_PROCESS.md`; `DEV/ARCHITECTURE/DESIGN_PROCESS.md`; `PRODUCT_OWNER_INPUT_PROCESS.md`; `DEV/CURRENT_PROGRESS.md` |
| Discovery/sequencing | `DEV/PROJECT_MAP.md`; `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md`; `NEAR_TERM_ROADMAP.md`; current Wave-05 plan/cursor; T06 Sorcerer override Senior review. Routing/status only where derivative |
| Product constraints | `DEV/PRODUCT_OWNER_INPUT.md`, applicable PO-003/004/007/008/010/011/012 entries; direct latest Product Owner scope/performance messages captured verbatim under the ledger process |
| Catalog/content | `DEV/ARCHITECTURE/CATALOG_CONTRACTS.md`, `CATALOG_ADMISSION.md`, `CATALOG_RESOLUTION.md`, `RULESET_PACKAGE_IDENTITY.md`, `RULESET_PACKAGE_MACHINE_CLOSURE.md`; exact package manifest/member closure and builder/loader; mandatory license attribution |
| Mechanical composition | `ACTIVITY_MODEL.md`, `RULE_ELEMENT_MODEL.md`, `MECHANICAL_CONTEXT.md`, `CALCULATION_SELECTOR_METADATA.md`, `PORTABLE_ACTIVITY_VALUES.md`, `ACTIVITY_PRIMITIVE_CONTRACTS.md`; exact primitive/selector/accessor contracts and schemas |
| Semantic owners | `ACTOR_MODEL.md`, `ASSET_MODEL.md`, `HEALTH_EFFECTS_RECOVERY.md`, `CHARACTER_PROGRESSION_READY_PC_SEED.md`, `DOMAIN_RULES_COVERAGE.md`, `HOUSE_RULES_MECHANICAL_BOUNDARY.md`; actual neighboring information/location/access/Procedure owners discovered by critics |
| Execution/storage/time | Step-3 final execution spec; Step-5.3/5.9 temporal amendment; WP-12 HOT, WP-13 durability, WP-15 temporal, WP-16 LIVE/access and applicable current amendments. Existing owned boundaries remain controlling |
| LLM/context/performance | Step-4 truth/knowledge and single-context amendment; R2.3/R2.4; WP-08/09; WP-24; `GAME/CORE/AI_REASONING.md`, `PLAY_POLICY.md`, `MECHANICS_INTEGRITY.md`, `RANDOMNESS.md`, rule routing and exact current Context/TurnRuntime carriers |
| Production evidence | `GAME/TOOLS/catalog_runtime.py`, `mechanics.py`, `runtime_execution.py`, `runtime_host.py`, `temporal.py`, `hot_store.py`, relevant source/tests and call sites; inspect contracts versus actual behavior explicitly |
| Conformance evidence | `DEV/TOOLS/validate_character_mvp_seed.py`, `validate_health_effects_recovery_seed.py`, current package validators and exact focused tests; do not treat reference execution as shipped closure |
| Corpus evidence | `DEV/docs/superpowers/research/2026-10-04-spell-coverage/` inventory/report; licensed SRD spell descriptions printed pages107–175 and neighboring referenced rules/stat blocks. Rewritten content and required legal attribution; source narrative is not public architecture authority |

## Risks and questions the result must answer

- Can spell breadth reuse current owned execution without a parallel state/commit system? Prove new transitions required by concrete spells.
- How are aliases/natural player intent mapped without loading339 descriptions or relying on player rules vocabulary? No automatic cast from a guessed available capability.
- Which recipe inputs require LLM adjudication, which are engine-derived, and how is accepted adjudication frozen/recovered? Adjudication is not permission to choose arithmetic or patch canon.
- How are candidate sets, concentration, repeat saves, zones, Actor creation and triggered effects bounded when published rules have variable cardinality or durations? No global per-turn scan or hidden dropped targets.
- How does exceptional magic such as Wish/illusion/memory/planes bind to existing truth/knowledge/agency owners without pretending all fiction is algorithmically enumerable?
- Which currently dormant selectors, rule-operation pairs, accessors, embedded values and primitive contracts need exact consumer-bound extension? A recipe cannot activate any of them by referring to a registered name.
- What counts as complete support, including reactions, spell duplication, external stat blocks, NPC/item casting, recovery and long-lived consequences?
- Which current production tasks are affected? Preserve accepted S1/S2/P0 and independently authorized P2/P3; do not close P1A or authorize expanded production before accepted amendments/plan gates.
- Which latency claims are structural, measured or unproven, and what exact negative/performance fixtures reject a misleading implementation?

## Expected artifacts and exit boundary

Design-only package under `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/`: this brief, framing critique/Review Stop1, bounded evidence/impact, decision summary, candidate architecture,339-entry requirement coverage and adversarial/resolution/Senior records. Accepted law is promoted to the appropriate existing owner or final `specs/` only after the required decision gate. After that decision, Step 8 completes owner/status/traceability synchronization, finding propagation, applicable verification, publication and read-back before independent Senior Review Stop 2. The candidate boundary keeps that exact continuation pending; it does not report Step 8 or Stop 2 complete. No competing canonical owner is created by a draft's filename.

VERSION_IMPACT: NONE for this design-only framing. Future accepted source/schema/catalog/engine changes perform their own Version Impact Gate.
