# Story Baseline Projection Source Contracts

Status: **FINAL IMPLEMENTATION-FACING SOURCE-CONTRACT REGISTRATIONS — IMPLEMENTATION NOT ACTIVATED**

Date: 2026-09-08

Companion to [Story producer, persistence and retrospective consumer contract](2026-09-07-story-producer-persistence-retrospective-consumer-contract.md), especially §§11–17, 25 and 29. That contract owns serialization, validation/publication, correction, availability and consumer acquisition. This document supplies its closed production candidate, enumeration and materialization policies. It introduces no history owner, campaign registry, scheduler, global cursor or additional Story layer.

**Current PO-009 amendment.** `2026-09-09-story-commentator-self-contained-corpus-owner-decision.md` supplements and narrowly supersedes the earlier baseline Commentator fallback allowance. For the **baseline Commentator**, every WP-19-required retained material T0 decision-basis factor must be recoverable from a **Story-local** source-bound representation; a native-only pointer no longer discharges that promised consumer support. Native SemanticEvent/history owners remain authoritative, hidden reasoning/chain-of-thought remains excluded, and ordinary Master/diagnostic/deep-source native capabilities remain intact. The exact persisted Story fields and self-contained Commentator eligibility/control-projection representation remain downstream realization decisions and are not claimed as implemented here.

## 1. Product responsibility and exact scope

Story is a durable, navigable campaign corpus for Commentator retelling and eligible Master retrospective use across chats. Preserving the full accepted semantic story is useful; corpus size alone is not a reason to discard established events. Bounded retrieval limits one operation/context, not the length of the retained campaign corpus.

The baseline therefore preserves **every admitted nontechnical SemanticEvent and every admitted historical relation** in both EVENTS and NARRATIVE, with different presentation granularity. MECHANICS preserves the explicitly selected committed gameplay facts and resolved outcomes in §6. Selection is not a model's importance score. Native owners already decide what becomes accepted history or mechanics; Chronicler cannot apply a second discretionary materiality threshold to the required set.

TRANSCRIPT retains the existing Selective Exact boundary: ordinary accepted participant messages are eligible for archival, while an accepted exact-archival commitment requires the specified representation. An empty TRANSCRIPT without such commitments is permitted by Step 5.11. It does not license empty EVENTS/NARRATIVE over accepted gameplay history. Exact speech, host text, semantic communication occurrence and objective truth remain different evidence claims.

Preserving source-bound meaning does not require duplicating full native records, every Resolver trace, every state snapshot, superseded literary versions or unrelated personal/OOC text. Additional eligible participant prose may be retained; there is no corpus-wide size quota or requirement to minimize Story record count. No mandatory per-turn generation, new serial gameplay call, cross-chat host-memory authority or whole-history preload is introduced.

### 1.1 Owning-source reconciliation

| Owner inspected | Binding consequence here |
|---|---|
| [Step 4](2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md), §§10.5, 12–22 | Four layers; accepted evidence; one message/utterance per Transcript unit by default; human-meaningful Event/Mechanics beats; literary NARRATIVE; provenance and whole-unit availability |
| [Step 5.10](2026-08-21-step-5-10-story-projection-durability-canonical-spec.md), §§5–8, 22–29 | Domain-local enumeration, generation-typed terminal coverage, explicit cardinality, no late insertion, no required skip ledger; catch-up may lag |
| [Step 5.11](2026-08-21-step-5-11-transcript-history-retention-compaction-canonical-spec.md), §§4–16, 19–25 | Stable message identity after compaction; selective exactness; ordinary Transcript omission; exact-archival obligations; minimum IC/OOC scope; semantic-content discharge |
| [Step 5.12](2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md), §§4, 6, 8–14 | Outbound admission at EMISSION_COMMIT; no literal-read/rendering claim; re-presentation is not a second fictional occurrence; source-native message identity |
| [R2.1](2026-08-24-r2-1-continuity-history-canonical-spec.md), §§2–9 | Cross-chat continuity remains source-bound; Story is optional/lagging orientation; native escalation; source correction; no universal memory owner or exact archive |
| [WP-10](2026-09-01-r2-7-WP-10-durable-campaign-record-family-completeness-canonical-spec.md) | Separate Message/Interaction, SemanticEvent/relation, execution, MechanicalEvent/receipt and Story responsibilities; protocol values do not become new families |
| [Step 3](2026-08-19-step-3-execution-boundary-canonical-spec.md), §§4, 8–10, 22–23 | Segment and immutable receipt identity; committed mechanics; stable child/root linkage; suspended execution is not final outcome |
| [WP-15](2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-canonical-spec.md), §§6–8, 11–12 | Native accepted occurrences; sparse typed relations; late evidence about old anchors; no global fictional order or reconstruction from old Git bytes |
| [WP-18](2026-09-04-r2-7-WP-18-story-continuity-dramaturg-planning-canonical-spec.md), §§1–4, 10–15, and [final amendment](2026-09-04-r2-7-WP-18-final-senior-recovery-canonical-amendment.md) | Layer-local metadata and publication; no Story lock/queue or planning-to-history promotion; remaining runtime realization is not activated |
| [WP-19](2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-canonical-spec.md), §§7, 9–11 | Ordinary Master retrospective; bounded native T0 decision-basis evidence; no T1 substitution or full psychology archive; zero additional serial capture work |
| [PO-009 Commentator self-contained corpus](2026-09-09-story-commentator-self-contained-corpus-owner-decision.md) | Baseline Commentator support must be Story-local for retained WP-19 material T0 factors; self-contained eligibility/control projection is required conceptually; native authority is unchanged and exact machine representation remains deferred |
| [Step 5.13](2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md), §§4, 8, 14–22 | Owner-typed protection, survivor-before-removal, stable enumeration, no historical Git resurrection; Story correctness is independent of gameplay recovery |
| [SemanticEvent schema](../../../../GAME/SCHEMA/event.schema.yaml), [MechanicalEvent schema](../../../SCHEMAS/runtime-mechanical-event-state.schema.json), [receipt schema](../../../SCHEMAS/resolution-receipt.schema.json), [Resolution schema](../../../SCHEMAS/runtime-resolution-state.schema.json), [Dialogue](../../../../GAME/CORE/DIALOGUE.md) | Existing identity/payload evidence; socially consequential meaning is retained natively; exact machine schemas still lack some accepted source-enumeration/T0 realizations and do not yet realize PO-009's Story-local T0/control projection; they are not evidence that those laws are already implemented |

## 2. Closed registrations and source-local codecs

The following eight registrations are the baseline. `S` is a native origin scope defined below. Every row starts at **semantic_contract_generation = 1**. The `source_domain_id` in this document is serialized as `source_domain` in the main contract. No runtime-discovered generic plugin registry or campaign registration record is required: these are fixed engine dispatch cases over existing owners.

| Registration | layer | source_domain_id | Native lane | Candidate |
|---|---|---|---|---|
| T-MSG | TRANSCRIPT | `campaign.participant_messages@S` | `msg` | One admitted participant communication representation |
| T-ARCH | TRANSCRIPT | `campaign.transcript_archival_requests@S` | `arc` | One exact target of an accepted finite archival request |
| E-EVT | EVENTS | `campaign.semantic_events@S` | `evt` | One accepted SemanticEvent |
| E-REL | EVENTS | `campaign.semantic_relations@S` | `rel` | One newly accepted native historical relation assertion |
| M-SEG | MECHANICS | `campaign.mechanical_segments@S` | `seg` | One immutable committed ExecutionSegment receipt closure |
| M-OUT | MECHANICS | `campaign.mechanical_outcomes@S` | `out` | One established terminal invocation/direct-transition outcome receipt |
| N-EVT | NARRATIVE | `campaign.semantic_events@S` | `evt` | The same native event candidate as E-EVT, independently projected |
| N-REL | NARRATIVE | `campaign.semantic_relations@S` | `rel` | The same native relation candidate as E-REL, independently projected |

E-EVT/N-EVT share native enumeration, not Story progress. E-REL/N-REL do likewise. M-SEG and M-OUT are separate because an accepted intermediate fact and a terminal outcome may become available at different times. A terminal miss or failed save cannot disappear merely because no state-changing MechanicalEvent was produced. T-ARCH is separate because a newly accepted request may obligate archival of a message already terminally considered by T-MSG.

### 2.1 Native origin, identity and enrollment

The campaign is already selected by the main contract. Within it, origin is exactly `LOCAL` for the campaign-local native history stream, or `LIVE:<native live epoch id>` for evidence established in an independently writable live origin. `S` is that origin string with each UTF-8 byte outside ASCII letters/digits/`-._~` encoded as `%HH` using uppercase hexadecimal. Decoding must round-trip; no Unicode normalization or case folding is permitted. Absorption into campaign storage preserves the original origin and native identity, rather than re-enrolling the same evidence as LOCAL. The live epoch's ID remains native; Story does not allocate it.

Each lane/origin uses the source family's **append-monotonic enumeration anchor** required by Step 5.10 and, for messages, Step 5.11. An anchor contains the immutable candidate identity and its positive integer admission ordinal. The ordinal is assigned when that lane's source evidence is established under the native acceptance/publication contract, not when a prospective ID is allocated, a host message appears, a model runs or a Story job starts. Within a lane/origin, ordinal assignment and enrollment are coherent with that native source establishment. Unpublished preparation cannot reserve a hole that later acquires meaning behind a published cursor.

The physical realization stores/routes these anchors with the existing native family envelope or native family index. It must not create a second history payload store, Story work queue or global ID reservation publication. A native family index may be derived from surviving native enrollment evidence; an index that carries the only stable enrollment anchor cannot be discarded as wholly rebuildable. Existing campaign/live history routing supplies origin discovery and origin-to-current-source routing. If that routing cannot prove the requested source-scope set complete, return UNKNOWN/defer that completeness claim; do not scan all live/Story records or call an incomplete set caught up.

The six lanes have independent ordinals. There is no comparison across origins or lanes. `world_order.sequence`, wall-clock time, file order, lexical source IDs, Git HEAD and Story ID numbers are not substitutes. A late relation, late terminal outcome or late archival request enters its lane at a fresh ordinal even when it addresses old events, old segments or an old message.

### 2.2 Concrete identity and cursor encoding

`CID(parts)` means a JSON array of the listed strings/integers, serialized without whitespace. Escape quote and backslash as `\"` and `\\`; escape U+0008/0009/000A/000C/000D as `\b`/`\t`/`\n`/`\f`/`\r`; encode other U+0000–001F controls as lowercase `\u00hh`. Do not escape `/` or other valid Unicode characters; reject isolated surrogate code points. Integers use decimal digits without leading zeroes. Decoders reject other spellings for persisted candidate identity. This is a reversible identity tuple, not a digest or new native semantic identifier.

| Lane | candidate_id components | Cursor token |
|---|---|---|
| `msg` | `CID([message_id])` | `msg:<ordinal>` |
| `arc` | `CID([interaction_id, clause_id, target_ordinal])` | `arc:<ordinal>` |
| `evt` | `CID([semantic_event_id])` | `evt:<ordinal>` |
| `rel` | `CID([native_relation_owner_family, native_relation_owner_id, assertion_key])` | `rel:<ordinal>` |
| `seg` | `CID([execution_owner_family, execution_owner_id, segment_sequence])` | `seg:<ordinal>` |
| `out` | `CID([execution_owner_family, execution_owner_id, "terminal"])` | `out:<ordinal>` |

`execution_owner_family` is `runtime.resolution` for an Activity invocation or `runtime.command` for a direct transition. A root action Command's aggregate receipt is not another terminal invocation candidate; its root and child Resolutions supply their own candidates. `assertion_key` is the source owner's stable relation ID or immutable embedded assertion selector, never a Story-created relation identity. Archive `target_ordinal` is the 1-based position in the accepted clause's frozen target list. Message/event IDs and the source-native live identity remain unchanged.

For every lane, `ordinal` is a positive integer encoded as unpadded decimal; comparison parses that integer under the bound lane/origin/generation. Start coverage is `{"kind":"CONTIGUOUS","through":null}`. A non-null cursor is inclusive. There is no baseline SPARSE codec: these particular registrations require monotonic native enrollment. Another source that cannot supply it needs a separately admitted contract, not reinterpretation of these tokens.

The production `SourceWindow.source_basis` has exactly:

```json
{
  "origin": "LOCAL",
  "lane": "evt",
  "upper": "evt:12",
  "enumeration_representation": "native-history-enrollment-representation",
  "owner_contracts": [
    {"family": "runtime.semantic_event", "schema_version": 1}
  ]
}
```

`origin`, `lane`, `upper`, `enumeration_representation` and `owner_contracts` are required. `upper` is a lane cursor or null for an empty lane at this pinned basis. Each `owner_contracts` entry has required `family`, optional `schema_version`, and optional `semantic_generation`; the fields present must be exactly those needed by that actual native codec, with at least one version/generation per entry. A receipt embedded in its owner uses that owner's codec version. Unsupported interpretations fail closed. `enumeration_representation` is the source owner's exact binding to the enrollment/compaction view used; it is not a freshness timestamp or new hash algorithm. The literal representation above is an example placeholder, not a production identity.

The outer SourceWindow already fixes domain/generation; `campaign_pin` supplies the transport basis. Every selected source manifest entry separately binds the exact payload/survivor used. These bindings must jointly establish an unchanged finite native candidate prefix. Compatible append beyond `upper` does not expand the frozen window. Compaction may use a proved equivalent anchor representation; changed identity, selection meaning or required material invalidates the prepared window.

Enumerate `(expected.through, proposed.through]` in ascending lane ordinal, stopping at or before `upper` and the admitted resource bound. Include **every** enrolled candidate in that interval, including MAY_OMIT candidates. No ranking/top-K/recency/scene-finished filter may remove an interior candidate. A native enrollment interval may contain deliberately unused ordinal slots only if the source proves they can never acquire candidates. Tail, absence and interval-completeness proofs use the native lane index/anchors, never an LLM search result. A nonempty selected window and successful required output are necessary for CATCH_UP; an empty lane requires no dummy write.

### 2.3 Common output, proof and minimum manifest

All registrations require the main contract's native identity, admitted representation, source-generation compatibility and complete whole-unit availability inputs. Each `Candidate.source_keys` names the decisive manifest inputs, including any survivor used to replace a removed source payload. `projection_basis` retains the actual registration's domain, generation and candidate IDs. A cross-layer Story link is never a replacement factual source.

For MUST_MATERIALIZE, the union of mapped durable records must cover **all required material named by its registration**. One or more records may share a candidate; one record may combine compatible candidates. Grouping is unrestricted only within the finite admitted window and compatible availability. Narrative pacing, merging, low importance, repetition, cost, model failure and lack of current player eligibility do not waive required material. Restricted history is retained with correct availability or handled by an eligible producer later; it is not declared omitted because a current reader cannot see it.

An ID/source-reference list with a vacuous body does not materialize the required account. The readable body must preserve the required distinctions; refs support navigation and stronger-source escalation. The validator checks identities, source/facet mapping, cardinality, exactness where required and closure. As R2.1 states, structural checks alone do not prove every natural-language claim: dropped required facts or invented claims are specification violations even if a schema validator misses them. Deterministic rendering of the bounded native facts is a valid fallback; a failed generative draft is not a lawful omission.

Existing output may satisfy another candidate only when its current native dependencies, retained required material and `projection_basis` are validated and, where needed, updated atomically with coverage. A prior loose topical mention is insufficient. No persistent per-fact coverage ledger, generic skip ledger or new Story payload is added.

## 3. TRANSCRIPT registrations

### 3.1 T-MSG — accepted participant communications

| Field | Production contract |
|---|---|
| layer / source_domain_id / initial generation | `TRANSCRIPT` / `campaign.participant_messages@S` / `1` |
| Native source family/scope | Step-5.11 `runtime.message` representations admitted to durable Interaction/history, in the fixed native origin; inbound and outbound, including private/subset recipients |
| Candidate identity | `CID([message_id])`; one accepted representation, not one host rendering, fictional utterance inferred from gist or retained-payload revision |
| Enumeration / basis / cursor | Lane `msg`, §2 codecs; enrollment after inbound HDM acceptance or outbound EMISSION_COMMIT and the native durable boundary required for Story publication; no re-enrollment on retry or live absorption |
| Admission/filtering | Include admitted gameplay input, admitted OOC provenance and qualified outbound participant content. Exclude private prompts/reasoning/tool traces, unsupported host-only chatter and generated-but-unemitted drafts before enrollment. Recipient restrictions are availability, not a source filter. Non-participant diagnostics do not become eligible through a public tool surface |
| MUST_MATERIALIZE vs MAY_OMIT | Every ordinary T-MSG candidate is `MAY_OMIT`. An accepted mandatory exact archive is independently covered by T-ARCH; T-MSG progress cannot discharge it. This is deliberate Selective Exact, not permission to omit semantic communication history from E-EVT/N-EVT |
| Output/cardinality | Either zero records with `OPTIONAL_TRANSCRIPT`, or one record per selected whole message/exact slice or non-exact utterance presentation. Never combine different messages into one T record. All selected representations retain speaker, audience provenance, accepted-representation scope and message identity. Exact output requires the main exactness checks; non-exact output makes no quotation claim |
| Minimum source manifest | Stable message/enrollment envelope, Interaction/source linkage, participant/speaker/channel/audience and representation kind, payload state, exact text plus whole/slice certification when copying exactly, or sufficient native semantic communication evidence when presenting a non-exact account; outbound emission qualification and any relevant disclosure binding |
| Terminal coverage | Every message candidate in the prefix has validated optional materialization or `OPTIONAL_TRANSCRIPT` omission. Missing ordinary exact payload after lawful compaction permits omission. Missing/unknown message admission or source continuity is failure, not omission |
| Retention/correction | Ordinary T-MSG does not protect arbitrary exact payload from lawful Step-5.11 compaction. Identity/anchors and admitted surviving provenance remain interpretable. Host edit does not change accepted history. An accepted new communication/correction is a new native source; a later exact archival request enters T-ARCH and cannot pretend deleted prose survives |

For optional omission after lawful envelope retirement, the minimum manifest is the surviving native enrollment/admission anchor and owner proof of lawful payload/envelope loss; removed text or nonessential provenance is not demanded again. That exception supports omission only, not a reconstructed communication account. Missing admission or loss-legality evidence is still a source failure.

### 3.2 T-ARCH — explicit exact-archival commitments

The baseline accepts a finite, explicit archival selection through an existing accepted `runtime.interaction` / IntentPlan clause. It freezes the target message identities, whole/exact-slice selectors, expected native exact certification, requested audience restrictions and archival meaning. These are the retained parameters/provenance of that Interaction, not a new `archive_request` record family or policy registry. A conversational wish, model recommendation or transient unaccepted request is insufficient. This is the concrete Step-5.11 typed archival-request case; the baseline adds no automatic archive-all policy.

| Field | Production contract |
|---|---|
| layer / source_domain_id / initial generation | `TRANSCRIPT` / `campaign.transcript_archival_requests@S` / `1` |
| Native source family/scope | Accepted Interaction/IntentPlan archival clause and its frozen finite targets; origin is the request's origin, even if a target message came from another origin |
| Candidate identity | `CID([interaction_id, clause_id, target_ordinal])`; one request target, whose message ID/selector cannot change in place |
| Enumeration / basis / cursor | Lane `arc`, §2 codecs; enroll each frozen target at request acceptance, including requests concerning messages before T-MSG coverage. Native request and protection enrollment must be coherent before the promise is acknowledged. Multiple targets are independently pageable candidates; their accepted list is immutable |
| Admission/filtering | Only an authorized, durably accepted exact-archival commitment with sufficient surviving exact source and bounded target selection. An unsupported/unavailable exact request remains unaccepted/failed. Whole-message OOC retention requires that explicit scope; selecting an IC phrase does not enroll unrelated OOC text |
| MUST_MATERIALIZE vs MAY_OMIT | Every accepted candidate is `MUST_MATERIALIZE`; no MAY_OMIT branch. A later lawful withdrawal may end a promise through explicit native correction and scoped Story maintenance; it is not an LLM-selected omission |
| Output/cardinality | Exactly one current T record per requested target scope, retaining that whole/slice exact content and certification linkage. Compatible existing exact T output can be reused and acquire the request's contribution. Overlapping requests may share it only when each requested scope is exactly satisfied and availability remains valid; a larger body does not satisfy an exact-slice request by textual containment alone |
| Minimum source manifest | Accepted request clause/target and authorization/protection provenance; target message identity, native exact-text selector/digest and actual surviving exact text; speaker/recipient/emission qualification and availability. Gameplay-critical exact content remains independently owned/protected by its natural owner |
| Terminal coverage | Every target through the cursor has the required exact T survivor and contribution, published coherently with coverage. A summary, source digest without text, non-exact T copy, cancelled model run or T-MSG caught-up status cannot discharge the promise |
| Retention/correction | Before source exact loss, required T survivor/certification must exist under Step 5.11/5.13. Source protection and Story-reference closure are revalidated on edits or retirement. Exactness cannot be silently downgraded while the promise is live. A new target, expanded scope or different accepted wording is a new request target/source correction; it never appears behind the old cursor |

## 4. EVENTS — E-EVT

| Field | Production contract |
|---|---|
| layer / source_domain_id / initial generation | `EVENTS` / `campaign.semantic_events@S` / `1` |
| Native source family/scope | Accepted compact `runtime.semantic_event` / LOG history in the native origin, including material Actor decision/cognitive-transition history and native corrections |
| Candidate identity | `CID([semantic_event_id])`; stable accepted occurrence identity, not a Story beat/scene/session boundary |
| Enumeration / basis / cursor | Lane `evt`, §2 codecs. Every accepted SemanticEvent enters once. Child/consequence events retain their own identity. Order is history enrollment only; old fictional time does not imply an earlier source cursor |
| Admission/filtering | All accepted SemanticEvents, including action, consequence, discovery, transfer, relationship, process, combat, travel, social and custom. No player-only, visible-only, dramatic-importance, newest-only or changed-state-only filter. Failed attempts and communication occurrences still qualify when admitted as semantic history |
| MUST_MATERIALIZE vs MAY_OMIT | `MUST_MATERIALIZE` except the closed `TECHNICAL_ONLY_EVENT` predicate below. That predicate alone permits MAY_OMIT with the identically named omission code. An unrecognized accepted kind/payload defaults to required handling; an unsupported native codec fails closed |
| Output/cardinality | At least one compatible E record covers each required event's complete semantic spine below. Merge/split is allowed; no required event or required part disappears. Preserve explicit participant/entity/source/causal/temporal navigation and player-intent attribution where native history supplies it. Native record bodies need not be copied wholesale |
| Minimum source manifest | Accepted event envelope and compact event meaning; participants/location, player attribution, decision/action/communication/consequence, nonempty semantic delta and supplied causal/temporal support. Include native T0-basis binding when present, accepted mechanical/communication evidence where materially used, and source availability inputs. A mutable current Actor/world record alone cannot supply past meaning |
| Terminal coverage | Each required event in the prefix has a materialized semantic spine; only proved technical-only candidates may omit. Coverage does not assert native history has recorded every arbitrary occurrence, nor establish eligibility or exact dialogue |
| Retention/correction | Preserve the minimum native semantic input or compatible native survivor needed for this supported projection path until required output is established; do not retain full state/trace solely for E. Accepted correction is new evidence, with bounded repair of affected existing Story. Historical occurrence identity and Story allocation are not rewound |

`TECHNICAL_ONLY_EVENT` holds only when **all** are established from the admitted native representation: (1) kind is `maintenance`; (2) it reports only storage/publication/cleanup/diagnostic administration; (3) it has no accepted fictional action, communication, choice, resolved gameplay outcome, Actor decision/basis, knowledge/disclosure/relationship/process transition, or new historical/temporal/causal assertion; (4) no semantic created/changed/destroyed identity, factual/knowledge delta or player-intent meaning would be lost. Ambiguous notes, custom meaning or a nonempty unclassified delta defeat the proof. A maintenance label alone is never sufficient. A non-maintenance NO_CHANGE event admitted as history remains required: an accepted attempt may matter without changing a value.

The **semantic spine** is the event's accepted occurrence/decision/communication and outcome, identified actors/affected entities, recorded player attribution, and each distinct established factual, knowledge, relationship or process change carried by its compact native history. Preserve the meaning and direction of each change, including quantities when the event's proposition depends on them, epistemic stance versus objective truth, unsuccessful/partial outcomes, and native temporal/causal qualifications. Native WP-19 remains the authority for retained T0 decision-basis factors. Under PO-009, every WP-19-required retained material T0 factor must also be recoverable from a Story-local source-bound representation for baseline Commentator use; a native-only navigation pointer is insufficient. This does not require retaining hidden reasoning/chain-of-thought, raw schema bookkeeping, complete current state or nonessential diagnostic calculations, and it does not transfer native factual authority to Story. When provenance/meaning is insufficient, qualify the supported account and retain the limitation; never invent the missing claim or silently mark a required event omitted.

## 5. Historical-relation registrations — E-REL and N-REL

These registrations cover independently appended native historical relation evidence, especially WP-15 late relations between old anchors. A causal/temporal field already established within a SemanticEvent is part of E-EVT/N-EVT's manifest/spine and is not independently re-enrolled unless the native owner actually accepts a distinct new assertion. Native chronology/provider observation unrelated to an accepted historical relation is not a candidate merely because a clock/Agenda/index changed.

| Field | E-REL | N-REL |
|---|---|---|
| layer / source_domain_id / initial generation | `EVENTS` / `campaign.semantic_relations@S` / `1` | `NARRATIVE` / same source domain / `1` |
| Native source family/scope | Existing WP-10 SemanticEvent/relation historical evidence and WP-15 owner-anchored typed assertions; embedded or separately native-addressed, in assertion origin | Same native source; no EVENTS dependency |
| Candidate identity | §2 `rel` tuple: native owner family/id + immutable assertion selector | Identical native candidate |
| Enumeration / basis / cursor | Lane `rel`, §2 codecs; fresh ordinal at assertion acceptance, not old-anchor position or inferred fictional date | Same native enumeration, independent N coverage |
| Admission/filtering | Every accepted new historical assertion, including cause, precedence, coordinate/elapsed bounds, or accepted correction/supersession evidence. Exact domain, direction and anchors must be native-supported. Derived Agenda changes, repeated retrieval and recomputation of the same assertion are excluded | Same |
| MUST_MATERIALIZE vs MAY_OMIT | All candidates `MUST_MATERIALIZE`; no MAY_OMIT | Same |
| Output/cardinality | One or more E units explain the supported relation/correction and link both endpoints plus the native assertion. Existing endpoint account may be revised; a separate fictional occurrence is not fabricated | One or more N units incorporate/explain the relation and link its native evidence/anchors; editorial repair is allowed; no new fictional occurrence is fabricated |
| Minimum source manifest | Native assertion and stable selector, both endpoint identities, typed order/metric/provider scope and bounds where present, source compatibility/correction evidence and availability; only bounded endpoint context necessary to express the relation | Same, plus any selected existing N units as editorial dependencies |
| Terminal coverage | Each assertion through the cursor is represented with its typed meaning; source refs alone, arbitrary total ordering or a lower-layer mention are insufficient | Same obligation, independently fulfilled in N |
| Retention/correction | Native relation survivor/compaction remains WP-15/Step-5.13-owned. Preserve supported projection input or an equivalent native survivor; late/corrective evidence appends and repairs affected Story through bounded closure | Same; no campaign-wide narrative rewrite just because an old anchor gained a relation |

These source families are addressed using their existing native family/selector codecs. `campaign.semantic_relations` is a projection domain name; it does not admit a `runtime.semantic_relation` mega-family or normalize all temporal/causal evidence into a new historical ontology.

## 6. MECHANICS registrations

### 6.1 Closed required mechanical material

For M-SEG, **every** committed fact matching any row below is required, irrespective of whether Chronicler considers it exciting. Several rows may apply to one segment. Scope is accepted gameplay mechanics for any Actor/target, including NPC-only and off-screen material, with native availability retained.

| Required category | Exact selection and minimum represented meaning |
|---|---|
| Health | Any nonzero accepted HP/temp-HP/maximum-HP change, or an accepted damage/healing application including prevention/absorption when it was the resolved gameplay result: target, amount/type and before/after meaning when supplied natively |
| Resources and action economy | Any accepted spend, recovery, reservation/commit/release or loss/gain changing an available gameplay resource/use/action/reaction/slot: owner, resource identity and direction/amount; exclude internal storage/compute budgets |
| Effects, Conditions and LifeState | Accepted application/removal/replacement, value/stack/suppression/activation change or LifeState transition: affected target, semantic identity, transition and native cause/outcome |
| Duration, expiry and recovery | A committed gameplay duration/deadline/expiry/recovery change or firing with gameplay consequences: owner, accepted consequence and typed temporal qualification. Agenda reevaluation/provider cache refresh alone is excluded |
| Position and tactical relations | Accepted movement or a change in location, distance/range band, cover, reach, engagement, targeting legality or procedure participation/phase/turn that changes available gameplay choices: actors/targets and changed tactical fact. Rendering coordinates/cache refresh without changed gameplay meaning is excluded |
| Adjudicated check/save/attack/roll | An accepted resolved gameplay answer to a check/save/attack/contested/random adjudication, including miss/failure/zero-effect/immunity: actor/target, test/activity and resolved outcome; retain natively supplied roll/total/target/difficulty/degree only to the extent they are accepted outcome evidence, not all intermediate calculations |

This set is closed for generation 1. A new native mechanic mapping into these categories needs an exact source-codec mapping, not a model importance vote. A genuinely new material category requires a reviewed semantic-generation change rather than silently MAY_OMIT. Unknown semantics that might belong to a listed category cannot prove a technical-only omission. No lower numeric threshold, PC-presence test, spectator visibility test or scene/drama heuristic is admitted.

### 6.2 M-SEG — committed segment facts

| Field | Production contract |
|---|---|
| layer / source_domain_id / initial generation | `MECHANICS` / `campaign.mechanical_segments@S` / `1` |
| Native source family/scope | Step-3 immutable committed ExecutionSegment/receipt under `runtime.resolution` or direct-transition `runtime.command`, together with its MechanicalEvents; native establishment origin |
| Candidate identity | §2 `seg` tuple. A beat is not an arbitrary LLM-created episode, whole combat, complete root chain or individual low-level event row |
| Enumeration / basis / cursor | Lane `seg`, §2 codecs; enroll at immutable committed segment establishment. Include already-committed intermediate facts while later work is suspended; rejected prospective segments and transport retries produce no new candidate |
| Admission/filtering | All committed segment closures are considered. Classify against every §6.1 row from accepted MechanicalEvents and immutable receipt/export/binding evidence. A receipt with no MechanicalEvents still requires classification |
| MUST_MATERIALIZE vs MAY_OMIT | MUST if any §6.1 fact exists. MAY_OMIT with `EXECUTION_BOOKKEEPING_ONLY` only if the complete accepted segment contains none: e.g. pure cursor/fingerprint/cache/Continuation routing or fixed-but-not-yet-adjudicated RNG. Unknown/missing native classification evidence is not omission |
| Output/cardinality | At least one M beat covers every selected committed fact, actor/target and consequence, retaining native segment/event/receipt links. Merge/split across compatible facts is allowed. A partial segment account must say what has committed and must not claim the whole invocation/root chain completed |
| Minimum source manifest | Segment identity and immutable receipt; complete bounded event/export set needed to classify all §6.1 categories; selected event payloads and accepted actor/target/activity/rules bindings; RNG/outcome evidence only where used; relevant duration/cause/availability support. Do not pass a whole mutable Actor, full dependency DAG or diagnostic trace by default |
| Terminal coverage | Every selected fact has required output, or a complete no-selected-fact proof supports the single allowed omission. Checking only the first event, first target, net HP total or final receipt status is insufficient |
| Retention/correction | Compact detailed mechanics only after native live/recovery consumers and required projection inputs have sufficient survivors. Preserve selected committed facts until projected or a compatible native survivor can supply them. Later child/reaction facts get their own segment candidates; no reroll/re-execution, no waiting for scene end or full root completion |

### 6.3 M-OUT — terminal gameplay outcomes, including zero-change results

| Field | Production contract |
|---|---|
| layer / source_domain_id / initial generation | `MECHANICS` / `campaign.mechanical_outcomes@S` / `1` |
| Native source family/scope | Existing immutable terminal outcome receipt retained by an Activity Resolution or direct-transition Command; origin of the accepted outcome. Receipt stays an embedded/protocol value |
| Candidate identity | §2 `out` tuple. One terminal result per accepted execution identity; retries reuse it. Child Resolutions retain distinct identities; no extra candidate for a parent's aggregate echo of a child's result |
| Enumeration / basis / cursor | Lane `out`, §2 codecs; enroll only when the native execution owner establishes its terminal outcome. Earlier running/suspended receipt is not terminal; later completion enters a fresh lane position, regardless of old execution ID |
| Admission/filtering | All terminal invocation/direct-transition receipts are considered. Include a completed gameplay adjudication whether it changed state, failed a roll, missed, was resisted or yielded zero. A transport/validation/hydration failure before any adjudicated gameplay result is not a fictional failure |
| MUST_MATERIALIZE vs MAY_OMIT | MUST for an established gameplay result or any committed §6.1 fact summarized by a terminal partial/aborted result. MAY_OMIT with `NO_GAMEPLAY_OUTCOME` only when native evidence proves no adjudicated result and no such committed fact. Engine `FAILED` status must never be equated to a failed in-fiction check |
| Output/cardinality | One or more M units retain actor/source/targets, accepted activity/direct-transition, result/degree/partiality, natively supplied consequential roll/total/target evidence and material consequences. A compatible M-SEG record can be revised/reused; it must gain the terminal contribution and qualification. Repeating the same numbers is unnecessary; losing miss/failure is forbidden |
| Minimum source manifest | Immutable terminal receipt, native terminality/identity binding, accepted invocation/actor/target facts, selected outcome exports/RNG/effect evidence and links to the necessary committed segments/children. Full root-chain traces are not required merely to narrate one invocation; unresolved root closure must not be mislabeled settled |
| Terminal coverage | Each gameplay result is represented, including no-change outcomes; only proved no-gameplay-result candidates may omit. All overlapping segment/outcome candidate obligations must remain traceable even if one M record satisfies both |
| Retention/correction | Native idempotency/terminality and accepted interpretation remain controlling. Preserve sufficient selected result/identity evidence for supported projection; exact diagnostic traces may retire. New lawful reversal/correction appends native evidence. A Story revision never substitutes a new result for accepted mechanics |

## 7. NARRATIVE — N-EVT

| Field | Production contract |
|---|---|
| layer / source_domain_id / initial generation | `NARRATIVE` / `campaign.semantic_events@S` / `1` |
| Native source family/scope | The same accepted SemanticEvent history as E-EVT, independently read from native sources |
| Candidate identity | `CID([semantic_event_id])`; a native semantic occurrence, not a paragraph, generated episode/chapter, finished scene, session, Story Event or selected source-window ID |
| Enumeration / basis / cursor | Lane `evt`, §2 codecs; independent N coverage. Event arrivals produce N backlog regardless of whether EVENTS/MECHANICS/TRANSCRIPT have run. No dependency on scene/session closure or a lower-layer publication |
| Admission/filtering | Exactly E-EVT's accepted source set and closed technical-only exclusion. Every admitted nontechnical gameplay event is eligible/required at native acceptance, including accepted NPC/private/off-screen history under correct availability |
| MUST_MATERIALIZE vs MAY_OMIT | Exactly E-EVT's requirement: MUST for every nontechnical event; MAY_OMIT only with proved `TECHNICAL_ONLY_EVENT`. Literary taste, pacing, age, repetition or lack of an attractive story arc cannot justify omission |
| Output/cardinality | One or more coherent N passages preserve each contributing event's complete semantic spine from §4. Many events may form a passage; one event may span several units. Compression must preserve distinct choices, outcomes, participants, consequences and relevant qualifications. Detailed native mechanics may remain behind native refs where the Story promise does not require them; WP-19-required retained T0 factors must remain Story-local recoverable, directly in EVENTS or through a valid Story-local EVENTS/cross-reference path. Bare event IDs or an unrelated chapter synopsis do not satisfy the account |
| Minimum source manifest | E-EVT's decisive native event/spine/basis evidence and availability, plus only the native communication/mechanical/relation inputs actually used by this passage. Existing T/E/M/N units may support editorial continuity and crossrefs but never replace missing factual source evidence |
| Terminal coverage | Every required event through the N cursor has the required readable account in N itself. A caught-up E cursor, an M explanation or a placeholder saying “events occurred” is insufficient. N-REL has separate coverage for late historical relations |
| Retention/correction | Required N input may use an accepted sufficient native survivor; it never depends on reconstructing facts from lower Story prose. Literary revisions preserve candidate obligations and availability; structural rewrites preserve crossref/chapter closure. Late native relations/corrections repair only affected material. N may lag without blocking canon or lower layers |

NARRATIVE is not required to reproduce every optional Transcript line or every mechanically detailed intermediate fact. Those may remain discoverable through native references and their proper Story layer when outside the PO-009 baseline Commentator promise. It is required to preserve the entire semantic campaign account admitted by the existing SemanticEvent/relation owners, and qualifying retained WP-19 T0 factors must remain recoverable through the Story-local path above. A sparse native semantic log is not an instruction to invent missing scenes from current state; a native history defect must be reported under that owner.

## 8. Retention, correction and nonvacuous completeness

1. Registration is an obligation on supported projection/coverage, not a promise that a service has run. Story may remain absent or lagging; gameplay responses/save/recovery do not wait for it. A reader cannot trigger catch-up through the read-only capability.
2. For an enrolled MUST candidate, native cleanup must preserve the **minimum sufficient source material/anchor** until the required output exists, or retain an admitted equivalent native survivor. This is a typed Step-5.13 supported-projection dependency. It does not retain whole original records/traces or turn Story into an owner of gameplay truth. E and N obligations may share a compact native semantic survivor; one layer need not wait for another's materialization. T-MSG's optional payload is explicitly exempt; T-ARCH has its exact-specific protection.
3. A missing required input without an adequate survivor prevents legal materialization/coverage. Report SOURCE_NOT_AVAILABLE or the applicable integrity/currentness failure. Neither compaction nor context loss converts MUST into MAY_OMIT. Already lawfully deleted, previously unpromised legacy material is unavailable; adoption may not fabricate it or label its unknown history caught up.
4. Once required output is established, Story retains that account while its compatible coverage promise is supported. Same-ID revisions and split/merge/retirement must preserve the required material in compatible output, or explicitly end/migrate the affected promise under native authority. “Story is noncanonical” is not permission to delete required output while keeping its satisfied coverage claim.
5. T-ARCH protection is established with request acceptance; existing protection routes/source fences prevent a race with compaction. A later withdrawal or source correction requires native evidence and a bounded compatible maintenance closure. It is not a new generic cancellation status in Story. Ordinary exact gameplay protection remains independently natural-owner-owned and is not automatically an archive request.
6. Every new event/relation/result/request is admitted at a new native lane position. Source correction never mutates old candidate identity into a different event. An editorial-only edit does not rewind coverage. A source contract change affecting old candidate obligations requires explicit per-domain generation migration/reprojection/reset; prompt/model/style changes do not.
7. `CAUGHT_UP` is meaningful only for one declared layer/domain/generation/native upper basis with the required output closure verified. No global scalar is stored or inferred. A presentation may report completion over an explicitly listed finite set of domains only when each is complete and native routing proves that set is the requested scope. Omitting an origin, T-ARCH, M-OUT or N-REL from the check cannot justify a broader completion statement.
8. A newly requested chat reads the same campaign-backed Story IDs, native provenance and layer metadata under current eligibility. No host-chat cursor or model memory is used to decide what the corpus contains. A portable copy used without its native sources remains noncanonical orientation with truthful native/exact/currentness limitations.
9. Baseline Commentator readiness additionally requires the PO-009 self-contained eligibility/control projection at a compatible control basis. This architecture obligation is accepted; the concrete persisted representation is not selected or machine-realized by this document.

## 9. Adversarial acceptance matrix

The conformance question is: **given identical accepted native evidence, source scope, generation and archival commitments, can two implementations disagree about the material they are obliged to preserve?** Under these registrations, **NO**. They may differ in optional Transcript additions, prose, grouping, IDs allocated by differing publication histories and service timing. They may not differ in the required candidate/fact set while both claiming the same coverage.

| Case | Required result |
|---|---|
| Material action event is called “boring” | E-EVT and N-EVT MUST; importance ranking cannot remove it |
| Non-maintenance event records a failed attempt with zero delta | E/N MUST preserve the attempt/outcome |
| `maintenance` event carries a factual/knowledge change | E/N MUST; kind label alone cannot prove technical-only |
| Pure technical maintenance record, no semantic content | E/N MAY_OMIT only by TECHNICAL_ONLY_EVENT proof |
| Opaque custom event or unclassified nonempty notes/delta | Required handling or unsupported-source failure; no guessed omission |
| Fifty accepted events merged into one N passage | Legal only if all fifty contributions and their semantic spines remain; “a busy day” plus fifty refs is insufficient |
| EVENTS current but NARRATIVE empty over those events | N is lagging, regardless of E coverage |
| A scene never closes / a campaign changes chats mid-scene | Native event candidates remain projectable; no scene-end or chat/session delimiter required |
| Normal admitted IC/OOC message without exact archive promise | T-MSG may retain it or omit it; material communication meaning still follows native semantic history and required E/N projection |
| Exact phrase selected from mixed IC/OOC message | T-ARCH MUST retain that exact scope; unrelated private text is not implicitly archived |
| Archive request accepted after T-MSG covered/omitted its message | New T-ARCH candidate; old message cursor cannot discharge it |
| Requested exact prose already lawfully compacted with no exact survivor | Cannot accept/fulfil an exact promise; truthful unavailable, never generated quotation |
| Generated outbound draft never crosses EMISSION_COMMIT | No T-MSG candidate |
| EMISSION_COMMIT followed by interrupted rendering | Eligible committed representation keeps Step-5.12 qualification; no claim every character was read |
| Roll misses, produces no MechanicalEvent, returns gameplay failure | M-OUT MUST preserve resolved miss/failure; empty event list is not omission proof |
| Invalid target / hydration error before any gameplay result | No fictional failed-check claim; terminal M-OUT may omit only with NO_GAMEPLAY_OUTCOME proof |
| Damage segment commits, resolution awaits reaction/child | M-SEG MUST preserve committed selected facts without claiming final settlement |
| Pure fixed-RNG/Continuation segment before adjudicated outcome | M-SEG MAY_OMIT with complete EXECUTION_BOOKKEEPING_ONLY proof; later result independently enrolls in M-OUT |
| HP -1, resource +1, an off-screen NPC Condition change | M-SEG MUST; no value-size or PC-presence threshold |
| Health changes -5 then +5 in one segment | Preserve both admitted applications and causes when distinct facts; net zero does not erase them |
| Segment has health, resource and Condition consequences | Every selected category/fact must be represented; first-fact-only output fails |
| Same result appears in M-SEG and M-OUT | May share compatible output; both contributions/terminality obligations must be satisfied |
| Root aggregate receipt repeats child outcomes | No duplicate M-OUT invocation candidate; native root settlement remains distinct |
| Late accepted relation connects two old anchors | New E-REL/N-REL candidate at new native position; preserve typed relation, not invented chronology |
| Two live origins accept messages/events concurrently | Independent source domains/cursors and stable identities; absorption does not duplicate candidates |
| Current player cannot see a private event/T0 basis | Required source obligation survives; comprehensive Story-local retention remains, while availability/eligibility controls use; no privacy-based fake omission or leakage |
| NPC state changes from T0 to T1 | E/N retain the decision; qualifying retained WP-19 T0 factors remain Story-local recoverable for baseline Commentator, while native T0 authority remains distinct and current Actor values cannot replace historical evidence |
| Story source is compacted before required projection | Retain sufficient native survivor or defer cleanup; missing material cannot advance coverage |
| Required output retired while coverage remains satisfied | Invalid unless compatible replacement/end-of-promise migration preserves the contract |
| Model fails on the final required candidate | Prefix may be reselected explicitly; the failed candidate stays unconsidered |
| Implementation checks only msg/evt/seg and announces full corpus caught up | Invalid: required archival, terminal-result, relation and origin scopes also require explicit checks |
| Prose-only style rewrite changes no obligations | No semantic-generation bump; preserve material and availability |

These are design acceptance cases, not claims of executed Story runtime tests. The semantic-spine checks are stronger than mere schema/source-ID coverage and must be included in implementation acceptance and adversarial prose evaluation. Native event admission and WP-19 material-factor selection remain their original owners; this contract freezes the producer's responsibility over their already accepted results.

## 10. Compatibility, realization and boundary

The main specification's former unscoped examples were illustrative fixtures, not production registrations. Its updated `fixture.*` domain names cannot be published as baseline production coverage. The eight scoped registrations above start at semantic generation 1; no existing production generation is silently redefined or inherited. Existing experimental coverage must be rejected or explicitly reconstructed from sufficient surviving native evidence, not relabeled by string replacement.

No StoryUnit, StoryLayerProjectionState, StoryProjectionExchange or StoryRead schema version changes are performed by this documentation reconciliation. The existing `source_basis`, candidate, SourceInput material and NativeRef selector extension points carry the source contracts described here. PO-009's Story-local structured T0 representation and self-contained Commentator eligibility/control projection are **accepted architecture but not yet concretely machine-realized**: exact persisted fields, schema version impact, cache/control topology and writer mechanics remain for later authorized realization. In particular, current `GAME/SCHEMA/event.schema.yaml` is not evidence that those PO-009-specific representations already exist.

Later implementation must realize the native enrollment anchors, immutable terminal-result binding, archival clause/target/protection mapping, typed relation selectors and the accepted PO-009 Commentator-locality obligations in their proper owners. The logical membership, encoding, terminality and required output decisions are fixed here; physical filenames, indexes and native adapter implementation do not reopen them.

Version Impact Gate: **VERSION_IMPACT: NONE for existing machine/release values**. This change declares/reconciles source-contract semantics and current owner routing; it changes no implemented persistent schema, runtime module, package/protocol machine value, campaign/storage/catalog generation or hash contract. Any later material change to registered projection semantics or concrete persisted PO-009 representation must use the applicable domain/schema/version compatibility rules. Physical implementation must perform its own Version Impact Gate for actual owner/schema changes.

No runtime implementation, implementation plan, roadmap/current-stage change, gameplay archive migration, release or new native history family is authorized by this document. It completes the baseline source-registration decision surface of the main Story contract under the current PO-009 amendment.