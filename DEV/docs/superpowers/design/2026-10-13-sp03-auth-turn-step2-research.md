# SP03 authenticated-input and common-turn bridges — Step2 research/draft

Date: 2026-10-13. Status: **RESEARCH / UNACCEPTED ARCHITECTURE DRAFT + SELF-PERFORMED ANALYTICAL GATE**.

## 1. Result, scope and evidence identity

**Recommend owner-native retained input provenance with fresh operation authorization for A, and a Procedure-issued current-turn basis plus Actor-native shared progress and causal normalization/spend closure for B. Neither bridge presently has a demonstrated deployed positive issuer.** These are separately dispositioned recommendations, not accepted architecture, SP03 output, Stop2, or implementation GO.

- Local HEAD and successfully refreshed `origin/v1/engine-rearchitecture`: `39ab1b4a1c7a844f4df2e7886c4b2ac17e401243` (`git fetch --prune origin` succeeded).
- `git diff afca759c38480f0e4a5629236b08c9d401ecd10d HEAD --name-only` found cursor/allocation/SP00 qualification changes; no GAME or owning bridge semantic/process changes. Actual primary reads below are checkout bytes at 39ab, not inherited claims from afca.
- First read: coordinator-retained `DEV/docs/superpowers/design/2026-10-13-sp03-auth-turn-bridges-task-brief.md`, **untracked at this HEAD**. It records independent Senior Stop1 GO `ses_ec97befd4ffeCwmiiZnavkhK4O` with binding additions. Its ruling is supplied by that retained assignment; no independently obtained Senior transcript is claimed.
- Original external scope is a locator only. The [source ledger](2026-10-13-sp03-auth-turn-step2-source-ledger.md) and [case ledger](2026-10-13-sp03-auth-turn-step2-case-ledger.md) accompanying this report identify actual inspected sources and claim depth; [verification receipt](2026-10-13-sp03-auth-turn-step2-verification.md).
- Only task-owned external Markdown outputs were created. No repository/source/cursor/index writes, commits, pushes, agents, production tests or runtime activation.
- Skills: brainstorming (architectural path adapted to accepted Step1/Step2 authorization), Clean Architecture, SOTA Python (bounded carrier/trust-boundary source inspection; typing rule §2/§4/§5). No tooling replacement or general Python audit. Current official OpenAI route used only for the exact host capability question (§4).

Checklist completed within the authorized slice: context/source selection; scoped primary extraction; two alternatives/recommendations; owner/carrier/producer/consumer/recovery mapping; case accounting; analytical challenge; explicit proof limitations. Later candidate, independent critic, canonicalization and implementation are separate process units.

## 2. Findings that constrain both drafts

**FACT F01 — Identity mismatch spans owners.** `recovery_roots.validate_unresolved_input_owner:582–588`, `durability.RoutedSerializedOperation:347–355` and `_handoff_owner_id:626–631` use input-message ID for Interaction identity. `native_storage.native_identity_from_record:139–159` and `collaboration._load_interaction:1629–1642` instead resolve an Interaction's own `id`/`interaction_id`. Existing collaboration fixture `test_rd12_collaboration:1214–1224` expressly has different Interaction/message IDs. A schema-only no-Player patch would leave incompatible promised roots/routes.

**FACT F02 — Structural auth is not origin.** `VerifiedPrincipal`/`resolve_principal` accept structural values, including a mapping/default `verified=True`. `resolve_player` validates bounded candidate bodies; it does not authenticate the upstream external request. `authorize_operation(gameplay)` checks active membership, not cast-specific PC control. Current publication transport resolves the acting publisher. None of those proves the historical author of a particular accepted invocation.

**FACT F03 — Current read footprint is closed.** Host root preparation reads command/root Resolution/derived roles; independently `activity_contracts:587–591` requires exactly that union. Both reject non-null Procedure (`runtime_host:1933`, `activity_contracts:667`). `spell_cast:213–234` requires the same union plus complete Effect/Asset coverage. No unchecked infrastructure extras or fake selector roles may be appended.

**FACT F04 — Procedure has distinct concrete and generic contracts.** Concrete combat uses schema2, `procedure.combat_minimal`, phase/initiative/exact budget keys/capacity/spent. Generic Procedure lacks this grammar. Seven concrete transitions are owner-declared; DEV producer validates permutation, range and budgets but emits `event.procedure.state_changed`, not current-turn issuance. The separate `advance_combat_turn` helper has different cursor behavior and cannot define a combined lifecycle.

**FACT F05 — Progress validates shape, not cause.** Actor `spell_progress` admits definition-keyed `lifecycle.progress.turn_gate` with `turn_occurrence_key`/`consumed`. It has no current closed cause/definition issuance contract. `actor_continuity._spell_progress` validates fields. `temporal.evaluate_temporal_binding` consumes boundary status; it does not issue a turn.

**CONSTRAINT F06 — Sufficient evidence survives; handles need not.** Step5.2 laws5/6/12, Step5.4 law13, Step5.7 law13, WP14 laws8/10, Step5.11 laws3/4/10/12/15 and Step5.13 laws36–41 distinguish disposable derived handles, retained native meaning/provenance, exact prose and resolvable references. Existing `runtime.message` is lawful. Neither permanent full text, a new history family, nor persisted BoundaryOccurrence follows.

**CONSTRAINT F07 — Protection precedes dependency escape.** Step5.14 law2 requires durable cleanup-visible protection before/with externally writable dependence, unless admitted self-containment/fencing already prevents loss. Same-domain publication may replace/remove atomically. Cross-domain survivor is confirmed first; release can lag. Missing complete negative proof means retain.

**CONSTRAINT F08 — Technical movement is not gameplay.** Save/restart/absorption/unrelated revision cannot create a new turn, original input, voluntary agency or RNG experiment. Recovery preserves historical inputs while re-resolving current mutable owner/control routes. Accepted remote/native success survives later local or publication failure.

## 3. Draft A — original input basis and operation authority

### A recommendation and alternatives

**A-R1: embed a closed accepted-input provenance basis in Interaction; retain communication content/compact provenance in runtime.message; derive an operation-local proof through the trusted RuntimeHost composition.** Use existing owners/direct routes. Confidence HIGH for ownership/retention requirements; MEDIUM for concrete representation pending candidate review; deployed issuer **NOT_ESTABLISHED**.

| Alternative | Disposition and reason |
|---|---|
| Retained Interaction basis + message + fresh current authority | RECOMMENDED. One accepted-input owner, no credential persistence, bounded direct chain; requires coordinated schema/routing/producer/protection changes. |
| Existing message carries the entire origin basis; Interaction only references it | LAWFUL alternative, not rejected on ownership grounds. More required message dereferences/retirement coupling; useful if supported adapter already establishes communication provenance there. No actual such issuer found in inspected composition. Choose this instead if that evidence appears. |
| Transient-only handle / cached current publisher / strings or hash | REJECTED. Cannot reconstruct historical origin after handle loss; equality does not authenticate. |
| Separate authorization ledger/history registry or permanent whole input archive | REJECTED as unnecessary. Existing owners satisfy responsibility; grows privacy/storage/cleanup obligations without a demonstrated need. |
| Defer positive original-author proof and keep read-only holds | REQUIRED fallback while indispensable issuer evidence is unavailable; does not block unrelated SP03 conformance. |

### A minimum representation (proposed, not today's schema)

Interaction owns stable identity in its native envelope: `(kind=runtime.interaction, id=I)`, campaign/session associations, `input_message_id=M`, `intent_plan_id=P`. **I is not M.** Do not add a second independently writable identity; any serialized association must equal the envelope.

Proposed closed embedded `accepted_input_basis` contains:

1. explicit basis-contract generation and admitted deployment adapter/profile identity;
2. repository/campaign scope, accepted session association and Interaction/input-message identities;
3. accepted host invocation identity and, only where needed for exact retry/edit/branch distinction, owner-qualified host item/revision/lineage discriminator;
4. provider `github`, stable authenticated account ID and login-at-acceptance; no access token/session secret;
5. accepted representation kind + typed content-digest contract/identity (text exact relative to accepted representation, not undocumented UI bytes);
6. historical authorization variant: `multiplayer` with accepted Player identity and exact accepted authority/control basis, or `creator_singleplayer` with native first-initialization provenance association + authenticated accepted login; no fake Player/sentinel;
7. stable accepted semantic interpretation/provenance dependencies needed by command/continuation/collaboration, and the owner-qualified acceptance evidence that makes the above historical rather than a caller assertion.

These are necessary semantic fields, not a demand to duplicate every value already unambiguously fixed by the native envelope/enclosing generation. Candidate formalization should remove redundant projections, fixing equality for any retained projection. A typed historical authority witness may keep only the validated relation and its establishing native evidence, not whole Player/Actor snapshots. Its accepted material meaning remains immutable when the Player later changes.

Message M keeps its own envelope ID, `interaction_id=I`, inbound direction, accepted representation/digest, exact content while required and compact participant/source provenance thereafter. A's compact message may reference the Interaction basis rather than copy all auth fields. Current schema's unconditional `recipient_player_id` is outbound-oriented: draft a direction-qualified participant/recipient contract, allowing creator-only inbound communication without manufacturing Player. No `details` escape. Outbound EMISSION_COMMIT/disclosure remains its existing owner; inbound evidence never fabricates delivery or knowledge.

### A issuer, exact checks and current authority

Trusted deployment adapter supplies the external-origin observation to deterministic acceptance at the host boundary. Model/domain callers supply requested intent, not adapter objects, principal verdicts or trusted origin mappings. Composition binds the adapter to the selected repository/campaign; no public transport override. Existing TCB rules apply; no arbitrary-Python token/weak-registry authentication scheme is proposed.

Before initial protected acceptance, validate a finite chain:

`native I + accepted M + P + exactly one clause C -> command K -> root Resolution R`.

Check envelope/state kind/ID/campaign equality; accepted campaign/session/input/invocation/account agreement; I↔M and I↔P; K.interaction/plan/clause; unique matching clause, populated C.command_id=K; R root/initiating-command and admitted compiled request/context. The acceptance producer, not text, fixes the binding. Root footprint includes only owner-required infrastructure refs and bounded account-route evidence; compiler/gameplay selectors do not gain auth owner reads.

Multiplayer initial authority: authenticated account -> current owner-proven complete `PrincipalPlayerRoute` -> exact reload of every nominated candidate -> one active Player -> Player envelope/state equality -> intentional principal in current `controlled_pc_ids` -> operation-specific authority. Loading only I.player_id proves neither uniqueness nor freshness. The current route constructor's complete flag is not an external-origin guarantee; host must obtain its owner-valid completeness basis and currentness.

Creator singleplayer: current authenticated login must equal owner-issued native first campaign-initialization author login. Stable account ID does not replace this rule. Keep the existing no-Player branch and accepted rename read-only outcome. A recovered input remembers accepted creator provenance; it does not turn that past authority into permission for a new write today.

| Operation | Historical basis / current boundary |
|---|---|
| New intentional input | Fresh adapter-authenticated input + fresh current authority. Later identical prose is new I. |
| Exact transport retry/duplicate | Lookup accepted I/K/resume identity first; compare fixed basis/fingerprint; return existing outcome/suspension, never reexecute. Access/disclosure to return material is checked currently. No blanket old-author/current-controller equality requirement. |
| Cold read-only inspection | Reconstruct historical basis from retained owners; current read/recipient eligibility. No write permission inferred. |
| Continue automatic mandatory accepted work | Preserve original cause; follow native execution/current operation authorization and routing. An executor is not necessarily the old author. Mere current publication permission does not permit arbitrary continuation. No new delegation policy invented. |
| Continue with new voluntary protected mutation | Authenticate the present input and current controlled subject/purpose. If no existing native mapping authorizes that continuation, hold; do not relabel a different actor's new intent as old input. |
| Fresh Choice/Reaction response | Authenticate responder input; exact current Continuation generation/offer/responder/option or Activity; current responder control; single-consume. It may be another player from the root author. Extra intent follows Step3 §13, not silently the reaction child. |
| Controller change during open work | Keep accepted actions/provenance; reacquire current control for new agency. WP17 obsolete/successor collection requirements where applicable; no synthesized consent or transfer action. |

A does not define an unrestricted executor/delegation service. Automatic accepted descendants and new voluntary inputs are distinguished by Step3/WP16/WP17, not a proposed universal ACL.

### A recovery, retention and exact carrier reconciliation

| Owner/carrier | Producer | Reader/consumer | Recovery/protection/discharge |
|---|---|---|---|
| Interaction accepted basis and stable I | trusted adapter + deterministic Interaction acceptance | command binder, host auth join, retry, collaboration | known-I native route; promised unresolved I independently rooted only on actual durability/handoff promise; retained while command/consumer needs origin |
| Message M / compact provenance / required exact slices | accepted communication producer | interpreter, exact-text consumers, bounded history | known-M route from I; exact retained only until content sufficient or natural exact owner promotion; no universal immediate publication |
| Plan/clause normalized accepted meaning | Interpreter + deterministic acceptance | command, WP17 collection/handoff | direct P from I; immutable material interpretation while referenced; correction is new accepted input |
| Command/Continuation fixed source links | execution acceptance/segment owner | retry/resume/native producer | no replay; existing command roots/Continuation references protect exact closure |
| Current account route/Player/control | campaign access owners | operation-specific auth join | reacquire pinned campaign authority, bounded complete route + exact bodies; not historical permission lease |
| Creator history witness | HistoryService/native initialization-history producer | creator-only current auth | reissue from authenticated native history when needed; cache only immutable provenance; current login always distinct |

Later coordinated realization must reconcile `recovery_roots`, durability routing/handoff identities, native-storage envelope validation, collaboration loaders, publication/root companions, recovery hydration and tests **as one identity closure**. Keep MP-only collection obligations MP-only; a no-Player Interaction is not a fake collaboration contributor. `_validate_recovered_root_closures:858–897` currently validates execution/catalog, not the new origin/message/control closure; extend owner-routed hydration and final operation checks, not a permissive callback.

Promised pre-command input: actual Step5.4 handoff/Step5.5 SAVE or admitted independently durable collection reliance determines survival. Do not enroll every arriving message. If meaning is incomplete, required exact input content and provenance enter that promise. An abandoned unaccepted draft is not durable history. Unexpected loss before an applicable successful durability promise can lose SOFT input; no reconstructed text/choices from hash or host memory.

Message compaction retains origin attribution/digest plus independently sufficient accepted semantics. Envelope removal requires explicit provenance-only or survivor-backed reference semantics and idempotency discharge. Legacy raw refs remain resolvable by default. A cross-source command/consumer either has all sufficient basis self-contained or has cleanup-visible typed protection before its acceptance; eventual registration is invalid.

## 4. Exact supported-host capability evidence

Accepted deployment is R2.6 §1/§8: ChatGPT Plus ordinary Project-capable one-chat-per-human, deterministic core + fixed GitHub Connector. WP16 law1 specifies connected Connector current stable GitHub ID separate from login; Step5.6 laws2/30 require authenticated acting/delegated principal. September21 composition §2/§3/§9 places authenticated adapters in the TCB and final product wiring in Wave05. PCR amendment proves a particular ref capability shape, **not message origin**.

Inspected implementation evidence: RuntimeHost checks repository/history operations and optional publication operations; publication protocol's `resolve_authenticated_acting_principal` explicitly concerns publication. Bootstrap composes supplied ports. History requires `read_authenticated_commit_author` for creator provenance. None of these inspected interfaces supplies an accepted connected participant-input/invocation/revision observation. Fixtures are legal trusted composition but prove only deterministic contract behavior. `turn_runtime.start_turn` is control-only, not an identity issuer.

Cheap official check: `webfetch https://help.openai.com/en/articles/11145903-connecting-github-to-chatgpt` returned **HTTP403** on 2026-10-13. No page content or current vendor feature claim was obtained. No alternate host/MCP/API MVP was built. This is failed documentation retrieval, not proof the selected product lacks the capability.

**Actual deployed original-issuer proof: UNAVAILABLE in this OpenCode surface.** Required bounded next evidence is a supported connected deployment observation showing (a) trustworthy participant principal bound to the exact input, (b) stable external acceptance/retry/revision discriminator or an already admitted equivalent that distinguishes retries from new identical intent, (c) loss/restart reconstruction mapping, (d) no caller/model override. Current-principal lookup detached from message acceptance is insufficient. An HDM-issued key can support retry only when the host reliably resubmits/binds it; generating random keys per invocation does not prove retry identity.

Contract design may be reviewed with this positive deployment gate retained. Claiming supported secure deployed casting or exact retry coverage cannot pass until evidence closes it. If real host evidence proves impossibility, Step5.14 law5 requires profile restriction/refinement or explicit affected architecture reopening; do not silently weaken input authentication. A privacy/availability/trust trade-off involving a new service or weaker assurance would be human-owned; none is proposed here.

## 5. Draft B — common definition, Procedure occurrence and Actor progress

### B recommendation and alternatives

**B-R1: one immutable compiler-admitted common gate descriptor, one Procedure-native current-turn establishing basis, existing Actor progress value, and compact owner-native causal evidence. Normalize the exact subject lazily at a lawful native edge; SP03 only observes an already coherent result.** Confidence HIGH for owner allocation/causal laws, MEDIUM for representation. Actual GAME turn issuance/reset/slot establishment **NOT_ESTABLISHED**.

| Alternative | Disposition and trade-off |
|---|---|
| Exact-subject lazy native normalization + atomic consume | RECOMMENDED. Avoids resetting every Actor on every turn; no scan, same shared gate. Missing/stale progress holds the reader until genuine native normalization. New subject admission must prove no earlier same-turn consumption can be hidden. |
| Eager reset of the finite complete owner-enrolled caster set at each actual turn-start | LAWFUL alternative. Simple read state; exact enrollment/closure potentially greater write fanout and cross-source cost. Cannot assume all Actors/participants; exact enrollment must include relevant non-active reacting casters. Choose if actual bounded fanout/native evidence makes it simpler. |
| `(round,index)` / Procedure revision / restart-derived key with implicit unused default | REJECTED. Equal timing can recur, unrelated mutation is not a turn, missing cause/progress grants no permission. |
| Generic Procedure gate or cast-history authority | REJECTED. Relocates native Actor progress/duplicates source-dependent gate; history is evidence only. |
| Defer positive gate read until native proof exists | REQUIRED current fallback. Read-only Procedure/budget negatives can proceed independently; no reversed SP03→SP04 prerequisite. |

### B exact immutable definition and subject

Proposed descriptor has a stable common definition key (spelling to be assigned by the final admitted owner), explicit generation, `profile=lifecycle.progress.turn_gate`, `owner=world.actor`, `subject=rule-defined caster`, one slot-spend-to-cast gate across all source/mode consumers, actual-turn provider/boundary, and closed initialization/reset/consume/nonconsume rules. The compiler retains the exact descriptor/definition identity and consumer bindings in admitted frozen bytes. A profile name is not this definition, and no new generic catalog kind/primitive is inferred merely to house it.

Ordinary source witness proves principal=physical=source=origin; that Actor carries the gate. A split principal/body/payer needs the exact admitted source's subject binding and one stable gate owner; this draft does not infer all roles equal, transfer gate to a cost payer or grant a second body gate. Unsupported/unproved split binding is held. Source-specific action/reaction/resource costs remain their respective owners.

### B Procedure occurrence representation and seven transition dispositions

Recommend a **compact current-turn basis embedded in concrete Procedure-native state/evidence**, not a persisted BoundaryOccurrence record. Required semantics: Procedure stable identity/lifecycle, admitted boundary producer/profile/generation, exact active participant, stable establishing execution segment + local boundary declaration, and sufficient accepted start-turn cause/phase evidence. An occurrence key is an injectively framed derivation of `(Procedure identity, accepted start-turn segment identity, local boundary key)`; exact wire encoding is candidate work. Existing stable segment sequence is owner-local, not Procedure revision. Lifecycle validation must prove a segment cannot establish two turns under that key and a transport retry returns the same accepted edge.

| Transition | Occurrence/gate consequence |
|---|---|
| initialize | Opens Procedure between turns; establishes lifecycle/initiative, **no active turn merely from round1/index0**. |
| start_turn | From exact ACTIVE/between_turns/no pending round, valid participant; accepted causal segment establishes one new actual turn and immutable current-turn basis. |
| spend_action | Mutates action budget under that current turn; retains turn occurrence. |
| spend_movement | Mutates movement budget under that current turn; retains turn occurrence. |
| end_turn | Closes that active turn; no slot permission in between-turns; next index alone is not a new occurrence. |
| advance_round | Changes cursor/round between turns; no active turn until accepted start_turn. |
| terminate | Native terminality; no new occurrence/reset/slot permission; preserve protected accepted dependencies. |

Current DEV request/result grammar replaces one Procedure state and records after digest/revisions; it does not already carry this causal basis. Future realization may extend those exact producer/projection contracts coherently; DEV transition execution alone cannot impersonate GAME acceptance. Do not combine the convenience `advance_combat_turn` helper with seven-transition semantics.

Other creature's turn: Procedure active participant is that creature, while caster subject may differ for an admitted reaction. Do not require active participant=caster for every cast. The common slot gate is keyed to **that actual current turn**, not the caster's next/last turn. Between turns/terminal/noncombat without an exact admitted provider is held; source-defined noncombat providers are outside this concrete draft and cannot be invented from host messages.

### B native progress, causal companion and normalization

Keep existing Actor value unchanged: `spell_progress[common_key] = {profile_id, turn_occurrence_key, consumed}`. Missing is missing, not false. To avoid changing the shared exact turn-gate value or requiring full old events forever, recommend a **closed Actor-native evidence companion keyed by that same definition** (proposed `spell_progress_basis`, spelling unaccepted). It carries compact immutable evidence for the last establishing transition, not another counter/current-state owner:

- common definition identity/generation and actual bound subject;
- current turn's establishing Procedure/boundary/accepted segment/local key and retained sufficient producer/cause meaning;
- Actor transition identity and lawful branch `INITIALIZE | RESET | CONSUME`;
- predecessor progress/transition identity where required to prove lawful replacement and avoid double reset;
- for CONSUME only: exact accepted cast execution/segment/consumer and actual resource-expenditure owner/definition/cause, including source-defined cost boundary (not only a receipt name);
- compact accepted-result linkage adequate for retry/native validation; detailed event refs are resolvable only while required or replaced by sufficient compact evidence.

When a gate is consumed, retain the sufficient **current-turn INITIALIZE/RESET basis as well as the CONSUME basis**. A consume's bare predecessor ID must not force an unbounded chain back through older receipts. Compact the current-turn establishment and expenditure evidence into the same native companion (or their bounded protected existing references); older-turn detail can discharge only after all open/idempotency/causal consumers retain sufficient survivors. A combined normalize+consume segment records both logical causes under its one actual accepted edge, not an invented intermediate receipt.

The companion is checked **against** native progress/accepted closure; it cannot independently say spent/unused or initialize/reset it. Unknown/unadmitted companion rejects. If an existing accepted event/receipt route supplies bounded protected sufficient evidence more simply, prefer a direct typed reference instead of the companion. Either choice requires source-owned producer/recovery/retention proof; today's arbitrary string ref is not enough.

Lazy native rules:

1. **Same actual turn + consumed=false**: consume only with one real accepted slot expenditure to cast; couple gate/resource/causal/execution/receipt closure at one lawful segment.
2. **Same turn + consumed=true**: another slot expenditure through any source rejects; exact accepted retry returns the same result, not a second consume.
3. **Old proved turn**: owner validates accepted new actual turn cause and exact predecessor. Reset/normalize this subject through native establishment (possibly in the same complete consume segment). A reader never silently rewrites or interprets old consumed state as false.
4. **Missing progress**: initial admission requires source-owned lifecycle evidence proving a lawful first-use origin and that no earlier same-turn expenditure can be concealed by re-enrollment. Then an explicit native INITIALIZE edge creates progress/evidence. Missing basis or unknown prior lifetime holds; do not initialize from absence alone.
5. **No-slot branch**: slotless/ritual/countered/interrupted-without-slot leaves gate unconsumed. Long cast preparation/start/repeated action is not slot consumption; actual lawful accepted slot boundary consumes. Invalid-target spend follows its exact source cost branch, not blanket refund.

SP03 may return observed current unused/consumed only after genuine owner-native initialization/reset evidence. A preparation fragment predicting legal normalization is not a positive current permission or a receipt. These later writer obligations are separate from SP03 read proof.

### B owner/producer/reader/recovery mapping

| Owner/carrier | Producer | Reader/consumer | Recovery/retention |
|---|---|---|---|
| common immutable gate descriptor | admitted source/compiler contract | cast consumer + native validator | exact compatible frozen definition/context recovered; unknown definition held |
| Procedure current-turn establishing basis | registered Procedure start-turn native transition | turn resolver, temporal consumers, gate validator | active Procedure root; accepted segment/local basis directly reachable; transient BoundaryOccurrence reconstructed |
| Actor common progress + compact causal companion | exact native progress producer within segment | SP03 gate observation; later cost producer | subject direct route/protected open command; no full cast history; companion/progress/cost cannot split durable closure |
| accepted resource expenditure | owning Actor/Asset/Procedure resource + cast segment | same gate validation/retry | same lawful native closure, stable IDs/RNG/receipt retained |
| enrollment/protection | forward native consumer + bounded derivative route | normalization discovery, recovery, cleanup | exact subject/definition/provider edges, no campaign Actor scan; enrollment changes with movement/lifecycle |

Lazy normalization needs only requested subjects, not eager all-Actor reset. Armed independently-due obligations, if any exact admitted reset mechanic has them, still obey mandatory temporal enrollment; this gate cannot use lazy reachability to waive Step5.2 law13. Provider movement preserves occurrence identity and exact current owner basis; it does not reset. Termination/new Procedure cannot reuse old key merely because numeric cursor matches. A transferred/split subject retains exactly one lawful gate or holds until exact native policy is proven.

HOT: complete inseparable progress/resource/Procedure-cause/runtime/receipt/dirty closure at the admitted native segment fence. LIVE: exact source CAS establishes shared state; SQLite only adopts confirmed acceptance. Procedure and Actor/resource on different writable sources need admitted closure/freeze/forward movement before coupled mutation; no distributed transaction or independent half-spend. Current `hot_store._establish_actor_owner` is Actor-phase admission, not this mechanical kernel. Current recovery/root handoff helpers preserve routing identity but do not automatically hydrate the new cause/retention closure.

## 6. Protection and race obligations common to A/B

| Race/failure | Required deterministic disposition |
|---|---|
| Consumer acceptance vs message payload compaction | Same-domain complete closure or prior exact protection/self-contained sufficient semantics; stale negative index cannot delete. |
| Cross-source new command vs origin/message envelope retirement | Before/with accepted dependence, target-cleanup-visible registration or admitted fence/self-containment; otherwise retain/hold. |
| Turn starts while cast is preparing | Revalidate exact Procedure occurrence/Actor/cost read union; stale prospective work rejected/recomputed at safe native boundary. |
| Two source casts compete for one caster gate | One owner/currentness fence establishes one consume; loser observes consumed or its exact stored retry; no merge of booleans. |
| Crash before vs after reset/spend | Before acceptance none; after accepted coupled state resume same segment/cause; no free gate or duplicated cost. |
| Cause detail compaction vs LIVE movement/absorption | Confirm sufficient compact native survivor/protection before loss; continuous bounded routes and same IDs; source movement invalidates stale assessment. |
| Player/control revocation vs protected mutation | Fresh campaign-domain authorization plus WP16 close/no-window transition when affected LIVE authority changes; CAS alone cannot legalize stale permission. |
| Publication success then local handle/adoption loss | Recover current accepted native closure; reissue handles; do not replay. |
| Partial multi-source close or publication ambiguity | Preserve actual accepted technical edges; dependent semantic bridge held until exact final composition proved. |

## 7. Minimum future impact and version assessment

This is a design impact forecast, **not an implementation Envelope or permission**.

A affected owner/consumer set: Interaction/message/Intent/clause/command links; RuntimeHost composition/input acceptance/read footprint; current account/Player/creator checks; recovery_roots/durability route/handoff/recovery hydration; collaboration historical vs current paths; native storage identity/projection validation; message/retention/cleanup/history consumers and direction-specific emission qualification.

B affected set: immutable common gate definition/compiler bindings; concrete Procedure state/transition/event/receipt cause projection; Actor progress evidence; native gate/cost producer; host/contracts/membership/current-owner union and cache identity; temporal/provider/root/enrollment/protection/recovery; HOT/LIVE/dirty/publication closure; domain conformance and actual GAME producer proofs.

Every new field/read expansion propagates to exact issuer + independent validator + source membership union + recovery/protection + tests. No selector-read permissions, broader roles, model/network pass, history census or source-quality weakening follows.

**VERSION_IMPACT: NONE for this external-only research delta.** No current HDM namespace owner/projection changed. Future material runtime modules require one owner-local revision bump each; new contract carriers need explicit schema/generation classification; incompatible required identity/direction/Procedure/Actor changes require their owning schema assessment and synchronized consumers/projections. Changing accepted command fingerprint participating provenance requires digest generation assessment (current2), not silently same-generation hashes. Shared generic progress need not bump merely because a separate companion is proposed, but affected owner/protocol shapes must be classified. Released breaking persisted semantics require local schema + campaign generation/migration closure; clean-slate removes pre-release compatibility shims, **not version discipline or accepted-work provenance**. Catalog/compiler/profile/package generations are assessed under actual incompatible/compatible change, not automatically globally bumped.

**SYSTEM_IMPACT: ARCHITECTURE_REVIEW_REQUIRED on both bridge edges remains.** No boundary crossed by this report.

## 8. Analytical quality gate (DEV/DESIGN_PROCESS §12)

1. **Strongest opposing case.** A adds persisted origin assertions but cannot demonstrate the external issuer; these may become elaborate security theatre. Mitigation is separate actual adapter acceptance proof and fail-closed positive gate. B companion duplicates causal detail and lazy normalization adds a writer requirement at first-use; an already protected native receipt plus finite eager enrolled reset might be simpler. Prefer existing sufficient evidence when observed; do not canonize speculative companion syntax.
2. **Simplest viable comparison.** Existing Interaction + runtime.message + closed historical basis + fresh access chain is sufficient, without auth/history registry or full text archive. Existing Actor gate + Procedure-native start cause + smallest retained causal witness suffices, without cast-history truth/all-Actor reset. Structure is only justified where exact recovery/native validation needs it. Ref-only is simpler only with bounded guaranteed surviving source; hash-only is not sufficient.
3. **Assumption attack.** H-A1 host binds participant to exact invocation (UNVERIFIED; false => positive A unsupported/reopen profile). H-A2 host preserves retry distinction after restart (UNVERIFIED; false => cannot promise exact duplicate recognition by prose). H-B1 immutable gate subject is admitted for actual split consumer (conditional; false => split positive held, ordinary case unaffected). H-B2 compact witness is sufficient for every enrolled causal consumer (candidate validation required; false => keep fuller source/protection). H-B3 requested subject's first-use admission proves no erased earlier spend (required technical proof; false => hold, never initialize from absence).
4. **Counterexamples.** Different current publisher with same K; two Player bindings; creator rename; new controller answers an old offer; message compacted before typed meaning; I≠M cold root; same round/index in new Procedure; another creature's turn reaction; lazy init after prior consume erased; repeated reset retry; cast/turn race; second source cost on another LIVE authority; compacted cause during movement. All are individually mapped in case ledger with held or native proof disposition, not asserted tests PASS.
5. **Local/global check.** A cannot fix schema while stranding durability/collaboration identities. B cannot make read evaluator elegant by moving progress into Procedure or treating every new source revision as a new turn. Both require coordinated finite infrastructure footprints; broad Context/control/state authority and generic GC/platform work are avoided.
6. **Best-practice applicability.** Python frozen DTO/Protocol supports an immutable local carrier but authenticates nothing by itself; runtime-checkable method presence is not external provenance. Clean Architecture composition isolates host transport from mechanics, not substitute ownership or require new interfaces gratuitously. No unsupported external pattern/vendor feature drives the draft.
7. **Reversibility.** Keep exact shared progress value and existing record families. Before release, replacement shapes are reversible under clean-slate; accepted inputs/causes still cannot be fabricated. New deployed trust boundary/security weakening or material additional ordinary round-trip cannot be smuggled into representation choices.
8. **Falsifiability.** Change A recommendation if actual supported adapter already owns a sufficient message-native origin carrier; restrict/reopen if actual host cannot bind participant/retry. Change B representation if existing owner-valid receipts provide sufficient bounded survivors with less metadata, or finite eager enrollment demonstrably reduces complexity without material cost. Lifecycle-proven derivation from existing state would remove new turn metadata only if it proves stable causal uniqueness across the entire lifecycle; current cursor/revision evidence does not.

## 9. Completeness, residual proofs and next process unit

- Applicable primary-law/source extraction and all Task Brief cases are accounted for in supporting ledgers. Coverage means **required disposition/proof mapping**, not executed behavior or production closure. No whole-repository audit, full WP case-suite coverage or deployment support claim.
- Remaining proofs: actual connected input/principal/invocation/retry issuer (A); genuine native Procedure start-turn/initialization/reset/slot causal establishment and compact-survivor tests (B); future candidate's exact footprint/schema/enrollment/retention realization. These are agent/deployment technical evidence, not human proofreading.
- **Human decision required: NO established for the owner-conforming drafts.** Accepted security/creator/agency/slot/retention laws settle the semantics. Missing deployed proof is a capability/acceptance gate, not a question whether the human wants security. **YES only if** actual evidence forces a new trust/delegation/host profile, weaker guarantee, externally meaningful compatibility change or material latency/availability/privacy trade-off; supply a separately decision-ready choice then.
- Analytical gate completed as a distinct self-challenge. **Positive deployment completeness remains HELD**, explicitly rather than PASS. Source-sensitive technical draft can proceed to Step3 with that hold visible; no claim that the selected deployed adapter works.
- Next exact process unit: coordinator reviews this frozen Step2 package, then produces **separate Step3 Decision Brief dispositions A/B** and recorded Step4 HumanDecision YES/NO. If no new human trade-off, continue technical design; obtain indispensable host evidence before any affected deployed positive claim. Then Step5 candidate -> independent fresh-context whole-project Step6 critic -> Step7 resolution/propagation -> Step8 owner synchronization/verification/publication/read-back -> independent Senior Stop2. Only afterward reconcile implementation Envelope/plan and obtain Senior implementation GO.
- This worker stops at its assigned Step2 boundary. Main retained brief, sources and cursors remain coordinator-owned.
