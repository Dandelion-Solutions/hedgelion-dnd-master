# R2.7 WP-08 Step 2 — Current Instruction and Representation Evidence Slice

Status: **STEP-2 EVIDENCE SLICE COMPLETE — CURRENT SHIPPED SURFACES**

Date: 2026-08-31

## Scope

This slice reads the current shipped package-instruction surfaces and the
task-brief-selected schema/test surfaces at published ref
`d783d59a28ff46984f261011f585b9ad855f3596`. It distinguishes an observed
behavioral guard from an accepted R2.3/R2.4 machine contract. It does not infer
global absence from a focused source set and does not implement a mapping.

## Sources read

| Source group | Exact paths read |
|---|---|
| Package/bootstrap boundary | `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`; `GAME/INSTALL/00_DND_BOOTSTRAP.md` |
| CORE activation/instruction boundary | `GAME/CORE/PLAY_POLICY.md`; `GAME/CORE/CORE_INDEX.md`; `GAME/CORE/RUNTIME.md`; `GAME/CORE/AI_REASONING.md` |
| Information, Actor, output and multiplayer consumers | `GAME/CORE/INFORMATION.md`; `GAME/CORE/NPC.md`; `GAME/CORE/NARRATIVE.md`; `GAME/CORE/MULTIPLAYER.md` |
| Persistent schema samples | `GAME/SCHEMA/current_state.schema.yaml`; `GAME/SCHEMA/session.schema.yaml`; `GAME/SCHEMA/player.schema.yaml`; `GAME/SCHEMA/event.schema.yaml`; `GAME/SCHEMA/checkpoint.schema.yaml`; `GAME/SCHEMA/live_scene.schema.yaml` |
| Runtime-representation samples | `DEV/SCHEMAS/runtime-command-state.schema.json`; `runtime-continuation-state.schema.json`; `runtime-intent-plan-state.schema.json`; `runtime-interaction-state.schema.json`; `runtime-mechanical-event-state.schema.json`; `runtime-procedure-state.schema.json`; `runtime-resolution-state.schema.json`; `runtime-resolution-trace-state.schema.json` |
| Existing test/evidence samples | `DEV/TESTS/RUNTIME_CONTEXT_RESEARCH_CASES.md`; `DEV/TESTS/test_step_5_0_contamination.py`; `DEV/TESTS/test_s6d_04_mechanical_context_contract.py` |

## Observed surfaces and dispositions

| ID | Observed primary evidence | Relation to canonical owner evidence | Disposition |
|---|---|---|---|
| S01 | Project Instructions and bootstrap select/validate one exact runtime package and bind package-relative reads to one transient `current_runtime_root`. They state that detailed gameplay behavior is owned by bootstrap/CORE after runtime selection. | This is a package/bootstrap boundary, not an ordinary logical-role/instruction owner. It must remain separate from the R2.4 phase hierarchy. | NO_DELTA |
| S02 | `PLAY_POLICY.md` explicitly separates cached engine instructions, module activation, campaign retrieval, tools and external research. It preloads full CORE once, says this is not ChatGPT Memory/campaign canon, and keeps campaign data lazy. | Directly supports the R2.4 distinction full preloaded CORE vs semantic activation vs role-local evidence. It does not itself establish a `RoleContextRequest`, bundle, trace or typed handoff contract. | PARTIAL SUPPORT; REQUIRED MAPPING |
| S03 | `CORE_INDEX.md` repeats “preloaded != active”, routes activation to module headers and identifies always-active correctness guards. `PLAY_POLICY.md` says the index cannot create a competing activation policy. | Supports one activation route and rejects copied activation authority. It is routing/activation evidence, not R2.3 eligibility/currentness authority. | NO_DUPLICATE_OWNER |
| S04 | `AI_REASONING.md` requires the state-to-narration order, information compartmentalization, a smallest authoritative working set and escalation when a concrete unresolved issue changes a material result. | These are compatible behavioral guardrails for R2.1 source escalation and Step-4 knowledge separation. They do not supply the registered R2.3 packet/trace/outcome semantics or R2.4 phase/rebind contract. | PARTIAL SUPPORT; REQUIRED MAPPING |
| S05 | `INFORMATION.md` keeps knowledge sourced/perspectival. `NPC.md` requires NPC knowledge boundaries and sparse goals/intentions. `NARRATIVE.md` makes narration a projection of resolved state and preserves PC agency. | Compatible with R2.1/R2.2/Step-4 but operational prose cannot replace source-Actor/private-continuity versus `world.knowledge`, typed handoff or pre-emission machine contracts. | PARTIAL SUPPORT; REQUIRED MAPPING |
| S06 | `MULTIPLAYER.md` binds one authenticated user to one active player identity and states that multiple players share objective world while each PC/player has separate knowledge. | Compatible with R2.5 recipient-scoped eligibility. It is not evidence that catch-up/planning/Narrator boundaries are already realized. | PARTIAL SUPPORT; REQUIRED MAPPING |
| S07 | The selected campaign schemas represent world/session/player/checkpoint/live-scene concerns. Their inspected text contains no `RoleContext`, `TurnEnvelope` or `ContextTrace` carrier. `player.schema.yaml` explicitly says policy authority never bypasses information eligibility or native validation. | This supports the accepted non-persistence presumption: these existing records are not silently repurposed as a generic durable role/context owner. It does not prove all future representation choices. | NO_DURABLE_ROLE_CONTEXT_RECORD; NO_DELTA |
| S08 | The inspected `DEV/SCHEMAS/runtime-*.schema.json` files and S6D mechanical-context contract test are specialized existing machine-contract surfaces. The latter explicitly tests exact invocation-generation bindings and structural schemas that do not claim execution authority. | Existing “context” terminology is not by itself R2.3 RoleContext Runtime authority. Any reuse requires a later exact owner/interface mapping, not name-based promotion. | CANDIDATE REALIZATION SURFACE ONLY |
| S09 | `RUNTIME_CONTEXT_RESEARCH_CASES.md` verifies exact package selection, full CORE preload, “context is not ChatGPT Memory”, activation distinction, no CORE reread and lazy campaign data. `test_step_5_0_contamination.py` tests retired catalog/schema contamination. | These give direct regression evidence for S02/S03 and narrow structural non-duplication, but do not test R2.6 behavioral containment/lawful-later-use, phase rebind, typed handoffs or protected trace/output paths. | VERIFICATION OBLIGATION |
| S10 | No inspected current surface asserts that a persistent session/current/checkpoint/player record is the authority for hidden reasoning, role frames or a complete private bundle. | This agrees with R2.1/R2.3/R2.4 prohibitions. It is a negative result limited to this named source set; broader repository search/reconciliation remains required before a full Step-2 conclusion. | NO_DELTA; CONTINUE EVIDENCE |

## Current evidence route

```text
Project Instructions / bootstrap
    -> exact package root
    -> full CORE cache
    -> header-driven semantic activation
    -> targeted campaign retrieval / existing operational guidance
```

The route has no identified competing package/bootstrap authority. Its remaining
WP-08 question is not whether CORE may be cached; it is how the existing route
will be mapped to the accepted active-role, R2.3 bundle/trace, typed-handoff,
fresh-Narrator-rebind and R2.6 explicit-containment requirements.

## Open evidence work

The next Step-2 slice must reconcile the remaining actual runtime/catalog/test
consumer graph, including all material references to role/context/instruction
terms and the precise current owner for the WP-07/F06 instruction obligation.
It must also distinguish absent realization from stale prose and from a
verification-only gap. No human decision is requested by this slice.
