# Health, Effects and Recovery

Status: **CANONICAL S6D-08 OWNER**

## Authority map

| Semantic fact | Mutable authority |
|---|---|
| current and temporary HP | Actor hp |
| maximum HP basis | Actor hp base/adjustment plus derived health.maximum |
| current LifeState and transition progress | Actor LifeState fields under the bound LifeStatePolicy |
| persistent Resource consumption | Actor/Asset ResourceState selected by ResourceDefinition |
| procedure budget consumption | runtime.procedure participant ResourceState |
| one Effect application | world.effect |
| current Condition result | derived aggregation of applicable nonterminal Effect applications |
| intrinsic Effect deadline | the Effect temporal_binding |
| owner-local periodic next-due fact | the Effect scheduled_trigger_state |
| rest qualification/completion | RestPolicy/rest procedure |
| committed mutation fact | MechanicalEvent |
| execution outcome/evidence | receipt/trace |

HP and temporary HP are not generic Resources. No world.condition or mutable Actor condition list exists. DurationSpec, TemporalBinding, boundary occurrence, Signal and StateDelta are values, not independent lifecycle owners.

## Health and LifeState

A materialized hp object contains current and maximum_base; temporary and maximum_adjustment are optional. Materialization requires life_state_id in the same Actor transition.

Damage applies to temporary HP first, then current HP, flooring current at zero. Healing applies to current HP up to the pinned derived maximum. Any mechanically material health change and required LifeState change are candidates in the same ExecutionSegment.

The bound LifeStatePolicy owns transition semantics. HP arithmetic does not derive a competing lifecycle. For the supported character-like policy:

- active reaching zero enters dying and initializes death-save progress;
- remaining damage at zero at least equal to derived maximum HP causes immediate death;
- damage while dying or stable adds one death-save failure, or two for a critical hit, enters/remains dying when below three, and transitions to dead at three; massive damage at zero kills from either state;
- a natural 1 death save adds two failures; a natural 20 restores one HP, enters active and clears progress;
- healing a dying or stable Actor above zero enters active and clears progress;
- a third death-save success transitions to stable;
- a third death-save failure transitions to dead;
- the stored dying counters remain 0–2 because the third result is the transition, not a persisted counter value;
- stable owns a fixed-RNG 1d4-hour recovery TemporalBinding; the fixed roll remains receipt/retry evidence rather than part of the binding. When due, the Actor regains one HP, enters active and clears progress. Active/dead own no LifeState progress.

The LifeStatePolicy atomically creates an applicable condition.unconscious world Effect when entering dying/stable and terminates that source when entering active/dead. The Effect supplies Condition aggregation without copying Condition state onto the Actor.

Derived maximum HP is maximum_base plus maximum_adjustment with a floor of zero for the supported policy. A decrease clamps current HP in the same segment; maximum zero enters dead. Temporary HP is unchanged by a maximum change.

## Resources and mechanical recovery

ResourceDefinition chooses Actor, Asset or procedure lifetime and current/spent storage. Capacity is calculated from pinned engine state. A canonical normalization cannot depend on invocation-adjudicated input.

Supported bounded pools store nonnegative integers. Actor resource keys resolve an admitted Actor-owned ResourceDefinition, current cannot exceed pinned capacity, and a capacity decrease normalizes current in the same segment.

RestPolicy qualifies a rest and emits one scoped completion boundary. It never enumerates or performs cross-domain mutations. The boundary resolver discovers all owner-local responders before mutation, computes same-coordinate prospective closure, and atomically commits through Step 3.

The supported package responders are exact:

- the shared Second Wind/Tactical Mind pool has two uses at the supported Fighter level, regains one expended use on short-rest completion, and restores to capacity on long-rest completion;
- spell-slot level 1 and Innate Sorcery pools restore to capacity on long-rest completion;
- Exhaustion is conformance-only/nonselectable in this bounded seed; partial counter/recovery semantics do not imply gameplay support.

The Action Surge extra-action entitlement is procedure participant state for the current turn. It is not Actor ResourceState.

## Effects, Conditions and support

Each application is one canonical `world.effect` record. Its envelope owns stable application identity (`id`), `kind` and `definition_id`; its `state` owns target, optional source, rules origin, immutable structural support parent, parameters, causal application order, temporal bindings and active/terminal lifecycle. `definition_id` and any derived reapplication key are forbidden as pseudo-fields inside Effect state. Reapplication matching is derived from the definition-owned key over canonical envelope/state fields; for the admitted Innate Sorcery case this is `(state.target_id, state.source_id, envelope.definition_id)`. Replacement terminates the prior envelope-owned episode and creates a new envelope-owned episode in the same segment.

Reapplication matching and action are definition-owned. Prospective activation validates exact references, parameter declarations, applicability and the scoped dependency/support DAG before commit. A support parent ending terminates descendants with effect_end.support_lost; a child ending does not mutate its parent. No detach or generic reverse-lifecycle policy exists.

Condition definitions own aggregation and intrinsic mechanics. Applicable nonterminal Effect applications are inputs. Presence aggregates once; cumulative units preserve per-application provenance and bounds. Suppression/inapplicability can remove an application from the current aggregate without making it terminal.

## Duration, boundaries and due work

Definitions own reusable DurationSpec. Concrete Effects own TemporalBinding. Metric, procedure-boundary and semantic-boundary bases remain distinct. Remaining duration is derived.

Temporal Agenda and the concrete dependency DAG are disposable indexes. Due processing is driven by accepted chronology/procedure/rest transitions and indexed owner bindings. There is no background scheduler, global event queue, wall-clock authority or campaign-wide scan.

An occurrence is scoped and stable. Responder idempotency uses occurrence_key plus responder owner identity. Processing phases are DISCOVER, PROSPECTIVE_CLOSURE, ATOMIC_COMMIT, then EVENT_AND_RECEIPT. Same-coordinate consequences use the common bounded Step-3 chain contract.

Owner-local scheduled triggers remain an admitted shape but no periodic playable content is activated in S6D-08. The generic concentration support case is conformance-only until a real package consumer is separately admitted.

## Durability recovery and cleanup

Recovery selects current authoritative state under Step 5, restores Actor/Effect/procedure owners and accepted fixed execution inputs, then rebuilds Agenda, scoped DAG and Condition aggregates. It does not restore derived indexes as authority.

Active bindings, structural support, causal order and live retry/idempotency consumers protect their required evidence from cleanup. Terminal Effect detail may retire only after native authority has ended and all protected chronology, provenance, reference and retry obligations have sufficient survivors. Missing required evidence fails closed and is never invented.

## Execution contract

Every supported mutation follows:

validated invocation -> pinned evaluation -> prospective ExecutionSegment changes -> accepted segment disposition -> owner mutation -> MechanicalEvent -> receipt/trace

Retry reuses fixed RNG and accepted causal inputs. It does not reapply an already committed owner response or create a second Effect episode.

## Machine owner

GAME/RULES/packages/hdm.rules.dnd2024-srd52-core/health-effects-recovery-seed.json is the exact bounded machine seed. It is constrained by current schemas/catalogs and focused S6D-08 tests. It does not promise full SRD mechanical-state coverage.

The package capability record binds an exact closed two-file content set with per-file SHA-256 values and an aggregate content-set digest. Missing, extra or modified S6D-08 content fails reconstruction.

