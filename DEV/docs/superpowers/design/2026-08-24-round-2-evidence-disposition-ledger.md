# Round 2 Evidence Disposition Ledger

Status: **RESEARCH SYNTHESIS / NON-NORMATIVE EVIDENCE ACCOUNTING**

Date: 2026-08-24

Purpose:

> Provide auditable item-level accounting for the DIAMOND and STRONG candidate set that informed the owner-approved Round-2 roadmap decomposition.

This artifact is not architecture authority. It preserves research semantics, qualifiers and current disposition so that the roadmap can be derived without turning research candidates into automatic requirements.

Canonical sequencing remains in:

- `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md`

Owner-approved program decomposition is recorded in:

- `DEV/docs/superpowers/specs/2026-08-24-round-2-roadmap-owner-decision.md`

## 1. Source Manifest

Primary sources inspected for this rebaseline:

| Source | Role | Why relevant |
|---|---|---|
| `AGENTS.md` | repository governance | bootstrap, documentation completeness, branch/transport rules |
| `DEV/DESIGN_PROCESS.md` | canonical process | Source Manifest, evidence extraction, completeness gate, decision rights |
| `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | HDM process adapter | item-level qualifier preservation, Round-1 preservation rule, roadmap evidence gate |
| `DEV/PROJECT_MAP.md` | derivative locator | dependency/source discovery only |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | previous sequencing authority | prior decomposition to be replaced, not treated as evidence for its own correctness |
| `DEV/ARCHITECTURE/CANONICAL_ARCHITECTURE_INDEX.md` | derivative Round-1 locator | locate owning accepted sources; stale sequencing ignored |
| `2026-08-23-round-1-step-6-closure-round-2-rebaseline-owner-decision.md` | owner decision | Round-1 closure, ChatGPT-Plus/single-context baseline, Round-1 preservation rule |
| `2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md` | canonical Step-4 owner | truth/knowledge/disclosure/roles/Context Assembler/Story ownership |
| `2026-08-23-step-4-single-context-role-containment-canonical-amendment.md` | canonical amendment | one-context logical-role containment; supersedes physical-isolation premise |
| `2026-08-19-step-3-execution-boundary-canonical-spec.md` | canonical Step-3 owner | LLM proposer/deterministic execution boundary |
| `2026-08-21-step-5-10-story-projection-durability-canonical-spec.md` | canonical Step-5 owner | Story/Chronicler projection authority and lag semantics |
| `2026-08-21-step-5-11-transcript-history-retention-compaction-canonical-spec.md` | canonical Step-5 owner | semantic continuity vs selective exact retention; host history mutation |
| `2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md` | canonical Step-5 owner | recipient disclosure, Retry/Edit non-rewind, emission boundary |
| `2026-08-21-step-5-14-full-recovery-concurrency-adversarial-review-canonical-final.md` | canonical integrated closure | recovery/concurrency constraints and unresolved physical feasibility questions |
| `HDM_External_Architecture_Idea_Dossier_2026-08-21.md` | research input | 24 DIAMOND + 58 STRONG candidates and explicit revisit triggers |
| role-context validation Protocols 1–3 | research evidence | empirical support for single-context logical containment and reasoning-profile observations |
| current host/platform feasibility research | research input | host limitations/questions, filtered through current owner-approved baseline |
| former Step-6 working notes and reusable-instruction note | historical/noncanonical input | useful unresolved questions only; retired physical-isolation premise excluded |
| `GAME/CORE/AI_REASONING.md` | current runtime contract | reasoning/authority/context discipline |
| `GAME/CORE/NPC.md` | current runtime contract | existing NPC tiering, layered identity/state, sparse cognition |
| `GAME/CORE/PREP.md` | current runtime contract | situation/pressure preparation without plot authority |
| `GAME/CORE/NARRATIVE.md` | current runtime contract | pacing/initiative/player-agency presentation constraints |
| `GAME/CORE/PROCESSES.md` | current runtime contract | causal world processes, bounded off-screen advancement |
| `GAME/CORE/MULTIPLAYER.md` | current runtime contract | authenticated player binding, split scenes, synchronization, chronology |
| `GAME/CORE/LIVE_SCENE.md` | current runtime contract | shared-scene currentness/CAS and per-PC observed information |
| `GAME/CORE/SESSION.md` | current runtime contract | recovery/resume/semantic recap and host-history independence |

This ledger claims item-level accounting only for the **82 DIAMOND/STRONG candidates** because that is the candidate set used to derive the Round-2 stage horizon. RESERVE / NEGATIVE INTELLIGENCE records remain stage-local adversarial evidence and are not claimed as separately activated roadmap candidates.

## 2. Disposition vocabulary

- **ACTIVE** — current Round-2 design must consciously resolve the candidate.
- **ACTIVE DELTA** — the broad principle already exists, but a concrete new Round-2 consumer/extension remains unresolved.
- **INHERITED / ALREADY SATISFIED** — accepted/current HDM already owns the material principle; preserve it as a constraint/regression rather than reopen it.
- **CONDITIONAL / DORMANT** — no current architecture work is created; preserve the source's revisit trigger.

Coverage does not imply activation.

## 3. Completeness summary

```text
DIAMOND + STRONG candidates     82
ACTIVE                          34
ACTIVE DELTA                     9
ACTIVE total                    43
INHERITED / ALREADY SATISFIED   16
CONDITIONAL / DORMANT           23
unaccounted                      0
```

## 4. Item-level disposition
| Item | Claim / qualifier preserved | Disposition | Current handling |
|---|---|---|---|
| D01 | Layer continuity instead of one memory blob; minimum viable layers, no duplicate authority. | **ACTIVE** | R2.1 |
| D02 | Context is a materialized bounded projection, not knowledge storage. | **ACTIVE** | R2.3 |
| D03 | One semantic context allocator with reservations/degradation; do not copy fixed quotas. | **ACTIVE** | R2.3 |
| D04 | Context assembly requires inspectable inclusion/exclusion trace; trace may contain secrets. | **ACTIVE** | R2.3 |
| D05 | Recent mutable horizon before consolidation; avoid derived artifacts from rejected history. | **ACTIVE** | R2.1 |
| D06 | History-dependent derived state must align with accepted ancestry/branch semantics; do not make host UI history canonical chronology. | **ACTIVE** | R2.1 |
| D07 | Broad/global continuity summary and episodic retrieval are distinct cognitive products. | **ACTIVE** | R2.1 |
| D08 | Per-entity continuity can bound recall without becoming a second entity authority. | **ACTIVE** | R2.1 |
| D09 | LLM semantic mutation proposals require bounded evidence and deterministic validation/commit. | **ACTIVE DELTA** | R2.1 first application; R2.2 consumer. General proposer/commit law inherited from Step 3. |
| D10 | Separate stable identity/foundation, durable evolving continuity and transient Actor state; avoid over-modeling incidental NPCs. | **ACTIVE** | R2.2 |
| D11 | World truth, observed evidence, knowledge/belief/suspicion/intention are distinct; use a narrow typed model. | **ACTIVE DELTA** | R2.2. Truth/knowledge split itself inherited from Step 4. |
| D12 | Relationships are directional Actor-owned views; preserve player agency. | **ACTIVE DELTA** | R2.2 |
| D13 | Prefer sparse/event-driven Actor cognition; NO_CHANGE is valid. | **ACTIVE** | R2.2 |
| D14 | Decision-critical packets must be complete; downgrade representation before defer, never silent partial truncation. | **ACTIVE** | R2.3 |
| D15 | Retry may use bounded rejected siblings as advisory negative space. | **CONDITIONAL / DORMANT** | Trigger: R2.6 evaluation shows repetitive Retry UX worth solving; requires separate PoC. |
| D16 | Auxiliary generations must not become visible gameplay/history; physical extra calls are optional, not implied. | **ACTIVE DELTA** | R2.4 |
| D17 | LLM interprets/proposes; deterministic runtime owns mechanics/RNG/accepted execution. | **INHERITED / ALREADY SATISFIED** | Step 3 canonical execution boundary; keep as invariant/regression only. |
| D18 | Long-range recall may combine coarse segment selection with exact evidence retrieval and selective exact preservation. | **ACTIVE** | R2.1 semantic promise; R2.3 retrieval realization. |
| D19 | Use narrow typed selectors rather than keyword-only activation; bound recursion/dependencies. | **ACTIVE** | R2.3 |
| D20 | Shared history gains observational finality; silent local retry must not rewrite shared-established outcomes. | **INHERITED / ALREADY SATISFIED** | Step 5.12 + Step 5 shared publication/history semantics already establish the core rule; integrate as R2.5 constraint. |
| D21 | Async multiplayer needs persistent collaboration semantics rather than transcript-as-coordinator. | **ACTIVE** | R2.5 |
| D22 | Split-party requires independent scene/context/chronology frontiers with causal bridges. | **ACTIVE DELTA** | R2.5 collaboration/context delta; independent scene/chronology/live ownership is already present in Step 5/runtime. |
| D23 | Coordination policy is mode/scope-owned; free-form and strict sequence cannot share one universal active-player gate. | **ACTIVE** | R2.5 |
| D24 | One canon must yield recipient/controlled-actor scoped context/disclosure projections. | **ACTIVE DELTA** | R2.3 projection semantics; R2.5 multiplayer integration. Core truth/disclosure split inherited. |
| S01 | Delay durable entity materialization until evidence/maturity warrants it. | **CONDITIONAL / DORMANT** | Trigger: automatic entity discovery/materialization is introduced. |
| S02 | Retrieval ranking may combine recurrence, recency and diversity/starvation rather than one signal. | **ACTIVE** | R2.3 |
| S03 | Evidence sources may carry different trust/provenance classes for promotion/mutation. | **ACTIVE** | R2.1 |
| S04 | Deduplicate semantically overlapping global/entity continuity channels without collapsing distinct facts. | **ACTIVE** | R2.1; realized in R2.3 selection. |
| S05 | Persistent derived records should detect/repair malformed, duplicate or orphan state. | **CONDITIONAL / DORMANT** | Trigger: persistent derived indexes/records are admitted. |
| S06 | Bound deep continuity/cognition to active/relevant cast; compact inactive actors. | **INHERITED / ALREADY SATISFIED** | Current NPC/runtime doctrine already uses tiering, lazy detail and bounded off-screen simulation; R2.2 must preserve. |
| S07 | Use explicit cognition modes rather than one generic 'think as NPC' operation. | **ACTIVE** | R2.2 |
| S08 | Protect stable Actor core while pruning low-value/stale continuity. | **CONDITIONAL / DORMANT** | Trigger: real Actor-local context/storage pressure requires selective forgetting beyond base lifecycle. |
| S09 | Authored long character arcs may use authority-defined staged evolution. | **CONDITIONAL / DORMANT** | Trigger: authored companions/major NPCs require explicit staged arcs. |
| S10 | NO_CHANGE is a successful semantic assessment outcome. | **ACTIVE** | R2.2; also applies to evidence-bound updates. |
| S11 | Transient private Actor state needs expiry/refresh semantics; turn-count TTL may be wrong clock. | **ACTIVE** | R2.2 |
| S12 | Aliases/names may need explicit lifecycle/evidence ownership. | **CONDITIONAL / DORMANT** | Trigger: alias resolution becomes a demonstrated identity problem. |
| S13 | Slow inference may use evidence accumulation/decay/promotion thresholds. | **CONDITIONAL / DORMANT** | Trigger: a concrete slow-inference consumer (aliases, habits, motifs, etc.) is admitted. |
| S14 | Inspectable noncanonical planning artifact may retain pressures/threads without canon authority. | **CONDITIONAL / DORMANT** | Trigger: retained separate planning state is proven necessary beyond existing PreparationDraft/provisional prep. |
| S15 | World-pressure progression ladder may help systemic authored threats but risks rails. | **CONDITIONAL / DORMANT** | Trigger: a systemic authored-threat model needs explicit staged pressure beyond existing world processes. |
| S16 | Timeskip may advance bounded domains/processes rather than simulate everything. | **INHERITED / ALREADY SATISFIED** | Current process/chronology runtime already uses bounded causal advancement; reopen only for a new unsupported timeskip mechanic. |
| S17 | Anti-stagnation pressure is advisory only, never event authority. | **INHERITED / ALREADY SATISFIED** | Current narration/prep/process doctrine already advances situations causally and rejects arbitrary drama. |
| S18 | Bookmarks should reference stable history nodes/branches rather than copy state. | **CONDITIONAL / DORMANT** | Trigger: explicit branching/navigation/bookmark UX is admitted. |
| S19 | High-value summaries can be reviewable/validated transformation candidates before promotion. | **ACTIVE DELTA** | R2.1; human review cannot be gameplay requirement. |
| S20 | Exact critical evidence may be pinned until semantic discharge rather than put in permanent memory. | **INHERITED / ALREADY SATISFIED** | Step 5.11 exact protection/discharge already owns this semantic need; R2.3 may consume it. |
| S21 | Late steering/procedure guidance should remain separate from world facts and campaign essentials. | **ACTIVE** | R2.4 |
| S22 | Typed dependency activation must be bounded by depth/budget/cycle rules. | **ACTIVE** | R2.3 |
| S23 | Semantic visibility/secrecy differs from UI hiding and from truth status. | **INHERITED / ALREADY SATISFIED** | Step 4 truth/knowledge/disclosure + amendment already establish the distinction. |
| S24 | Some guidance/conditions may be ephemeral over a semantic interval. | **CONDITIONAL / DORMANT** | Trigger: a concrete temporary narrative/procedural guidance owner is admitted. |
| S25 | Token/model-limit accounting should be centralized rather than ad hoc char counts. | **ACTIVE** | R2.3, constrained by actual ChatGPT host observability. |
| S26 | Multi-step auxiliary maintenance may need resumable bounded workpiece state. | **CONDITIONAL / DORMANT** | Trigger: multi-call compression/materialization is actually required. |
| S27 | One semantic assessment should commit at most one bounded durable mutation. | **ACTIVE DELTA** | R2.1 first application; R2.2 consumer. |
| S28 | Operational control markers/maintenance artifacts must not leak into visible output; sanitization is defense-in-depth only. | **ACTIVE** | R2.4 |
| S29 | Context assembly needs side-effect-free dry-run/trace mode for tests and diagnostics. | **ACTIVE** | R2.3 |
| S30 | Extensions should receive capability-scoped authority rather than ambient access. | **CONDITIONAL / DORMANT** | Trigger: HDM is explicitly made extensible. |
| S31 | Extensions need explicit lifecycle/order/propagation semantics if admitted. | **CONDITIONAL / DORMANT** | Trigger: an extension/plugin surface is approved; preserve principle, no framework now. |
| S32 | Auxiliary generations need rate/token/cost/backpressure budgets if multi-call orchestration exists. | **CONDITIONAL / DORMANT** | Trigger: R2.4 admits a real multi-call auxiliary execution topology. |
| S33 | Cheap lexical parsing may produce hints/candidates but not authority. | **CONDITIONAL / DORMANT** | Trigger: optimization/fallback evidence shows material benefit. |
| S34 | Entity resolution can try exact semantic identity before controlled partial/alias matching, then eligibility. | **CONDITIONAL / DORMANT** | Trigger: natural-language identity/mechanics resolution needs this beyond existing binder behavior. |
| S35 | Structured fact register/clustering is allowed only as projection over canonical owners. | **CONDITIONAL / DORMANT** | Trigger: an actual compact fact-index consumer is required. |
| S36 | Actor recall/retrieval should weight witnessed/known evidence above mere textual mention. | **ACTIVE** | R2.3 over R2.2/Step-4 epistemic sources. |
| S37 | Spatial/travel calculations may use a deterministic sidecar where maps/routes require it. | **CONDITIONAL / DORMANT** | Trigger: a real spatial/travel subsystem requirement appears. |
| S38 | Explicit admin/debug commands may serve repair/diagnostic fallback without becoming command-first gameplay. | **INHERITED / ALREADY SATISFIED** | Existing maintenance/support command direction already covers the need. |
| S39 | Provider cache-aware rolling context may optimize stable prefixes. | **CONDITIONAL / DORMANT** | Trigger: selected deployment profile exposes measurable/reliable prompt caching worth exploiting. |
| S40 | Context selection should prevent deterministic positional starvation. | **ACTIVE** | R2.3 |
| S41 | Participant intent must bind to authenticated principal and explicit controlled actor set. | **INHERITED / ALREADY SATISFIED** | Current multiplayer/access architecture already owns authenticated participant->PLAYER/PC binding; R2.5 preserves. |
| S42 | Table administration authority is separate from PC agency. | **INHERITED / ALREADY SATISFIED** | Current multiplayer/access architecture already distinguishes creator/admin rights from character authority. |
| S43 | OOC/social coordination, diegetic speech and actionable intent need distinct channel semantics. | **ACTIVE** | R2.5 |
| S44 | Returning participant needs bounded recipient-specific catch-up rather than full transcript replay. | **ACTIVE** | R2.5 |
| S45 | Join/rejoin into active scene/sequence requires explicit current-frontier acquisition and mode admission. | **ACTIVE** | R2.5 |
| S46 | Absence/idle does not authorize AI/host takeover of a PC. | **INHERITED / ALREADY SATISFIED** | Current multiplayer/player-agency rules already prohibit implicit control transfer; preserve in R2.5. |
| S47 | Presence/typing/reconnect are UX signals, not authority or fictional state. | **INHERITED / ALREADY SATISFIED** | Current multiplayer runtime explicitly avoids presence-based authority. |
| S48 | Explicit actor/entity/scene targeting may improve context precision but cannot bypass eligibility. | **ACTIVE** | R2.3 |
| S49 | Context budgeting must degrade representation with party size/relevance rather than linearly loading every PC. | **ACTIVE** | R2.3 |
| S50 | Conflicting live mutations require scoped serialization/CAS, not global fictional turn order. | **INHERITED / ALREADY SATISFIED** | Step 5/live-scene CAS and scoped ownership already provide this. |
| S51 | Shared participants need cheap currentness/resync rather than learning changes only on their own next write. | **INHERITED / ALREADY SATISFIED** | Current multiplayer/live contracts already define ref probes and targeted refresh; no new background push requirement. |
| S52 | Collaboration transfer state should stay bounded while deeper history/canon remain durable elsewhere. | **INHERITED / ALREADY SATISFIED** | Existing live/session/history separation already establishes the core; R2.5 may add bounded catch-up semantics. |
| S53 | Shared serving/model/safety profile should be explicit where one host/table profile governs group behavior. | **ACTIVE DELTA** | R2.6 host/support envelope; exact product-visible requirement subject to current ChatGPT capability. |
| S54 | Free-form scenes may batch several short intentions before one resolution under an explicit trigger/policy. | **ACTIVE** | R2.5 |
| S55 | Spectator/replay may use read-only sanitized projections. | **CONDITIONAL / DORMANT** | Trigger: sharing/publication/spectator product feature is admitted. |
| S56 | Solo continuation of a shared campaign should be an explicit fork with separate authority. | **CONDITIONAL / DORMANT** | Trigger: product semantics explicitly require solo/shared fork. |
| S57 | Invitation/discovery is not durable write authority; authenticated membership/binding is separate. | **INHERITED / ALREADY SATISFIED** | Current multiplayer access/join policy already enforces this. |
| S58 | Human/AI/delegated controller assignment must be explicit if mixed control is supported. | **CONDITIONAL / DORMANT** | Trigger: AI-controlled PCs, companions or explicit delegation become a supported product feature. |

## 5. Roadmap derivation consequences

The item accounting changes the previous roadmap in material ways:

1. **Actor continuity precedes Context Runtime.** R2.2 defines the Actor sources/semantics before R2.3 designs how those sources are selected and budgeted.
2. **No mandatory standalone Narrative Dynamics stage.** Existing Step-4/runtime preparation, process and NPC doctrine already cover the base semantics. Narrative-planning/world-pressure candidates remain dormant unless a real unsatisfied owner-level requirement appears.
3. **No generic optional-capability review stage.** Dormant items remain dormant with their triggers; they do not become end-of-round work merely because they are STRONG candidates.
4. **Multiplayer work is a collaboration/input/context delta, not a reimplementation of Step-5 live concurrency/chronology.**
5. **Host assurance follows concrete runtime design.** ChatGPT evaluation/security/degradation is performed after R2.1–R2.5 define what must actually be supported.
6. **Machine-realization mapping remains last.** Catalog/schema/runtime/instruction/test obligations are derived only after architecture closes.

## 6. Conditional-stage insertion rule

A dormant candidate does not reserve a roadmap stage or stage number.

If its explicit revisit trigger becomes true and the resulting design must precede an existing downstream consumer, the active roadmap is changed at that time. The new bounded stage is inserted where the dependency graph requires it.

This rule prevents both loss of preserved research and premature subsystem creation.

## 7. Completeness check

- [x] Relevant current ownership/dependency subgraph was discovered through `DEV/PROJECT_MAP.md`.
- [x] Owning canonical sources were inspected for disputed/overlapping Round-1 concerns.
- [x] All 24 DIAMOND and 58 STRONG candidates are individually accounted for.
- [x] `revisit when` / applicability semantics are preserved for dormant candidates.
- [x] Research candidates are not promoted to requirements by classification alone.
- [x] Accepted Round-1 architecture is reopened only for a concrete extension/new consumer/insufficiency.
- [x] Previous roadmap headings were not used as evidence of coverage.
- [x] No public third-party/source identity is introduced.
- [x] Remaining roadmap choice was presented to and approved by the project owner.
