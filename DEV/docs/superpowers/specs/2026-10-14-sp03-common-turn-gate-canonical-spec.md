# SP03 — Actual turn occurrence and common caster slot gate

Status: **TECHNICALLY REVIEWED CANONICAL DESIGN — LOCAL STEP8 SYNCHRONIZED; PUBLICATION AND INDEPENDENT SENIOR STOP2 PENDING**.
Date: 2026-10-14. Source basis: `75bc49af2fc6ca3159c18c4e59fd63befaa0894b`.

Sole implementation-facing owner of bridge B. Frozen R3 retains exact reviewed B-R2 semantics; supplied fresh independent Step6 `ses_ec4669fdeffeEgdXm9m8BF8ciG` PASS / AT6-01..04 CLOSED, HumanDecision NO. [History](../design/2026-10-14-sp03-auth-turn-history/README.md) is evidence/provenance, not parallel law. Actual GAME turn/admission/reset/slot atomic producer **NOT_ESTABLISHED**; DEV transitions/shape do not prove it. No installed generation/profile/schema activation, implementation GO or self SeniorStop2. Types/closed-object/absence rules use [input owner§1](2026-10-14-sp03-authenticated-input-canonical-spec.md#1-ownership-notation-and-invariant).

## 1. Exact common definition, subject and scope

Only concrete procedure.combat_minimal actual accepted turns are issued here. No host message/noncombat/generic Procedure/cursor becomes a turn. Immutable existing execution.spell_cast.srd521 contract declares exact common definition `progress.spell_slot_per_actual_turn`, generation1:

`{definition_key,definition_generation:1,profile_id:lifecycle.progress.turn_gate,owner_family:world.actor,subject_role:rule_defined_caster,provider_kind:procedure.combat_minimal,boundary_id:boundary.turn_start,reset_policy:next_accepted_actual_turn,consume_policy:accepted_slot_expenditure_to_cast}`.

Every admitted spell/class/item/mode slot-to-cast consumer binds that SAME definition/context; compiler rejects aliases/divergent descriptor. No catalog kind/registry/content primitive. Slotless/ritual retain own costs and no consumption. Constants/transitions are immutable contract, not mutable Boolean/Effect/Rule Element/history.

Ordinary principal=physical=source=origin Actor owns gate; payer/action/reaction budgets independently bound. Split source needs exact admitted rule-defined caster Actor/binding generation/native transfer, never inferred payer/body equality/copy/second gate; unproved split holds. Physical/principal lifecycle law unchanged. Resistance/re-entry target/source-local gates stay independently keyed/owned, not common caster gate. Actual occurrence interface does not produce their health/progress; Magic Missile lawful simultaneous/controller order is not lexical occurrence/caster ID order.

### 1.1 Concrete3/generic2 dispatch and narrow ordering

Validate envelope/native ID first, then subtype/schema. procedure_kind=procedure.combat_minimal requires full concrete target schema3/relational validator. Generic retains closed schema2 spent/casting/progress grammar and no current_turn_basis; absent discriminator lawful only when that actual generic grammar validates. Unknown kind, concrete2, schema3 without concrete kind or generic flattening rejects; number alone doesn't choose subtype. This is not a global Procedure2→3 conversion.

runtime_execution linked-Procedure/owner-schema and mechanics Procedure binding dispatch alike. Pending linked offer still needs exact identity/link/lifecycle ACTIVE. Concrete turn_active validates current_turn_basis; valid between_turns or generic ACTIVE can remain linked to an otherwise lawful pending offer without issuing slot permission.

September21 generation1 RULE_OWNED_ORDERED remains ONLY current R AWAITING_CHOICE/AWAITING_REACTION→its current Continuation/G→exact native offer/responder/candidates plus exact linked Procedure where present. Concrete3 replaces old schema2-only linked projection check, not a Procedure-only ordered producer. ACTIVE combat/current turn alone proves neither ordered family nor simultaneous-choice controller. Missing/stale/foreign referenced ordering owner holds, never downgrades to INDEPENDENT_IMMEDIATE. No new ordering semantic generation.

## 2. Procedure-native occurrence

Concrete current_turn_basis is required iff ACTIVE/turn_active, forbidden otherwise. Its exact members:

| Member | Type / law |
|---|---|
| basis_generation | Gen=1 |
| boundary_id | boundary.turn_start |
| producer_profile_id / producer_profile_generation | procedure.start_turn /1 |
| execution_owner_kind / execution_owner_id / segment_sequence / segment_id | runtime.command or runtime.resolution / ID /integer≥1 /ID; accepted embedded owner edge |
| local_boundary_key | turn_start, maximum one issuance per this Procedure/start segment |
| active_participant_id | ID=initiative_order[active_turn_index] at start |
| round_number / active_turn_index | integers≥1/≥0; accepted cursor equal current while turn_active |
| before_procedure_revision / after_procedure_revision | integers≥0, after=before+1 for establishing edge, not later revision |
| turn_occurrence_key | injective encoded key below |

Campaign/Procedure from native envelope/current source; immutable Procedure ID never reuses after terminality, no second lifecycle ID. Issuer validates predecessor ACTIVE/between_turns/no round pending, exact participant/permutation/budget keys/capacity≥spent/index and actual native request. Phase/budget reset/basis/segment/event/receipt/idempotency/dirty/root closure co-establish. DTO/string/state_changed after-digest is not native acceptance proof.

Key generation1: ordered strings `(campaign_id,procedure_id,execution_owner_kind,execution_owner_id,canonical decimal segment_sequence,local_boundary_key)`. Start ASCII `HDM-TURN-OCCURRENCE:1:`, append each decimal UTF-8 byte length +ASCII colon+exact UTF-8 bytes. Key=`turn.`+lowercase hex of ENTIRE frame. No hash-collision assumption/delimiter ambiguity/normalization; invalid Unicode/noncanonical integer/unsupported generation rejects. Basis retains explicit generation; bare key cannot issue. Same accepted edge key survives retry/movement/absorption; different Procedure/owner/sequence injectively distinct, IDs not reallocated.

Transient BoundaryOccurrence rederives only from validated native basis: boundary_id, producer_id=Procedure.id, scope_subject_id=active_participant_id, occurrence_key=turn key, causal_position=segment_id. No persisted independent boundary owner. Current Procedure proves active currentness; Actor compact cause retains past start meaning.

| Transition | Exact consequence |
|---|---|
| initialize | ACTIVE/between_turns, no turn basis even round1/index0; fixed initiative RNG; no Actor reset |
| start_turn | one accepted basis, active participant budgets reset; retry same edge |
| spend_action | exact active actor/budget, basis unchanged |
| spend_movement | exact active actor/budget, basis unchanged; durable location separate coupled owner route |
| end_turn | remove active basis with accepted closure; preserve required historical causes; cursor/pending law unchanged |
| advance_round | between_turns pending only, cursor change but no new turn until start |
| terminate | TERMINAL/terminated/no active basis; no free occurrence/reset; required accepted continuity survives |

Reaction on another creature's turn uses THAT current actual turn, while caster may differ and costs/control are separate. Between-turns/terminal/wrong subtype/missing source/provider cannot grant slot permission. The convenience `advance_combat_turn` helper is not composed with this seven-transition lifecycle. Direct Procedure start has execution_owner_kind=runtime.command/ID=K/K-owned segment under input owner; no fake action/rootR.

## 3. Actor-native value and bounded causal evidence

Keep `spell_progress[common_key]={profile_id:lifecycle.progress.turn_gate,turn_occurrence_key:ID,consumed:bool}` as sole current gate value. Add optional closed `spell_progress_basis[common_key]` only for THIS definition, not arbitrary profile map. Populated progress requires coherent companion; evidence cannot override balance.

Companion exact fields:

* basis_generation1, definition_generation1, subject_actor_id=actual gate Actor.
* admission:`{kind:native_actor_creation,execution_owner_kind,execution_owner_id,segment_sequence,segment_id}` with§2 types. Actual creation enrolls gate definition BEFORE any slot consumer spends. Minimal lifetime cause persists; absence/capability acquisition cannot fabricate it.
* establishment? `{branch:INITIALIZE|RESET,turn_basis:TurnEvidence,transition:TransitionEvidence}`, required iff progress exists. INITIALIZE only protected creation/no progress; RESET coherent predecessor/different genuine turn. Immutable current establishment until lawful replacement.
* consumption? `{transition:TransitionEvidence,cast_execution:CastEvidence,slot_expenditure:SlotEvidence}`, required iff progress.consumed=true, forbidden iff false.

TurnEvidence=complete§2 basis plus campaign_id/procedure_id, historical immutable cause not current budget copy. TransitionEvidence=`{execution_owner_kind,execution_owner_id,segment_sequence,segment_id,before_actor_revision,after_actor_revision,predecessor_turn_occurrence_key?,predecessor_consumed?}`; revisions integers≥0, after=before+1 for complete segment. Predecessor pair present together for RESET/CONSUME from existing progress; absent for creation/INITIALIZE. Sufficient validated prior relation/replacement avoids unbounded predecessor-receipt walks; arbitrary assertion doesn't qualify.

CastEvidence=`{root_command_id:ID,resolution_id:ID,consumer_id:ID,activity_id:ID,catalog_context_fingerprint_generation:Gen,catalog_context_fingerprint:SHA,segment_sequence:integer≥1,segment_id:ID}`. Exact accepted compiled/source identity, not whole context snapshot; compatible interpretation stays protected while needed.

SlotEvidence=`{owner_family:world.actor|world.asset|runtime.procedure,owner_id:ID,resource_definition_id:ID,amount:integer≥1,before_resource_revision:integer≥0,after_resource_revision:integer≥0,before_amount:integer≥0,after_amount:integer≥0,cost_profile_id:ID,cost_profile_generation:Gen,cost_boundary_key:ID}`, participant_id only/required for Procedure resource. Resource revision after=before+1. Actor/Asset remaining after=before−amount; Procedure spent after=before+amount with capacity independently validated. Exact admitted CostSpec supplies actual slot/amount/model/boundary; action/movement not slots. Source profile name alone insufficient. Amount witness is accepted cause, never current quantity/restoration authority; deeper still-live consumers retain separate evidence.

Validate companion key/generation/subject vs compiled descriptor/native Actor; progress key=establishment turn key; exact frame/native campaign/Procedure/edge; positive current observation requires equality to current active Procedure basis/participant/cursor/producer. Consumed CastEvidence edge=consumption transition=actual resource edge in SAME segment/turn. Combined normalize+consume retains both logical causes on one real edge and actual before/after revision; consumption predecessor is actual old progress or absent for INITIALIZE, not fictitious intermediate revision. Separate consume predecessor is current turn/false. Missing establishment, resource-only receipt, incompatible source/consumer/cause rejects.

First-use scope is native creation admission. Admission may exist without progress outside current combat; read holds missing progress. First actual turn can INITIALIZE from protected creation because every admitted slot path prevented earlier expenditure without this gate. Capability removal never clears admission/progress; re-enrollment cannot erase spend. Old/imported/unproved missing lifetime holds, no invented certification/migration. Existing gate RESET requires actual current accepted new turn and exact protected predecessor. Numeric/lexical key/round difference not newness; reused same key cannot reset. Provider change without admitted subject continuity mapping holds rather than any different ID granting reset. Split/transfer subject uses exact source law or holds.

## 4. Lazy native transitions, read phase and atomicity

Read-only SP03 never initializes/resets/enrolls/spends/issues accepted receipt. Slot-positive observation missing definition/occurrence/progress/cause→scoped hold, never implicit false. Already coherent current progress alone permits positive unused/consumed observation; predicted normalization is not permission.

Native creation-admitted missing progress→INITIALIZE on exact current turn; may combine with actual CONSUME on one edge, both causes recorded. Coherent older turn→RESET with current cause/predecessor; preserve admission and required survivor/protection before replacing old consumption. No eager all-Actor reset/scan. Current turn/false→CONSUME only one genuine slot-to-cast expenditure; true→reject second slot across all sources, exact stored retry reused. Slotless/ritual may proceed on own rules; this is not an all-casting ban.

Slotless/ritual/countered-without-slot/interrupted long-before-slot don't consume; actual action/component/time/concentration costs persist without invented refund. Long preparation/start/repeated Magic actions aren't slot cost; actual accepted completion/source slot boundary uses THAT then-current turn. Secret-invalid target retains actual source spend/no-effect law, no free probe/refund. Exact no-slot branch doesn't acquire missing slot-gate dependency merely for preflight; later actual-slot branch acquires full then-current dependency before edge. No-slot success is not unused-gate proof.

Exact native engine inventory profiles: progress.spell_slot.admit/initialize/reset/consume each contract generation1, no content primitive/callback bypass. Only native final plan builder dispatches from admitted graph. SP04/later producer establishes them; SP03 preparation cannot prove it backwards.

Infrastructure.actual_combat_turn generation1 derives exact Procedure from accepted R/Continuation procedure_id, never ambient caller state. Full concrete cause/Actor subject/admission/progress/cost/remaining resolvable execution/contract refs join finite observation. Host/independent activity validator/spell membership derive identical full base/input/turn/cost/declared Effect-Asset union. Embedded witness prevents unbounded histories; input owner's auth/history remains source evidence, not fake role. Expansion reacquires full union. Final edge validates active occurrence/Actor predecessor/resource/binding/cost/current route/operation authority. Changed turn/source/control invalidates prospective work at safe recompute phase with accepted fixed RNG/choice preserved. Cache includes definition/subject/binding/occurrence/cause/pins, not global revision.

Lawful HOT one fenced native segment atomically establishes progress/companion/actual resource/execution/event/receipt/fixed RNG/mandatory children/idempotency/dirty/required helpers or none. Raw `atomic_owner_mutation`, ACTOR-phase shape admission and synthetic ExecutionStore event aren't proof. LIVE pre-CAS prospective; exact-source CAS accepts, HOT adopts confirmed result. All inseparable mutated owners need one lawful accepted domain or bounded prerequisite close/freeze→exact final sources→forward coherent authority/semantic closure before mutation. Otherwise hold; never slot/gate half-spend/distributed transaction/network wait in SQLite. Partial prerequisite freeze is technical, not fraction of cast; accepted edges never rollback after later failure.

## 5. Recovery, protection, failures and concrete protocol

Current active Procedure roots/exact Actor/command roots/interpretation/protected cause hydrate first. Recovery rederives transient occurrence/validates progress/evidence, never starts/resets. Terminal Procedure no positive active turn but preserves required historical retry cause. Save/restart/unrelated revision/absorption/source movement preserve identity and do not advance fiction/RNG/unused Boolean. Missing/moving selected source cannot fall back campaign/cache.

Lazy gate has no independently-due reset obligation: normalize only at requested native use and hold reader beforehand. Other independently-due turn-start/health/Effect mechanics KEEP mandatory temporal enrollment; direct reachability cannot waive Step5.2 law13. Creation admission/owner links rebuild from native roots, not registry. Retain minimal lifetime admission/current establishment plus consumption iff true, not full turn/cast chains. Other protected causal/retry consumers need sufficient survivors. Unknown refs remain resolvable; only validated compact identity-only cause projection may outlive detailed targets. Hash/order alone not causal survivor. Same-domain protection/survivor/reference changes join edge; cross-domain existing typed protection before/with escape or lawful fence; confirmed survivor first, release can lag, incomplete blocker proof retains, no all-LIVE scan.

Use existing AUTHORITY_UNAVAILABLE/REVALIDATION_REQUIRED/CAPACITY_REQUIRED and exact native source failures: failure.action_economy_scope_invalid only for its existing admitted budget/constraint meaning, never generic auth; failure.idempotency_conflict/state_revision_conflict for their own identities/currentness; recovery READY/RETRY/BLOCKED with MISSING/CORRUPT/INCOMPLETE/AMBIGUOUS. Ambiguous establishment retains exact attempt/basis and resolves actual edge before retry. No new Resolution/error registry/permission lease; missing gate doesn't deny separately admitted no-slot branch.

Concrete seven-transition request/result initial schema_version1, existing fields/dispositions preserved; result new_value points concrete state3 and still exactly one Procedure mutation. Producer gets actual execution/segment/local-boundary coordinate from native builder, not caller authority fields. Later coupled cast uses general NativeSegmentEstablishment, not single-owner conformance result. State_changed event initial outer schema_version1, payload procedure_state_schema_version3/state_digest_generation1; after_state_sha256=SHA256(ASCII `HDM_PROCEDURE_STATE/1\n` + complete accepted new-state JSON, sorted keys, compact comma/colon, ensure_ascii=false, allow_nan=false, UTF-8, no normalization). State schema is hashed. Exact actual segment/root/causal ID independent of DEV idempotency spelling. Existing event kind/profiles/revisions/stable ordinal retained. Unqualified old digest not same contract. Events/receipts derive actual accepted final native result, never caller documents. Combined normalize/consume one segment/revision/two causes; no standalone ExecutionSegment/BoundaryOccurrence or new statuses.

## 6. Realization targets and proof limits

Architecture targets only: concrete state2→3; generic2 unchanged; Actor envelope2→3 for strict companion consumers; turn key/native/infrastructure semantic generations1; concrete request/result/event initial schemas1; qualified state digest1. Shared progress value unchanged. Every strict producer/parser/continuity/native validator/transition/event/compiler/inventory/read/membership/recovery/protection consumer synchronizes. Later admitted encoding/participating-field changes bump owning namespace. Catalog2 remains only for compatible additive vocabulary, not incompatible ABI; module-local material revisions and exact package/inventory/compiler identities assess actual realization. Released breaking persisted semantics requires family+campaign generation/migration; clean-slate cannot fabricate old native causes.

DEV-only canonicalization VERSION_IMPACT: NONE; no active machine projection changed. SYSTEM_IMPACT remains ARCHITECTURE_REVIEW_REQUIRED for implementation reconciliation. Actual GAME producer/admission/init/reset/slot/crash/native recovery **NOT_ESTABLISHED**; DEV seven transitions/shape/temporal evaluator never substitute. Cases B01–B24/BR01–BR03 plus direct-start/response cross-cases are in [63-case/19-wire ledger](../design/2026-10-14-sp03-auth-turn-history/case-source-ledger.md), requirements/proof obligations not passing tests. Required actual producer/pre/post crash/fixed retry/two-source race/other-creature reaction/compact recovery/LIVE movement proof remains. No full SP03/full casting/SP04 GO inferred or reversed prerequisite. Independent publication/SeniorStop2 and later approved plan/envelope/Senior implementation GO remain separate.
