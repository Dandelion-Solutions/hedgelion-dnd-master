# S6D-08 — HP/LifeState/Resource/Effect/Condition/Duration/Recovery — Research & Architecture Draft

Status: **STEP 2 COMPLETE — RECOMMENDED ARCHITECTURE / NO HUMAN DECISION IDENTIFIED**

Date: 2026-08-26

## Source Manifest

The current remote basis is the authoritative S6D-08 Step-1 publication. The mandatory graph was reconstructed from AGENTS.md, both design-process owners, DEV/PROJECT_MAP.md, NEAR_TERM_ROADMAP.md, the S6D owner/brief/plan, and these current owners:

- Step 1–2 retrospective assurance final; Step-2 mechanical-state ownership; HP/Effect query, LifeState transition, Effect application/reapplication, Condition aggregation/scope, B2 recovery; assurance Slice A–D resolutions.
- Step-3 execution-boundary canonical specification and current ExecutionSegment, MechanicalEvent, receipt, Continuation and boundary-occurrence contracts.
- Step-5.2 v2 resumability; Step-5.3 temporal pending continuity; Step-5.3/5.9 integration amendment; Step-5.7 checkpoint recovery; Step-5.9 chronology plus forward-extensible-time decision; Step-5.13 GC canonical contract and resolution.
- ACTOR_MODEL, ACTIVITY_MODEL, RULE_ELEMENT_MODEL, MECHANICAL_CONTEXT, PORTABLE_ACTIVITY_VALUES, ACTIVITY_PRIMITIVE_CONTRACTS, CHARACTER_PROGRESSION_READY_PC_SEED; shipped Combat/Chronology/Runtime/Randomness/Storage/Persistence/Durability/Save/Session/Integrity owners.
- Current catalog admission, mechanical surfaces, primitive contracts, Actor/Effect/Resource/Condition/Duration/RestPolicy/TemporalBinding schemas, S6D-07 package and focused Step-2/3/S6D tests.

MECHANICAL_RUNTIME_PROPOSAL.md and historical proposals are provenance-only. No summary or roadmap was used as semantic authority.

## Residual obligation ledger

| ID | Obligation | Evidence disposition |
|---|---|---|
| S8-01 | HP/temp HP/max HP single Actor authority | accepted owner; schema needs materialized-health tightening |
| S8-02 | LifeState separate policy-owned transition | accepted owner; exact transition table needs machine seed |
| S8-03 | Actor and procedure Resource models | accepted; bounded seed and recovery responders need exact closure |
| S8-04 | Effect instance/reapplication/support/lifecycle | accepted; exact seed and compiler invariants need closure |
| S8-05 | derived Condition aggregation/applicability | accepted; presence and cumulative examples need exact seed |
| S8-06 | DurationSpec/TemporalBinding separation | accepted; exact consumer ledger and negative cases needed |
| S8-07 | owner-local scheduled triggers | accepted dormant capability; no S6D-08 supported consumer proves activation |
| S8-08 | RestPolicy completion vs owner-local recovery | accepted; exact responder matrix needed |
| S8-09 | Step-3 commit/event/receipt and idempotency | accepted; scenario assertions needed |
| S8-10 | Step-5 durability recovery and GC protection | accepted; active Effects/bindings and retry anchors remain protected |
| S8-11 | S6D-07 health/resource/effect dependency | accepted narrow contracts; generic closure must realize but not broaden them |

## Inherited S6D-07 contract ledger

| Contract | Classification | S6D-08 treatment |
|---|---|---|
| Actor intrinsic HP/LifeState readiness evidence | REQUIRES_GENERIC_S6D08_COMPLETION | materialized HP requires current+maximum_base and matching LifeState |
| resource.hit_points definition | CONFLICT_REQUIRING_AMENDMENT | no consumer; violates Step-2 no-generic-HP law; remove from support definitions/dependency list |
| Second Wind healing + resource.second_wind | ACCEPTED_NARROW_CONTRACT | healing targets Actor HP; use restores only on short-rest boundary |
| Tactical Mind conditional Second Wind consumption | ACCEPTED_NARROW_CONTRACT | no new Resource lifecycle |
| spell slots / innate sorcery resources | ACCEPTED_NARROW_CONTRACT | Actor current pools; long-rest owner-local recovery |
| Action Surge use pool | ACCEPTED_NARROW_CONTRACT | Actor feature-use pool |
| Action Surge emitted extra action | UNSUPPORTED_OUTSIDE_EXACT_CONSUMER | current-turn procedure state, never Actor ResourceState |
| effect.innate_sorcery | ACCEPTED_NARROW_CONTRACT | same target/source/definition key, replacement, one-minute local binding |
| its temporal cleanup | REQUIRES_GENERIC_S6D08_COMPLETION | indexed due discovery, idempotent Effect transition; Agenda owns no fact |
| S6D-07 active primitives/selectors | UNSUPPORTED_OUTSIDE_EXACT_CONSUMER | preserve exact consumer allowlists; S6D-08 creates no blanket activation |

The resource.hit_points row is a technical owner-conflict repair, not a product choice: it has no Activity/feature/readiness consumer, while accepted Step-2 authority explicitly forbids generic Resource state from duplicating HP.

## Supported minimal seed

S6D-08 adds one bounded machine seed, not broad SRD content:

1. character-like HP transition policy: damage consumes temp HP first; HP floors at zero; zero invokes LifeState policy; healing from zero atomically returns to active; death-save progress is stored only while dying; third success becomes stable and third failure dead without storing an impossible third counter;
2. S6D-07 Second Wind, Action Surge use, spell-slot and Innate Sorcery pools with exact short/long-rest responders;
3. condition.unconscious presence aggregation, sourced by LifeState policy rather than a copied Actor condition list;
4. condition.exhaustion remains conformance-only/nonselectable because its full per-level mechanics and level-6 terminal consequence are outside the bounded playable seed; it proves no gameplay support;
5. an explicit concentration support root and dependent illustrative Effect contract used as an architecture/conformance case, nonselectable package content until a concrete spell consumer is admitted;
6. effect.innate_sorcery as the only active metric-duration package Effect;
7. the existing periodic owner-local trigger shape remains dormant: no supported S6D-07 consumer justifies adding a periodic disease to the playable package.

## Owner and transition matrix

| Mechanic | Mutable owner | Deterministic route | Evidence |
|---|---|---|---|
| damage/temp HP | Actor HP | validated damage -> segment candidate -> temp then current -> LifeState policy -> commit | event+receipt |
| healing at zero | Actor HP + LifeState policy in same segment | bounded heal -> policy transition active -> clear progress -> commit | event+receipt |
| death saves | Actor LifeState progress | roll result -> policy transition | event+receipt; fixed RNG |
| resource spend/recovery | Actor or procedure named by definition | exact resolver op / boundary responder | occurrence+event+receipt |
| Effect create/reapply/end | world.effect | exact primitive/policy -> DAG validation -> lifecycle transition | event+receipt+order evidence |
| Condition state | no mutable aggregate owner | applicable active Effect set -> definition aggregation | derived MechanicalContext |
| duration/expiry | Effect binding | chronology due occurrence -> Effect responder | occurrence key+event+receipt |
| Long Rest | Rest procedure/RestPolicy then each state owner | qualify -> completion occurrence -> discover all -> prospective closure -> atomic commit | scoped occurrence and receipts |

## Temporal and recovery matrix

- Metric Effect expiry stores the binding on the Effect; a disposable index finds it. Retry uses occurrence plus responder/owner identity.
- Procedure boundaries use procedure identity, participant and boundary anchor; Action Surge entitlement expires in procedure state.
- Semantic rest boundaries apply only to qualifying participants. Discovery precedes mutation; same-coordinate consequences close under Step 3.
- Mechanical recovery never selects durability source. Durability recovery restores current authoritative Actor/Effect/procedure/accepted input and rebuilds derived Agenda/DAG/Condition aggregates.
- Active Effect bindings, causal order and retry anchors block GC. Terminal payload may retire only after native authority ends and every idempotency/chronology/provenance consumer has a sufficient survivor.
- No background scheduler, wall clock, campaign broadcast or global scan is required.

## Machine gap findings and recommended deltas

1. Tighten materialized Actor hp: require current and maximum_base; require life_state_id as already enforced by the envelope dependency. Cross-field maximum arithmetic remains compiler/runtime validation because derived adjustments are outside JSON Schema arithmetic.
2. Remove unused resource.hit_points from the S6D-07 package dependency closure; HP remains intrinsic Actor state.
3. Add a compact identity-bound health-effects-recovery-seed.json machine contract containing exact supported/dormant cases, owner routes, boundary responders and negative-space declarations.
4. Add a strict schema plus reference validator/tests proving package identity, schema validity, HP/Resource nonduplication, exact death/stable-recovery behavior, S6D-07 recovery, Effect replacement/expiry/support loss, Condition derivation, occurrence idempotency, derivative reconstruction and no scheduler/global scan.
5. Add canonical architecture owner DEV/ARCHITECTURE/HEALTH_EFFECTS_RECOVERY.md.
6. Do not activate new primitives or periodic content. Existing active primitives remain restricted to their reviewed S6D-07 consumers.

## Alternatives

- **Recommended: bounded integration seed + narrow schema correction.** Closes the executable architecture contract and fixes the only duplicate HP representation.
- Documentation-only closure: rejected because the unused HP Resource conflict and missing executable transition/recovery assertions would remain.
- Generic lifecycle/scheduler subsystem: rejected because accepted local owners already cover every supported case and it would duplicate Step-2/3/5 authority.

## Human decision gate

No genuine product-semantic choice remains. The supported scope stays the accepted bounded S6D-07 vertical slice; all changes follow deterministically from accepted ownership. New content breadth, alternate death rules or periodic mechanics remain absent/nonselectable and would require future admission, not a choice now.

## Step-2 exit

Source, residual and inherited ledgers are complete for the stated claims; the recommended draft has one owner per fact, no hidden scheduler/query/mutation surface, and no unresolved human decision.

