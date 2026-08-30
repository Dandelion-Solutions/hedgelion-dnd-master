# S6D-08 — HP, LifeState, Resource, Effect, Condition, Duration and Recovery — Architecture Task Brief

Status: **STEP 1 TASK BRIEF — READY FOR HUMAN REVIEW AFTER BRIEF-CRITIC PASS**

Date: 2026-08-26

## 1. Purpose and stage boundary

S6D-08 closes the concrete supported rules-seed contracts for HP, temporary HP, LifeState, death and stabilization, owner-local resources, Effects, Conditions, concentration/support relationships, durations, scheduled triggers and recovery boundaries. It must prove that the already accepted ownership and execution architecture can express a bounded real D&D baseline without creating another state owner, workflow, event queue, scheduler, query engine or recovery authority.

In this loop, **mechanical recovery** means rules-driven rest/resource/Condition/Effect response; **durability recovery** means retry, reload, crash/checkpoint reconstruction and orphan cleanup. Every evidence and design matrix row must identify which meaning applies, or both.

This artifact is Step 1 only. It authorizes research and design framing after human approval; it does not select unresolved product semantics, change canonical architecture or machine artifacts, run Step 2 research, or begin S6D-09.

## 2. Governing inputs and source-manifest route

The design loop must fresh-read the current remote ref and then exhaust the task-specific dependency subgraph routed by `DEV/PROJECT_MAP.md`. At minimum the Step-2 Source Manifest must include and classify:

1. process/status owners: `AGENTS.md`, both design-process owners, `DEV/PROJECT_MAP.md`, `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`, the S6D owner decision, umbrella Task Brief and execution plan;
2. semantic owners: `DEV/docs/superpowers/design/2026-08-19-step-1-2-retrospective-architecture-assurance-final.md`, followed to every exact current Resource/HP/LifeState/Effect/Condition owner and assurance resolution it routes; the accepted Step-2 mechanical-state ownership design; and the exact health/effect selector-query, LifeState transition, Effect application/reapplication, valued/cumulative Condition, Condition intrinsic-scope and recovery-boundary decisions;
3. execution owners: `DEV/docs/superpowers/specs/2026-08-19-step-3-execution-boundary-canonical-spec.md`, its actual current execution/resume/event/receipt schemas and tests, `ACTIVITY_MODEL.md`, `RULE_ELEMENT_MODEL.md`, `MECHANICAL_CONTEXT.md`, `PORTABLE_ACTIVITY_VALUES.md` and `ACTIVITY_PRIMITIVE_CONTRACTS.md`;
4. state and continuity owners: `ACTOR_MODEL.md`, `GAME/CORE/COMBAT.md`, `CHRONOLOGY.md`, `RUNTIME.md`, `RANDOMNESS.md`, `STORAGE.md`, `PERSISTENCE.md`, `DURABILITY_GUARD.md`, `SAVE_CONTRACT.md`, `SESSION.md` and `INTEGRITY.md`; plus the exact accepted anchors `2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md`, `2026-08-20-step-5-3-temporal-pending-continuity-canonical-spec.md`, `2026-08-21-step-5-3-5-9-temporal-agenda-chronology-integration-canonical-amendment.md`, `2026-08-20-step-5-7-checkpoint-recovery-protocol-canonical-spec.md`, `2026-08-21-step-5-9-chronology-persistence-reconciliation-canonical-spec.md`, `../design/2026-08-21-step-5-9-forward-extensible-time-boundary-owner-decision.md`, `2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md` and its resolution gate;
5. completed S6D dependencies: selector metadata (S6D-03), accessors/facts/DAG (S6D-04), portable values (S6D-05), primitive contracts and activation law (S6D-06), and the exact S6D-07 playable character seed and its deferred durability/recovery dependency;
6. current machine surfaces: catalog admission ledger, `core-catalog.json`, `mechanical-surfaces.json`, primitive contracts, entity structures; Actor/Resource/Effect/Condition/RestPolicy definitions and world Actor/Effect state schemas; duration/temporal/boundary/trigger/predicate/execution/event schemas; every relevant focused Step-2, Step-3, Step-5 and S6D test/fixture;
7. current shipped domain rules and supported seed definitions actually claiming HP, death, recovery, resource, condition, concentration or duration behavior.

Routing/index sources are not substitutes for owning sources. The Source Manifest must record each source's authority, applicable obligations, qualifiers, supersession status and exact downstream claim. Enumerated requirements and deferred items require item-level accounting.

Every named anchor must be followed to its actual current schemas, tests or canonical scenario evidence. `MECHANICAL_RUNTIME_PROPOSAL.md` and any other superseded derivation are provenance-only and cannot override accepted owners. The loop must not invent executable test filenames where the owner supplies only canonical scenarios.

## 3. Established constraints that the loop must preserve

- Actor state owns current/max HP, temporary HP, LifeState and Actor-lifetime Resource instances; definition records own rules, not mutable instance state.
- LifeState changes occur only through the accepted LifeState transition policy. HP arithmetic must not infer or write an independent competing life state.
- Effects are explicit world instances with target/source/rules origin, parameters, temporal binding, support relationship and explicit active/terminal lifecycle where applicable. A Condition aggregate is derived from applicable Condition sources; it is not a second mutable status owner.
- Definition Effects/Conditions/Resources/RestPolicies remain declarative. They do not execute arbitrary code, query arbitrary state or obtain direct mutation authority.
- Prospective changes live inside evaluation/ExecutionSegment; commit disposition belongs to the segment; committed fact belongs to MechanicalEvent; outcome/evidence belongs to receipt/trace. Embedded values do not acquire independent lifecycle identity.
- Every state mutation goes through the accepted deterministic execution/commit boundary, with RNG, retry, suspension and receipt rules inherited from Step 3 and Step 5.
- RestPolicy determines qualification and emits/identifies an accepted completion boundary. The boundary invokes owner-local responders; RestPolicy does not directly mutate every Actor, Effect, Condition or Resource.
- Chronology emits due boundary occurrences through accepted local/indexed mechanisms. No background worker, mandatory wall-clock scheduler or ordinary-turn global scan may be introduced.
- S6D-06 primitives remain fail-closed unless a concrete supported consumer passes the Primitive Necessity Challenge. A seed reference alone is not activation evidence.
- S6D-07's bounded martial/spellcaster paths remain the playable dependency boundary. S6D-08 must close their exact health/resource/effect/recovery dependencies and only the additional minimal cases needed to prove this domain architecture; it must not broaden toward full SRD coverage.
- The exact S6D-07 contracts remain narrow: `effect.innate_sorcery`, its one-minute TemporalBinding, same-key replacement and expiry/recovery boundary do not confer generic Effect/Duration authority; Action Surge remains current-turn procedure state rather than Actor resource state. Second Wind, Tactical Mind and every activated selector/primitive pair retain only their reviewed consumer authority.
- Unsupported content is explicitly absent/nonselectable. Coverage is not activation.
- No backward-compatibility layer is required for nonexistent released campaigns.

If fresh owners contradict any statement above, Step 2 must report the exact conflict and precedence evidence rather than silently choosing.

## 4. Questions the design loop must answer

### 4.1 Supported seed inventory and closure

Produce an exact item-level inventory of the smallest real cases required by the S6D-07 paths plus representative closure cases for:

- damage, healing, temporary HP and maximum-HP interaction;
- zero HP, unconsciousness where supported, death saves, stabilization, damage while at zero and death;
- bounded Actor resources and spell-slot or equivalent spellcasting resource recovery actually required by S6D-07;
- presence and valued/cumulative Conditions required by the supported slice;
- passive, triggered, re-applied, concentration-/support-bound and expiring Effects;
- instant, metric, boundary-relative and permanent duration shapes only where a real supported consumer requires them;
- turn/round/scene/rest and metric recovery or expiry boundaries required by those cases;
- periodic Effects or scheduled local triggers, if and only if a supported case proves necessity.

For every case record: canonical consumer; definition IDs; mutable semantic owner; selectors/accessors/facts; Activity/primitive or owner-policy route; temporal/boundary route; exact mutation; MechanicalEvent/receipt evidence; durability/recovery obligations; unsupported negative space; and transitive dependency closure.

Produce a separate inherited S6D-07 contract ledger. Itemize every active S6D-07 health, resource, Effect, temporal, selector and primitive dependency and classify it as `ACCEPTED_NARROW_CONTRACT`, `REQUIRES_GENERIC_S6D08_COMPLETION`, `UNSUPPORTED_OUTSIDE_EXACT_CONSUMER`, or `CONFLICT_REQUIRING_AMENDMENT`. Generic S6D-08 contracts must realize the accepted exact cases, while unrelated Effect/Resource/temporal content remains nonselectable until independently admitted.

### 4.2 Owner and transition proof

For each proposed state change, prove a single route:

```text
validated invocation/input
-> deterministic evaluation
-> prospective segment-local change
-> accepted ExecutionSegment disposition
-> owner mutation
-> MechanicalEvent
-> receipt/trace
-> durable/recoverable state where required
```

Explicitly distinguish HP arithmetic, LifeState policy transition, Resource accounting, Effect lifecycle transition, Condition aggregation, support/concentration termination and recovery-boundary response. Reject any proposal that collapses these into an untyped generic state-delta engine or creates duplicate semantic owners.

### 4.3 Temporal and recovery proof

For every duration, periodic trigger, expiry and recovery case determine:

- chronology basis and exact accepted boundary/metric owner;
- whether the fact is derived locally, indexed as pending temporal work, or durably stored on its semantic owner;
- behavior across suspension, retry, crash recovery, scene transitions and long gaps;
- idempotency/deduplication evidence and ordering/recency tie-breaks;
- why no background scheduler or global scan is needed;
- which owner-local responder consumes a rest/boundary occurrence and what authority it has.

Scheduled-trigger shape extensions are forbidden unless a named supported case cannot be represented by the current owner contracts. Any extension requires a minimality proof and negative tests against a general event queue.

### 4.4 Machine-contract and catalog audit

Audit current schemas/catalogs before designing replacements. For every field/enum/ID classify `SUFFICIENT`, `CONFLICTING`, `UNDERCONSTRAINED`, `STALE/UNPROVEN`, `MISSING_FOR_SUPPORTED_CASE`, or `DORMANT`. Cover at least:

- Actor health/LifeState/resource instance state;
- ResourceDefinition capacity/state/recovery contracts;
- EffectDefinition, ConditionDefinition and RestPolicyDefinition;
- world Effect lifecycle, parameters, support, temporal binding and scheduled-trigger state;
- DurationSpec, temporal binding, boundary occurrence and trigger binding;
- relevant selector/accessor/fact and primitive registries;
- MechanicalEvent, receipt, retry/recovery and persisted-current-state projections.

The loop must prefer removal/quarantine or a tighter existing representation over a new owner or generic abstraction. Structural changes require RED evidence first and catalog-aware positive and negative conformance tests.

### 4.5 Cross-owner consistency

Check both directions across the whole project dependency graph:

- upstream: accepted Step-2/3/5 laws, House Rules typed-adjudication boundary and S6D-01…07 contracts;
- downstream: S6D-09 domain coverage, S6D-11 machine closure, R2.7 audit, runtime implementation planning, persistence/recovery, multiplayer/shared-state and package reconstruction.

When a conflict appears, identify the canonical owner and determine whether S6D-08 must conform, the earlier architecture is genuinely insufficient and must be amended, or a human product decision is required. Do not reopen accepted architecture merely because it overlaps.

## 5. Required Step 2–8 outputs

1. **Step 2 — Research & architecture draft:** Source Manifest; residual-obligation ledger; inherited S6D-07 contract ledger; current-contract inventory; supported-case/dependency matrix; gap and conflict evidence; architecture alternatives only where evidence supports them; exact recommended draft.
2. **Step 3 — Decision Brief:** only genuine human product/authority/risk choices. Technical representation that follows from accepted owners is agent-owned. If none remain, record that and continue.
3. **Step 4 — Collaborative review:** challenge the draft against owners, evidence, alternatives and implementation-facing clarity; repair every blocking/significant finding before candidate selection.
4. **Step 5 — Candidate specification and TDD machine realization:** produce one internally consistent candidate with schema/catalog contracts, invariants, failure behavior, conformance vectors and explicit owner amendments; materialize authorized machine-contract changes RED→GREEN.
5. **Step 6 — Independent whole-project adversarial solution review:** an independent critic, not the candidate author or collaborative co-designer, attacks duplicate owners/lifecycles, hidden scheduler/event queue, arbitrary mutation/query, LLM authority leakage, retry/RNG errors, temporal loss/duplication, cross-owner contradictions, unsupported breadth and hot-path scans.
6. **Step 7 — Resolution Gate:** resolve and record every finding, verify the complete exit criteria with fresh evidence and authorize or deny canonicalization. Zero unresolved `BLOCKING` and `SIGNIFICANT` findings is mandatory.
7. **Step 8 — Canonicalization/publication:** only after the Step-7 gate, update all affected canonical docs/catalogs/schemas/tests and `DEV/PROJECT_MAP.md`; publish/read back the canonical chain and stop before S6D-09.

The Step-1 brief critic and independent Step-6 solution critic must reconstruct the complete relevant dependency subgraph through `DEV/PROJECT_MAP.md`, read actual owners and consumers, search for indirect conflicts and classify findings as `BLOCKING`, `SIGNIFICANT` or `MINOR`. A local-document-only critique is invalid. Step 4 applies the same whole-project discipline collaboratively. Step 7 is the resolution gate, not a substitute critic. Closure requires zero unresolved `BLOCKING` and `SIGNIFICANT` findings.

## 6. Acceptance walkthroughs required before canonicalization

The final design must trace at least these architecture scenarios end to end:

1. martial Actor takes damage through temporary HP to zero, enters the correct LifeState, then stabilizes or dies under supported rules;
2. healing from zero restores HP and invokes the exact LifeState transition policy without duplicate state inference;
3. spellcaster spends and recovers the exact S6D-07 spellcasting resource across the applicable boundary;
4. an Effect contributes a passive modifier, is reapplied under its policy and expires without a scan;
5. a Condition derived from one or multiple sources changes when a source ends, including one valued/cumulative case if supported;
6. concentration/support loss terminates the correct dependent Effect(s) through an accepted deterministic route;
7. one periodic or delayed case, only if admitted, survives suspension/retry/recovery without duplicate execution;
8. Long Rest qualification emits the completion boundary and owner-local responders recover/remove exactly their own state;
9. save/reload or crash recovery reconstructs every authoritative state and pending temporal obligation required by the slice.

These are architecture/machine-contract proofs, not a demand to implement the production runtime in S6D-08.

## 7. Non-goals

- full SRD or broad bestiary/spell/condition coverage;
- combat orchestration, UI, dialogue scripting or production runtime implementation;
- a general scheduler, workflow engine, event queue, arbitrary trigger language, general query engine or generic state mutation protocol;
- a second Condition-instance store when aggregate Condition state is derived by accepted rules;
- an independent lifecycle for Signal, StateDelta, DurationSpec, boundary occurrence or receipt values;
- RestPolicy as global mutation coordinator;
- speculative activation of quarantined primitives;
- implementation-time compatibility/migration machinery for nonexistent campaigns;
- S6D-09 work.

## 8. Human decision and stop conditions

Stop for the human architect only when evidence leaves materially different product semantics, supported-content scope, authority allocation or risk acceptance. Present a narrow decision brief containing established facts, exact alternatives, recommendation, consequences and the precise decision requested.

Do not stop for repository discovery, document volume, machine representation choices determined by accepted architecture, test design, naming, ordinary schema closure or reconciliation whose precedence is already canonical.

## 9. Step-1 exit gate

Step 1 closes only when:

- the brief has been reviewed by a whole-project brief-critic using current remote owners and indirect consumers;
- every `BLOCKING` and `SIGNIFICANT` issue is repaired or explicitly resolved;
- the brief and critic record are published on the authoritative branch and read back;
- roadmap/project routing identifies S6D-08 Step 1 complete and Step 2 next;
- no Step-2 research draft, decision, candidate or machine change has begun.

