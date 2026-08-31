# R2.7 WP-08 Step 2 — Canonical Owner Evidence Slice

Status: **STEP-2 EVIDENCE SLICE COMPLETE — CANONICAL OWNERS / UPSTREAM INPUT**

Date: 2026-08-31

## Scope and method

This is the first bounded Step-2 evidence slice for WP-08. It reads the current
primary canonical owners named in the repaired Task Brief and the closed WP-07
Step-8 record. It records architecture-to-machine obligations and exclusions; it
does not claim that any current instruction, runtime, schema, catalog or test
already realizes them.

All sources below were opened on published ref
`4e31956d9fea6219a248ae6b60b4c9dc632e34d7`. Their current primary paths,
rather than historical design derivations or summaries, are the evidence basis.

## Sources read

| Source | Authority class | Relevant primary material |
|---|---|---|
| `DEV/docs/superpowers/specs/2026-08-24-r2-1-continuity-history-canonical-spec.md` | canonical R2.1 constraint | LAW R2.1-4, -5, -8, -15; R2.3/R2.4 downstream contracts |
| `DEV/docs/superpowers/specs/2026-08-24-r2-2-actor-continuity-canonical-spec.md` | canonical R2.2 constraint | LAW R2.2-1, -2, -14, -16, -17, -19, -21 through -27 |
| `DEV/docs/superpowers/specs/2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md` | canonical owner | role contracts; §§9–11, 21, 26–28 |
| `DEV/docs/superpowers/specs/2026-08-23-step-4-single-context-role-containment-canonical-amendment.md` | superseding canonical amendment | §§1–4, 7, 10–11 |
| `DEV/docs/superpowers/specs/2026-08-24-r2-3-context-runtime-canonical-spec.md` | canonical owner | LAWS R2.3-1 through -20; R2.4/R2.6 handoffs |
| `DEV/docs/superpowers/specs/2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md` | canonical owner | LAWS R2.4-1 through -30; §§6–11 |
| `DEV/docs/superpowers/specs/2026-08-24-r2-5-collaboration-multiplayer-canonical-spec.md` | canonical downstream constraint | LAWS R2.5-18 through -26, -36 through -49 |
| `DEV/docs/superpowers/specs/2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md` | canonical assurance constraint | LAWS R2.6-1 through -12; §3 instruction realization |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-10-story-projection-durability-canonical-spec.md` | canonical neighboring owner | Chronicler/Story non-authority and admitted-source/coverage constraints |
| `DEV/docs/superpowers/specs/2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md` | canonical neighboring owner | LAWS 5.12-3, -6 through -8, -16 through -17; `EMISSION_COMMIT` |
| `DEV/docs/superpowers/design/2026-08-31-r2-7-WP-07-step-8-canonicalization.md` | closed upstream audit input | F01–F06/N02 disposition and F06 implementation obligation |

## Extracted evidence and disposition

| ID | Primary evidence | WP-08 consequence | Disposition |
|---|---|---|---|
| E01 | Step-4 defines six logical roles by responsibility, eligibility, authority, input and output; a role is not a separate agent, process or model call. The amendment preserves this in one physical conversation and requires rebind before every phase. | Any Step-2 machine mapping must use one `TurnEnvelope`/logical-phase model. A second role runner, agent topology or physical-context requirement is outside WP-08. | PRESERVED CONSTRAINT |
| E02 | Step-4 forbids raw `DramaturgContext -> Narrator` transfer except for independently Narrator-eligible material. The amendment and R2.4 require lawful typed handoffs and make physical co-presence non-eligible. | Inspect current instructions and runtime boundaries for role/subject/purpose/context/handoff/output rebind and minimum semantic handoff; do not infer a safe transfer from text being in chat. | REQUIRED MACHINE MAPPING |
| E03 | R2.3 makes `RoleContextRequest -> bounded discovery -> currentness/eligibility -> packet closure -> RoleContextBundle + ContextTrace` deterministic support. A bundle is one bounded logical role/purpose/subject projection; trace is restricted diagnostic evidence, not prompt content or authority. | Locate any current machine realization separately. It must not create a second truth/currentness owner, durable generic role memory, unbounded graph walk or trace-to-player path. | REQUIRED MACHINE MAPPING |
| E04 | R2.3 assigns requiredness to the registered consumer/task contract; eligibility precedes role-local semantic use; required packet precedes optional material; representation downgrade cannot violate a required floor. `UNSATISFIABLE` is terminal/non-looping and requires a registered safe caller path. | Inspect existing profiles, callers and evaluation/test surfaces for explicit need/requiredness, legal degradation and finite fallback. Missing implementation is an obligation, not evidence for a new semantic owner. | REQUIRED MACHINE MAPPING |
| E05 | R2.1 says Story/history/current-chat visibility and prior model exposure do not widen role, subject or recipient eligibility. Material decisions escalate to the proper current/exact source class; hidden chain-of-thought, prompts, private diagnostics and unaccepted generations cannot become durable continuity input. | Inspect role-context/instruction surfaces for source escalation and the exclusion of hidden reasoning from continuity/recovery/authority. Do not turn history availability into preload permission. | REQUIRED MACHINE MAPPING |
| E06 | R2.2 gives source Actor the non-epistemic private-continuity boundary. `world.knowledge` remains the exclusive proposition-stance owner. One cognition assessment has one source Actor, explicit purpose and bounded eligible evidence/current state; R2.4 owns phase vocabulary. | Inspect Actor phase entry, purpose/result shape and deterministic acceptance boundary. Any Actor-private continuity mapping must not duplicate belief/suspicion or use ambient role context as evidence. | REQUIRED MACHINE MAPPING |
| E07 | R2.4 makes `TurnEnvelope` transient control, preserves registered phase/result vocabulary, requires rebind before phase and a fresh Narrator rebind after Chronicler. It forbids raw private handoff and hidden-reasoning dependency; only validated Narrator output reaches ordinary visible emission. | Inspect current Project Instructions/CORE for one hierarchy: package/engine contract, activation, envelope, role frame and bundle. A prompt fragment cannot create phase, authority or eligibility. | REQUIRED MACHINE MAPPING |
| E08 | R2.4 treats full preloaded CORE as physically present but semantically activated; lower layers may narrow but not override law. R2.6 requires an explicit shipped instruction equivalent to active-role eligibility, physical-presence non-eligibility and lawful later normal use. | Identify the exact single owner/activation route for this instruction and detect copied, stale or conflicting variants. Exact wording and tests remain later realization work. | REQUIRED MACHINE MAPPING; WP-07/F06 CARRY-IN |
| E09 | R2.5 keeps contribution use purpose/scope/generation-bound, makes catch-up recipient projection, excludes planning from player catch-up, forbids full planning preload and preserves Narrator/recipient eligibility despite planning co-presence. | Inspect multiplayer/catch-up/planning consumers only through concrete role-context edges. Planning must not become Narrator/catch-up evidence by shared physical availability. | REQUIRED MACHINE MAPPING |
| E10 | Step-5.10 keeps Chronicler/Story noncanonical and source-admitted; R2.4 prohibits same-envelope Story feedback. Step-5.12 rejects private drafts/hidden reasoning as emission, validates eligible Narrator content before `EMISSION_COMMIT`, and keeps disclosure recipient-scoped and separate from PC knowledge. | Inspect Narrator/Chronicler/result/emission surfaces for protected output, fresh rebind, pre-emission integrity and no auxiliary disclosure path. | REQUIRED MACHINE MAPPING |
| E11 | WP-07 closure classifies F03/F04/F06 as `IMPLEMENTATION_OBLIGATION`; F06 specifically retains R2.6 explicit active-role/`RoleContextBundle`/lawful typed-handoff instruction realization. It authorizes no immediate runtime/schema/catalog/storage change. | Preserve WP-07 as closed input. Record where WP-08 later maps F06; no WP-07 finding is reopened by this slice. | CARRY-IN; NO CONTRADICTION |

## Reconciliation

The source set is internally compatible for this domain:

- the Step-4 physical-isolation wording is superseded only as specified by the
  single-context amendment; logical eligibility, typed handoffs and deterministic
  Context Assembler ownership remain intact;
- R2.1 continuity orientation and R2.2 Actor-private continuity are inputs to
  bounded R2.3 selection, not alternative authority or role-context stores;
- R2.4 supplies the logical execution/instruction hierarchy, while R2.6 supplies
  the observable containment and lawful-later-uptake acceptance requirement;
- R2.5, Step-5.10 and Step-5.12 constrain consumers and output boundaries without
  redesigning their owned domains.

No product-owner decision, authority conflict, compatibility-policy choice, risk
acceptance or material scope choice is exposed by this canonical-owner slice.

## Next evidence slice

Read the actual current Project Instructions, CORE activation/reasoning/runtime
surfaces, relevant schemas/catalogs and tests named in the Task Brief. Map each
observed surface to E01–E11 as `SATISFIED`, `STALE_DEBT`,
`IMPLEMENTATION_OBLIGATION`, `VERIFICATION_OBLIGATION`, `NO_DELTA` or
`CONTRADICTION`; do not create implementation artifacts.
