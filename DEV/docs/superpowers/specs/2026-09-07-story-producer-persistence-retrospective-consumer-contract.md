# Story Producer, Persistence and Retrospective Consumer Contract

Status: **FINAL IMPLEMENTATION-FACING INTEGRATION SPECIFICATION — IMPLEMENTATION NOT ACTIVATED**

Date: 2026-09-07

**Scope:** the HDM-native boundary from admitted native history through optional Story transformation, deterministic publication, durable Story, correction, and bounded retrospective evidence acquisition.

**Composed owners:** Step 4; Steps 5.10 and 5.11; R2.1 and R2.3; WP-09, WP-10, WP-11, WP-13, WP-15, WP-18 and WP-19; the publication/currentness and versioning amendments linked below.

**Authority boundaries:** this specification **COMPOSES** these owners. It owns the integration representations and capability distinctions defined here. It does not replace native truth/history, Context Runtime, disclosure, chronology, mechanics, retention or transport owners.

**Non-goals:** runtime implementation, implementation planning, a new numbered work package, campaign migration, a new global progress cursor, and changes to consumer implementations. Publication of this document does not claim an independent Senior PASS or activate the next program stage.

## 1. Purpose and selected architecture

Native accepted history supplies projection candidates. An optional Chronicler transforms a bounded source bundle into a non-authoritative draft. Deterministic HDM control validates the draft, allocates final IDs and publishes a coherent Story change. Context Runtime uses typed Story/history/current-evidence capabilities to assemble context for a registered retrospective consumer.

Ordinary Master and Commentator share the capability family. Their registrations, purposes, subjects, recipients, representation floors and eligibility remain R2.3-owned. Neither role gains direct access to an unpublished draft. Chronicler output never becomes factual authority by publication.

Two viable integration realizations were considered:

| Realization | Benefit | Cost / disposition |
|---|---|---|
| Consumers adapt versioned Story files and native owners directly | Small initial infrastructure; straightforward file inspection | Each adapter must implement routing, source distinctions and compatibility correctly. Viable only if it still calls existing HDM admission/currentness machinery. Physical file coupling makes it a poor public consumer boundary. |
| Typed semantic capabilities underneath Context Runtime | Storage-neutral consumers; owner-specific evidence and currentness stay observable | Requires the explicit acquisition/result contracts below. **Selected.** One in-process provider may implement all variants; multiple owner-specific providers are equally valid. |

This selection adds no network service, mandatory database, additional LLM invocation or always-running process. Deferring the contract would leave independently developed producers and consumers to invent incompatible boundaries. Physical provider count and implementation language are not architecture decisions here.

## 2. Authority map and source manifest

Links in this table are relative to this specification's directory. Concern-specific sections of each owner, including its applicability qualifiers, govern the composition.

| Concern | Existing owner | This specification's role |
|---|---|---|
| Roles, Story layers/identity, whole-unit availability | [Step 4](2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md), §§10, 12–22 | Concrete Story envelope/payloads; narrow retrospective consumer integration |
| Candidates, allocator, coverage, publication, correction | [Step 5.10](2026-08-21-step-5-10-story-projection-durability-canonical-spec.md), §§5–20, 22–29 | Serialization and transient producer exchange |
| Message identity, exactness, compaction | [Step 5.11](2026-08-21-step-5-11-transcript-history-retention-compaction-canonical-spec.md), §§4–6, 10–19, 27–30 | Exact-reference use and read outcomes; no retention policy change |
| Outbound message admission and recipient exposure | [Step 5.12](2026-08-21-step-5-12-host-delivery-disclosure-boundary-canonical-spec.md), §§4–7, 10–14 | Consume EMISSION_COMMIT qualification; no literal-rendering/read acknowledgement promise |
| Claim-typed provenance, historical/current distinction, repair | [R2.1](2026-08-24-r2-1-continuity-history-canonical-spec.md), §§2–9 | Source-compatible Story use and native escalation |
| Requests, requiredness, discovery, eligibility, assembly | [R2.3](2026-08-24-r2-3-context-runtime-canonical-spec.md), §§2–18; [WP-09](2026-08-31-r2-7-WP-09-context-loading-resource-bounds-realization-canonical-spec.md) | Provider capabilities serving Context Runtime; consume its decisions |
| Native record families / embedded values | [WP-10](2026-09-01-r2-7-WP-10-durable-campaign-record-family-completeness-canonical-spec.md) | Native references; no new native history family |
| Physical routes and monolithic indexes | [WP-11](2026-09-01-r2-7-WP-11-physical-storage-topology-identity-indexing-canonical-spec.md) | Exact existing Story route; layer-local metadata realization |
| Publication/currentness | [WP-13](2026-09-02-r2-7-WP-13-durability-save-publication-canonical-spec.md); [publication repair](2026-09-06-hdm-publication-currentness-supported-ref-repair-amendment.md), PCR-1–7 | Story closure and scoped read-basis composition |
| Sparse chronology | [WP-15](2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-canonical-spec.md), laws 30–39 | References to temporal/causal evidence; no temporal owner |
| Story/continuity/planning integration | [WP-18](2026-09-04-r2-7-WP-18-story-continuity-dramaturg-planning-canonical-spec.md), §§1–4, 9–13; [final recovery amendment](2026-09-04-r2-7-WP-18-final-senior-recovery-canonical-amendment.md) | Layer-local realization; preserve no same-envelope feedback and deferred implementation |
| Ordinary retrospective and Actor T0 evidence | [WP-19](2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-canonical-spec.md), laws 20–23, 29–39; [retrospective owner decision](2026-09-05-hdm-gameplay-retrospective-and-campaign-exit-owner-decision.md); [Actor basis decision](2026-09-05-hdm-historical-actor-decision-basis-owner-decision.md) | Shared registered consumer edge and historical-basis capability |
| Entitlement / native information boundaries | [Access Control](../../../ARCHITECTURE/ACCESS_CONTROL.md), Step 4 and R2.3 | Current admitted access only; preference can narrow it |
| Version namespaces | [Versioning policy](2026-09-05-hdm-versioning-namespace-compatibility-policy.md), §§4–5, 9–12, 17–20; [compact policy](../../../RELEASE/VERSIONING.md) | Four justified serialized-contract namespaces; existing semantic generation |
| Proof classification | [WP-22](2026-09-07-r2-7-WP-22-verification-test-evaluation-completeness-canonical-spec.md), §§2–8, 11, 13.5 | Separate specification/scenario evidence from executable realization and empirical acceptance |

Existing machine/instruction evidence was checked at the integration boundary: `GAME/SCHEMA/event.schema.yaml`, `GAME/SCHEMA/campaign_manifest.schema.yaml`, `GAME/CAMPAIGN/MANIFEST.yaml`, `GAME/CORE/CHRONOLOGY.md`, `NARRATIVE.md`, `INFORMATION.md`, `DEV/SCHEMAS/resolution-receipt.schema.json`, `temporal-binding.schema.json`, and `DEV/TESTS/test_step4_story_retirement_contract.py`. These do not yet realize this Story contract. Their current incomplete/pre-release shapes do not override their semantic owners. In particular, a receipt is an embedded native execution value, and TemporalBinding is not a universal historical chronology record.

## 3. Terms, types and invariants

**Story unit:** one independently addressable noncanonical presentation record. **Source candidate:** an owner-enumerated opportunity/obligation for projection. **Coverage:** terminal consideration under one layer/source-domain/semantic-contract generation. **Representation binding:** evidence identifying the exact representation used, interpreted by its owner. **Read basis:** a transient collection of such bindings and current admission evidence, never a new historical snapshot owner.

The data model is JSON-compatible: objects have string keys; numbers used as integers must be represented losslessly; arrays are ordered; no implicit coercion, custom YAML tags, duplicate keys or cyclic values are legal. YAML is a serialization of the same values. An omitted optional field and an empty collection have the meanings stated below; `null` is permitted only where explicitly listed. Unknown fields, union variants, families and incompatible versions fail closed unless explicitly supported by the applicable versioned reader. Extension is by the owning contract, not by accepting arbitrary LLM keys.

Notation in tables: **R** required; **O** optional, but required when the stated condition applies; **P** persisted; **T** transient; **D** derived. **NC** noncanonical content/reference/derived routing, with no gameplay authority. **LC** authoritative only for local Story control/editorial structure, never gameplay truth. **NO** native-owner semantics, merely referenced or transported here. **CR** Context Runtime authority, consumed here. Every persisted field below uses its enclosing schema's compatibility rule; native values retain their native interpretation/version rules as well.

### 3.1 Minimal references

| Value / field | Type and requirement | Owner / authority / version behavior |
|---|---|---|
| `StoryRef` | String with `T`, `E`, `M` or `N` followed by the canonical decimal sequence, padded to at least six digits | Step 4; NC identity within enclosing campaign; Story schema |
| `NativeRef.family` | R nonempty registered native family string | Native owner/WP-10; NO; family codec |
| `NativeRef.identity` | R nonempty array of strings, complete native identity components in owner-defined order | Native owner/WP-11; NO; no new universal ID allocation |
| `NativeRef.selector` | O owner-defined JSON value selecting an embedded value or exact slice | Native owner; NO; legal only for a registered selector codec |
| `SourceDependency.ref` | R `NativeRef` | Native owner; NC linkage, no automatic proof |
| `SourceDependency.basis` | O owner-defined JSON compatibility evidence, required when identity alone cannot preserve the projected meaning | Native source owner; NO interpretation; no universal revision/exactness algorithm |
| `EntityRef` | `NativeRef` naming an admitted world entity, without a selector unless its owner requires one | Native identity owner; NC reference |

A selector never means an arbitrary filesystem path, JSONPath, query program or unrestricted Git lookup. A selected receipt uses its execution owner's family/identity and its registered embedded selector; it does not acquire a `receipt` native record family. Actor decision basis uses a SemanticEvent and an owner-defined factor selection. It does not become a historical `world.actor` snapshot family.

Owner codecs must expose validation, bounded resolution, compatibility and retention results sufficient for the requested capability. An immutable SemanticEvent reference may need no stored `basis`; a mutable value requires a valid owner-defined historical binding or retained T0 value in its proper native history owner. A pointer to current T1 state cannot pass as T0. An unresolved codec is `UNSUPPORTED_SCHEMA_OR_CONTRACT`, not permission for a guessed reference interpretation.

`StoryRef` carries the layer through its prefix. Persisted Story units therefore **do not store `layer`, `sequence`, a second `id`, campaign ID or physical path**. The enclosing campaign supplies campaign scope. If any transport wrapper supplies a layer, it must equal the prefix-derived layer. Minimum-width decimal formatting is canonical: sequence 1 is `E000001`, not `E0000001`; sequence 1000000 is `E1000000`. Sequences start at 1; high-water 0 means no allocation yet. The sequence is not fictional time.

### 3.2 Invariants

1. Gameplay truth, mechanics, SAVE and native recovery do not depend on Story presence, freshness or successful generation.
2. Chronicler cannot admit sources, allocate final IDs, advance coverage, authorize disclosure or publish.
3. Published Story has valid identity, source/availability metadata and complete Story reference closure.
4. Publication order, source enumeration, ID order and editorial order supply no fictional temporal/causal inference.
5. Source-bound, eligible, published and exact are different predicates. None implies the others.
6. Story absence, lawful omission, query exhaustion and provider unavailability do not generally prove semantic absence.
7. Every material factual, exact, motive, mechanical or current-state claim uses the appropriate admitted evidence class.
8. Spoiler preference can only reduce the HDM entitlement ceiling. Story availability cannot grant access or create disclosure.
9. Reader-dependent eligibility/currentness/exactness are evaluated at use time; no persisted `eligible_for_reader`, `current`, `truth_verified` or `is_exact` flag is admitted.
10. Retrospective reading never requires campaign mutation, projection catch-up, persisted index repair, disclosure writes or retaining a new historical snapshot.

## 4. End-to-end lifecycle

Native owners first admit the evidence and establish its relevant durable/publication boundary. Deterministic projection control selects a bounded candidate window under a source-domain contract and builds `StorySourceBundle`. Optional generation returns `StoryProjectionDraft`. HDM validates source dependencies, candidate dispositions, content shape, availability and reference closure, then allocates IDs and constructs one coherent write-set. Successful native publication makes the Story representation durable and advances the corresponding coverage.

Later Context Runtime routes an admitted retrospective request to the capabilities in §20. It checks owner currentness and eligibility, escalates from Story to stronger sources where the task requires, and owns final packet assembly. Correction uses the same deterministic publication boundary. A read never implicitly performs correction or catch-up.

Unaccepted prospective preparation, un-emitted Narrator drafts, hidden reasoning and unpublished HOT/LIVE-only material are outside the retrospective evidence boundary. A persisted LIVE source is admissible only when the native routing/publication owner selects it; branch presence is insufficient. Ordinary Master may separately use its existing gameplay current-state capabilities under their own contracts, but must not relabel volatile gameplay state as the committed NOW capability defined here.

## 5. Common persisted Story envelope

One record is an object with the following fields and exactly one prefix-selected payload from §§6–9.

| Field | Shape / requiredness | State, owner, authority | Version behavior |
|---|---|---|---|
| `schema_version` | R positive integer; this contract starts at `1` | P, StoryUnit contract, LC schema dispatch | Independent StoryUnit schema |
| `story_id` | R `StoryRef` | P, Step 4/5.10, LC identity | Preserve across editorial edits; never reuse |
| `content.body` | R nonempty string | P, layer/Chronicler projection, NC | StoryUnit; body changes revalidate dependencies |
| `content.title` | O nonempty string | P, Story editorial owner, NC | Same; whole-unit availability includes title |
| `sources` | R nonempty map of local source keys to `SourceDependency` | P, Step 5.10/R2.1 + native semantics, NC/NO | StoryUnit envelope; native codec compatibility |
| `projection_basis` | R nonempty array of `ProjectionContribution` below | P, Step 5.10, LC provenance | Shape version independent of semantic generation |
| `entity_refs` | O unique `EntityRef[]`, absent means no asserted links | P, native identities, NC | StoryUnit/native identity contracts |
| `cross_refs` | O unique `StoryRef[]`, absent means none | P, Step 4/5.10, NC navigation | Target closure required; no factual promotion |
| `temporal_source_keys` | O unique source-key array | P, WP-15, NC references to NO evidence | Referenced source must support temporal semantics |
| `causal_source_keys` | O unique source-key array | P, WP-15/native history, NC references | Causation must be owner-supported, not inferred from order |
| `availability` | R `Availability` below | P, Step 4, NC requirements consumed by CR | Recompute/revalidate on material edits |
| `payload` | R prefix-specific object | P, §§6–9, NC | Same StoryUnit schema; wrong payload is invalid |

Local source keys match `[A-Za-z][A-Za-z0-9_-]*`. They are names inside one record, not campaign identities. A source key referenced by a payload or relation must exist in `sources`. Every stored source must serve provenance, compatibility, availability or a declared payload dependency; unrelated source accumulation is invalid. Native bodies are not copied wholesale into `sources`.

`ProjectionContribution` fields are all required and persisted: `source_domain` (nonempty owner-defined string), `semantic_contract_generation` (positive integer), `candidate_ids` (nonempty unique array of opaque source-native strings). The enclosing Story ID supplies the layer. One candidate can contribute to multiple records and one record can include multiple candidates. These contributions record grouping/splitting provenance, not terminal coverage by themselves. Their owner is Step 5.10; authority is LC provenance only. Their shape follows StoryUnit schema; generation meaning remains domain-local.

`Availability` has required `requires_story_refs: StoryRef[]` and optional `requires_source_refs: NativeRef[]`; both are unique arrays, and an empty array declares no requirements of that particular kind. It never declares public/unrestricted access. Source requirements retain native disclosure semantics. Story reveal prerequisites must be resolvable without a cycle; cyclic mandatory prerequisites are a validation failure. Ordinary navigation crossrefs may form cycles and do not themselves grant reveal eligibility.

### Example convention

The records and logical values below describe a **fictional validation fixture**, not an existing campaign or observed runtime result. IDs and opaque handle strings are fixture values. Native references without selectors use their owner's complete-record identity semantics. Native material is a bounded owner-provided view, not a new serialized native schema. The examples use one admitted `campaign.semantic_events` source domain; production domain enumeration/basis codecs must satisfy §11.

## 6. TRANSCRIPT persisted schema

Default granularity is one accepted communication/utterance per Story unit. All payload fields follow StoryUnit schema.

| Payload field | Shape / requiredness | State / semantic owner / authority |
|---|---|---|
| `message_source_key` | R one source key resolving to `runtime.message` | P, Step 5.11, NC linkage to communication evidence |
| `speaker` | R union: `{kind: ENTITY, ref: EntityRef}` or `{kind: ROLE, role: string}` | P, native communication provenance, NC; role spelling must be admitted by that source |
| `recipient_refs` | O unique native participant/entity refs when source establishes recipients | P, native communication owner, NC; distinct from readers entitled to see Story |
| `interaction_ref` | O native `runtime.interaction` ref when useful/retained | P, native owner, NC provenance |
| `exact_text_ref` | O native full-message or owner-selected exact-text ref | P, Step 5.11, NC claim binding for `content.body`; no stored certification flag |

The named message must occur in `sources`; every additional payload ref must be admitted in the producer source manifest. A role speaker is neither a newly created Actor nor a claim about subjective NPC thought. Outbound communication must meet Step-5.12 EMISSION_COMMIT admission. This is not proof that every character rendered or that the recipient read/comprehended it: interruption after emission commit may leave only a visible prefix while the full frozen representation remains accepted. Edited/paraphrased text remains communication-oriented Story but cannot be quoted as original without §17 validation.

```yaml
schema_version: 1
story_id: T000001
content:
  body: The northern gate is safe.
sources:
  message:
    ref:
      family: runtime.message
      identity: [message-00000001]
projection_basis:
  - source_domain: campaign.participant_messages
    semantic_contract_generation: 1
    candidate_ids: [message-00000001]
entity_refs:
  - family: world.actor
    identity: [actor-0042]
availability:
  requires_story_refs: []
payload:
  message_source_key: message
  speaker:
    kind: ENTITY
    ref:
      family: world.actor
      identity: [actor-0042]
  exact_text_ref:
    family: runtime.message
    identity: [message-00000001]
```

This can establish that the guard communicated the sentence, and, when verified, its exact accepted wording. It does not establish that the gate was safe.

## 7. EVENTS persisted schema

| Payload field | Shape / requiredness | State / semantic owner / authority |
|---|---|---|
| `event_source_keys` | R nonempty unique source-key array; each resolves to native SemanticEvent/history evidence | P, Step 4 LOG/Step 5.10, NC factual-spine linkage; StoryUnit schema |

The common body is the human-meaningful beat. Common entity, temporal, causal and crossrefs supply the other requested links. A merged beat names all contributing candidates/sources; split beats retain the same source candidate and their own factual source selections. No redundant `is_split` flag, new occurrence ID or copied event delta is necessary. If factual detail matters, native occurrence evidence remains the stronger source.

```yaml
schema_version: 1
story_id: E000001
content:
  title: The gate opens
  body: The guard opened the northern gate for the party.
sources:
  event:
    ref:
      family: runtime.semantic_event
      identity: [event-00000001]
projection_basis:
  - source_domain: campaign.semantic_events
    semantic_contract_generation: 1
    candidate_ids: [event-00000001]
entity_refs:
  - family: world.actor
    identity: [actor-0042]
availability:
  requires_story_refs: []
payload:
  event_source_keys: [event]
```

## 8. MECHANICS persisted schema

| Payload field | Shape / requiredness | State / semantic owner / authority |
|---|---|---|
| `mechanical_source_keys` | R nonempty unique keys selecting admitted mechanical episode evidence | P, native mechanical/execution owner, NC references; StoryUnit schema |
| `resolution_refs` | O unique `NativeRef[]` where native resolutions materially support the episode | P, native execution owner, NC references; owner codec |
| `receipt_refs` | O unique native embedded-value refs when receipt detail is needed | P, receipt's native execution owner, NC references; registered selector required |

An episode may summarize several native events. Source types and selected receipts must support the claimed mechanical explanation. The body must not serve as a second execution log, replay instruction, full rules trace or current HP/resource owner. Exact mechanics explanation escalates to the native evidence capability.

```yaml
schema_version: 1
story_id: M000001
content:
  body: The lock check succeeded with a total of 17.
sources:
  check:
    ref:
      family: runtime.mechanical_event
      identity: [mechanical-event-00000001]
projection_basis:
  - source_domain: campaign.mechanical_episodes
    semantic_contract_generation: 1
    candidate_ids: [mechanical-event-00000001]
entity_refs:
  - family: world.actor
    identity: [actor-0042]
availability:
  requires_story_refs: []
payload:
  mechanical_source_keys: [check]
  resolution_refs:
    - family: runtime.resolution
      identity: [resolution-0000001]
```

The example assumes the native mechanical event supports the displayed total and outcome. It supplies no receipt selector because no receipt-level query is needed.

## 9. NARRATIVE persisted schema

| Payload field | Shape / requiredness | State / semantic owner / authority |
|---|---|---|
| `factual_source_keys` | R nonempty unique keys tracing the factual spine to native sources | P, Step 4/R2.1/Step 5.10, NC linkage; StoryUnit schema |

Common `cross_refs` may link Transcript, Events, Mechanics and other Narrative units for navigation/editorial continuity. Those references cannot replace native factual-spine dependencies. Literary interpretation must stay identifiable as such and cannot manufacture occurrence, motive, dialogue or causal truth. Chapter membership/order belongs to layer editorial metadata (§10), so records do not duplicate chapter identity or ordinal.

```yaml
schema_version: 1
story_id: N000001
content:
  title: Through the northern gate
  body: The guard opened the northern gate, and the party passed through.
sources:
  opening:
    ref:
      family: runtime.semantic_event
      identity: [event-00000001]
  passage:
    ref:
      family: runtime.semantic_event
      identity: [event-00000002]
projection_basis:
  - source_domain: campaign.semantic_events
    semantic_contract_generation: 1
    candidate_ids: [event-00000001, event-00000002]
cross_refs: [E000001, E000002]
availability:
  requires_story_refs: [E000001, E000002]
payload:
  factual_source_keys: [opening, passage]
```

Both E records must already be durable for this ordinary NARRATIVE publication. Their wording is not the evidence for the party's passage.

## 10. Projection-state schema and layer metadata

The fixed file is `<story_root>/<layer>/PROJECTION_STATE.yaml`.

| Field | Shape / requiredness | State / owner / authority | Version behavior |
|---|---|---|---|
| `schema_version` | R positive integer, initially `1` | P, StoryLayerProjectionState, LC | Independent persisted schema |
| `layer` | R `TRANSCRIPT`, `EVENTS`, `MECHANICS` or `NARRATIVE` | P, Step 5.10, LC | Must match directory and every indexed ID |
| `story_id_allocator_high_water` | R nonnegative integer | P, Step 5.10, LC | Monotonic, no ordinary reuse/reset |
| `coverage_by_source_domain` | R map, empty for no coverage | P, Step 5.10, LC | Entry generation remains independent of file schema |
| `lookup` | R map keyed by Story ID to `LookupEntry` | P but derived, Step 5.10/R2.3, NC | Rebuildable; enclosing state schema |
| `chapters` | O ordered `Chapter[]`, allowed only for NARRATIVE | P, Step 4 editorial owner, LC presentation | Unique editorial data, not a derived index; state schema |

Each coverage map value has required `semantic_contract_generation: positive integer` and required `terminal_coverage`, a union:

| Variant | Exact fields | Meaning |
|---|---|---|
| `CONTIGUOUS` | `kind: CONTIGUOUS`, `through: string or null` | Every enumerated candidate through the owner-defined token was terminally considered under the declared generation; `null` is the start boundary |
| `SPARSE` | `kind: SPARSE`, `evidence: owner-defined JSON value` | Registered source codec supplies bounded sparse membership/continuation proof; admitted only when contiguous enumeration cannot satisfy the source contract |

Both variants are persisted LC metadata owned by Step 5.10 plus the source-domain codec. Sparse is an extension point with a closed admission rule, not permission for an unbounded array of all historic candidates. Unsupported sparse codecs fail closed. No domain may use a generic Git HEAD as its `through` token.

`LookupEntry` has required unique arrays `entity_refs: EntityRef[]`, `source_refs: NativeRef[]`, and `story_refs: StoryRef[]`. It is a deterministic projection of the corresponding record: entity refs from `entity_refs`; source refs from `sources.*.ref`; Story refs from `cross_refs` plus `availability.requires_story_refs`. Canonical reference equality follows the native codec, with set deduplication. No body, title, private Actor factors, currentness grant or availability policy is copied into this routing entry.

There is exactly one lookup entry per current record in the layer. Known-ID reads derive the record path directly and need no index load. Bounded navigation, entity/source lookup and structural inbound-ref discovery may load the applicable monolithic layer metadata. The table is internal routing data: even IDs and counts may be protected. It is not a role-visible index dump.

`Chapter` has required `narrative_refs: nonempty unique StoryRef[]` (N prefix only) and `availability: Availability`; optional nonempty `label`, `title`, `part_label`, `synopsis`. Order is explicit. Chapters have no world identity; their transient list positions are meaningful only against that exact metadata representation. Chapter text/order is persisted editorial information and cannot be reconstructed from unordered records in general. Its loss may harm presentation fidelity. It is not classified as a disposable derived cache.

No additional Story file is required by this version. Embedding compact lookup and editorial metadata in the accepted layer-state file avoids a second topology and an otherwise unnecessary schema namespace. Monolithic metadata still obeys R2.3's admitted resource envelope; an oversized file produces a bounded failure, not a hot-path full-Story scan. Partitioning is dormant pending the existing measured-scale/host-limit trigger.

```yaml
schema_version: 1
layer: EVENTS
story_id_allocator_high_water: 2
coverage_by_source_domain:
  campaign.semantic_events:
    semantic_contract_generation: 1
    terminal_coverage:
      kind: CONTIGUOUS
      through: semantic-event-position-2
lookup:
  E000001:
    entity_refs:
      - family: world.actor
        identity: [actor-0042]
    source_refs:
      - family: runtime.semantic_event
        identity: [event-00000001]
    story_refs: []
  E000002:
    entity_refs: []
    source_refs:
      - family: runtime.semantic_event
        identity: [event-00000002]
    story_refs: []
```

Here E000002 is the fixture's separate passage beat with source candidate `event-00000002`. Coverage records consideration of both native candidates; it says nothing about NARRATIVE's coverage. `lookup` is rebuildable from surviving forward records. Missing/stale lookup cannot prove absence or authorize retirement. If completeness cannot be proved within the bounded operation, structural maintenance waits for an authorized rebuild; readers may still perform independently valid known-ID reads.

## 11. Source-domain and coverage model

A registered `(layer, source_domain, semantic_contract_generation)` contract must define:

| Requirement | Responsible owner |
|---|---|
| Native source family/scope and admitted candidate identity | Native source + Step 5.10 projection mapping |
| Source basis, token codec, comparison and bounded enumeration | Native source; no late insertion behind a valid contiguous cursor |
| Required source/excerpt manifest and source compatibility predicates | Native source; current routed selection remains its owner |
| `MUST_MATERIALIZE` / `MAY_OMIT` and output/cardinality rules | Typed projection contract; not model confidence |
| Terminal coverage interpretation and membership proof | Same layer/domain/generation contract |
| Retention/compaction continuity and correction routing | Source owner, Steps 5.11/5.13 and R2.1 |

These are engine contract registrations, not a new campaign registry, queue or ledger. Source-domain IDs may identify campaign or selected native epoch scopes; the codec must retain native source identity and must not collapse independently moving scopes into a global sequence.

The default eligible mappings are accepted participant communications to TRANSCRIPT, compact SemanticEvent history to EVENTS, meaningful native mechanical episodes to MECHANICS, and accepted historical evidence to NARRATIVE. A mapping must explicitly declare its disposition policy when activated. An ordinary optional candidate may be omitted; an admitted archival/materialization obligation is `MUST_MATERIALIZE`. This specification does not turn every native event, mechanic or conversation into mandatory Story.

The publisher validates the whole selected bounded window. `MATERIALIZED` references compatible existing/new output satisfying the candidate's cardinality; `OMITTED` is terminal only for a candidate whose contract allows the supplied omission. Generation failure, malformed output, unavailable required evidence and failed publication leave the candidate unconsidered. A smaller valid prefix requires a newly selected window; the model cannot silently truncate the bundle's obligation.

Contiguous coverage intentionally carries no per-candidate omission ledger. `MAY_OMIT` plus coverage alone proves consideration, not actual omission. `OMITTED_BY_PROJECTION_CONTRACT` is returned only when the native projection mapping and complete bounded output membership make that disposition provable; otherwise absence stays insufficient/unknown. A source contract requiring durable sparse dispositions must justify and own them.

Semantic generation changes that alter admission, enumeration meaning, terminal disposition or required output invalidate reuse of incompatible old coverage. Explicit generation migration/reprojection/reset is scoped to the affected domain. Prompt/model/style changes alone do not bump that generation or automatically replay history.

## 12. StorySourceBundle

This is a transient JSON-compatible value produced by deterministic HDM control. It is not a campaign file, job or authorization token that an external caller can mint. Handles below identify exact values held by the invoking control boundary; they must be resolved/validated there, not trusted by string equality supplied by a model.

| Field | Shape / requiredness | Owner / authority / lifetime |
|---|---|---|
| `exchange_schema_version` | R positive integer, initially `1` | StoryProjectionExchange schema; T dispatch |
| `bundle_ref` | R nonempty opaque string | Deterministic control; T identity of this exact bundle, not durable idempotency |
| `layer` | R layer enum | Step 5.10; T scope |
| `operation` | R `CATCH_UP`, `EDITORIAL_REVISION` or `STRUCTURAL_REWRITE` | Step 5.10; T permitted operation |
| `campaign_pin` | R opaque native transport/publication pin | Native publisher; T exact read/publication input, not source watermark |
| `expected_layer_representation` | R opaque exact binding or `null` for owner-validated initial absence | Story control; T optimistic precondition |
| `windows` | R array of `SourceWindow` | Source contracts; T obligations; empty only for correction without coverage advancement |
| `source_manifest` | R nonempty map of local source keys to `SourceInput` | Native owners/control; T complete admitted source footprint |
| `availability_inputs` | R map from every source-manifest key to `Availability` | Existing disclosure/availability owners via control; T requirements, not an access grant |
| `editorial_context` | R array of `{story_id, representation, unit}` | Story control; T bounded already-durable context; may be empty |
| `correction_targets` | R map from StoryRef to `{expected_representation, action}` | Story control; T allowed target set; `action` is `REVISE` or `RETIRE`; empty for ordinary catch-up |
| `maintenance_ref` | O opaque identity of one control-owned `StoryMaintenanceSet` | T; allowed only for the explicit structural composition in §16.2 |

`SourceInput` has required `dependency: SourceDependency`, `representation: opaque string`, and `material: OwnerValue`. `OwnerValue` is JSON data validated and supplied by the named native owner's admitted bounded-view codec. It is never arbitrary model-generated native truth or a universal historical payload schema. The representation binds precisely the owner data/excerpt used; existing external object identities may supply it where sufficient. Additional material needed for validation is acquired by control under the same bounded source contract.

`SourceWindow` has required `source_domain`, `semantic_contract_generation`, `source_basis: OwnerValue`, `expected_coverage: TerminalCoverage`, `proposed_coverage: TerminalCoverage`, and `candidates: Candidate[]`. Each `Candidate` has required `candidate_id: string`, `requirement: MUST_MATERIALIZE | MAY_OMIT`, and nonempty `source_keys: string[]`. These keys address the bundle manifest. Source contract validation supplies any stricter cardinality/omission predicate; there is no LLM-defined policy field.

Windows have distinct source domains and positive generations; candidate IDs are unique within their domain window. CATCH_UP requires a nonempty candidate window and real terminal progress. EDITORIAL_REVISION has no coverage window or retirement and revises only authorized same-ID targets. STRUCTURAL_REWRITE may have empty windows when repairing already-covered presentation structure. Correction targets and the bundle's layer must agree; cross-layer work uses separate layer bundles inside §16.2's common closure.

Control binds the bundle to all actual source, layer, referenced-Story, contract-generation and availability dependencies. A `bundle_ref` alone cannot prove those dependencies are still valid. Candidate/material disclosure to Chronicler follows its admitted role context; hidden reasoning and prospective planning are excluded even if physically available.

The fixture starts before any EVENTS allocation. Its native event view establishes the bounded transition being projected.

```json
{
  "exchange_schema_version": 1,
  "bundle_ref": "bundle-events-1",
  "layer": "EVENTS",
  "operation": "CATCH_UP",
  "campaign_pin": "published-campaign-pin-1",
  "expected_layer_representation": "events-state-empty",
  "windows": [{
    "source_domain": "campaign.semantic_events",
    "semantic_contract_generation": 1,
    "source_basis": "semantic-event-position-1",
    "expected_coverage": {"kind": "CONTIGUOUS", "through": null},
    "proposed_coverage": {"kind": "CONTIGUOUS", "through": "semantic-event-position-1"},
    "candidates": [{
      "candidate_id": "event-00000001",
      "requirement": "MUST_MATERIALIZE",
      "source_keys": ["event"]
    }]
  }],
  "source_manifest": {
    "event": {
      "dependency": {"ref": {"family": "runtime.semantic_event", "identity": ["event-00000001"]}},
      "representation": "native-event-1-admitted-view",
      "material": {"id": "event-00000001", "participants": ["actor-0042"], "delta": {"factual_changes": [{"summary": "The guard opened the northern gate for the party."}]}}
    }
  },
  "availability_inputs": {"event": {"requires_story_refs": []}},
  "editorial_context": [],
  "correction_targets": {}
}
```

The minimal fixture view is not a complete `semantic_event.schema.yaml` record; it is the native codec's admitted excerpt. The source remains the full native owner. Producer implementation must not validate this excerpt as though it were a substitute persisted SemanticEvent.

## 13. StoryProjectionDraft

Every field here is transient NC proposal data interpreted under `exchange_schema_version`; deterministic control remains the decision maker.

| Field | Shape / requiredness | Contract |
|---|---|---|
| `exchange_schema_version` | R same supported exchange version | Bundle/draft pair evolves together |
| `bundle_ref` | R exact originating bundle reference | No switching to another admitted context |
| `records` | R ordered array of `DraftRecord` | Empty only when all window candidates may legally omit or a valid structural retirement needs no replacement |
| `candidate_results` | R `CandidateResult[]` | Exactly one result per bundled window candidate; empty for correction-only exchange |
| `retirements` | R array of `{story_id, expected_representation, replacement_keys}` | Structural operation only; replacement keys address draft records; empty otherwise |
| `chapters` | O replacement `Chapter[]` for NARRATIVE | Bound to expected layer representation; uses draft references where needed |

`DraftRecord` has required `draft_key`, `action` and `unit`. Keys are unique local strings with the source-key syntax. `action` is exactly `{kind: CREATE}` or `{kind: REVISE, story_id: StoryRef, expected_representation: string}`. REVISE must match a control-authorized correction target; it does not allocate identity. `unit` has the common Story fields except `schema_version` and `story_id`, which control supplies. In `cross_refs`, availability Story requirements and proposed chapter members, a `DraftStoryRef` is either a durable StoryRef string or `{draft_key: string}`. Only inside an admitted `StoryMaintenanceSet`, `{bundle_ref: string, draft_key: string}` may address a companion layer's draft. No other draft reference syntax is accepted. Each existing ID can be revised or retired at most once in the complete publication, never both.

The draft's source dependencies must match admitted manifest dependencies; local source keys may be renamed if all payload links and candidate mapping remain explicit. Native payload/participant/entity/temporal/causal refs must be admitted by the manifest or its registered identity bindings. A payload ref materially supporting the body must also appear in persisted `sources`, with any required native basis. Existing Story references must be among the bundle's admitted editorial dependencies; companion-draft refs require the structural group validation below. Extra factual sources or relaxed availability requirements are rejected.

`CandidateResult` has required `source_domain`, `candidate_id`, and one of:

- `outcome: MATERIALIZED` with required nonempty unique `record_keys: string[]`;
- `outcome: OMITTED` with required nonempty `reason_code: string`, accepted only by that exact source contract.

Mapped records must actually retain the candidate's projection contribution and required native dependencies. Each contribution must name a bundled candidate or an explicitly admitted previously covered correction target; arbitrary past candidate IDs are invalid. A generic `success`, model confidence or free-text excuse cannot satisfy a missing obligation. For correction-only records, contributions trace the covered candidates being repaired; the control boundary independently checks that retained coverage remains legal.

```json
{
  "exchange_schema_version": 1,
  "bundle_ref": "bundle-events-1",
  "records": [{
    "draft_key": "opening",
    "action": {"kind": "CREATE"},
    "unit": {
      "content": {"title": "The gate opens", "body": "The guard opened the northern gate for the party."},
      "sources": {"event": {"ref": {"family": "runtime.semantic_event", "identity": ["event-00000001"]}}},
      "projection_basis": [{"source_domain": "campaign.semantic_events", "semantic_contract_generation": 1, "candidate_ids": ["event-00000001"]}],
      "entity_refs": [{"family": "world.actor", "identity": ["actor-0042"]}],
      "availability": {"requires_story_refs": []},
      "payload": {"event_source_keys": ["event"]}
    }
  }],
  "candidate_results": [{"source_domain": "campaign.semantic_events", "candidate_id": "event-00000001", "outcome": "MATERIALIZED", "record_keys": ["opening"]}],
  "retirements": []
}
```

Chronicler may choose wording, grouping, summaries, framing and draft-local structure. It cannot return a native-state mutation, final ID for CREATE, allocator/coverage successor, publication success, entitlement decision, authoritative chronology or restored mechanics. Deterministic copying is valid and need not invoke Chronicler.

## 14. Draft-local identity and final allocation

After validating all draft content and dependencies, control processes CREATE records in their explicit array order, assigning successive unused IDs above the current layer high-water. REVISE records retain their authorized IDs. It produces a complete local-key-to-final-ID mapping and resolves every `DraftStoryRef` before constructing persisted records, chapters and lookup metadata.

Validation then repeats reference/availability closure against the complete proposed tree. A reference may target an already-durable unit at the admitted basis or a unit in this same coherent transaction. Ordinary cross-layer targets must already be durable; a draft cannot schedule or require another layer's future output. Cycles in ordinary crossrefs are permitted, but dangling targets and cyclic reveal prerequisites are not.

Failed/abandoned allocation is not a durable reservation. Only published high-water advances. Published IDs are never reused after revision or retirement. Representation-binding mismatch on a REVISE target is a conflict; allocator remapping cannot fix it.

## 15. Deterministic validation and publication

The validation boundary checks schema/union shape, finite size/cardinality, native reference/selector admission, exact manifest dependency compatibility, source-domain generation and coverage legality, source-to-output mappings, exactness obligations when applicable, all Story reference closure, and whole-unit availability. It forbids writes outside the permitted Story closure.

Availability must cover every source/content/metadata dependency. The producer may suggest additional restrictions. Removing a requirement requires deterministic re-derivation from the owning rules, not a model assertion. A material edit invalidates prior availability validation. Structural validation does **not** prove that every sentence or literary inference is semantically correct; source-bound but poor prose remains a repairable noncanonical defect under R2.1.

### 15.1 Publication unit

Ordinary catch-up changes one layer: new/revised/retired record files plus that layer's `PROJECTION_STATE.yaml` carrying coherent allocator, lookup/editorial changes and applicable coverage. No coverage may precede its required output. A coverage-only commit is legal for a fully considered `MAY_OMIT` window.

Structural maintenance may include the bounded affected records and layer-state files across layers to preserve existing refs. It is one same-campaign transaction, not a new cross-layer distributed protocol. It cannot mutate native history/current owners or make gameplay wait for Story.

For supported Git-backed publication, pin H, construct C with sole parent H, then update the existing selected ref to C with `force=false`. The connector has no separate expected-old-SHA argument. The native monotonic fence and publication epistemics in PCR-1–7 govern. Merely creating a blob/tree/commit does not publish Story.

### 15.2 Movement, retry and acknowledgement

| Observation | Required action |
|---|---|
| Prepublication validation/generation failure | Publish nothing; leave coverage/high-water unchanged |
| Confirmed accepted ref response | Publication succeeded at that response point; no lease against later movement |
| Non-fast-forward/stale-source rejection | Refresh actual owners; never force the prepared sibling commit |
| Movement disjoint from source/layer/contract/Story-ref/availability footprint | Control may rebuild on the new verified parent and reuse generation |
| Same-layer coverage already terminally covers the intended window | Suppress duplicate catch-up, even if the winning prose differs |
| Relevant source/representation/availability movement | Revalidate; remap only where semantically sufficient; otherwise reassemble/regenerate |
| Incompatible semantic generation | Explicit affected-domain migration/reprojection; no allocator-only workaround |
| Repeated contention | Stop bounded retry and defer Story; gameplay retains priority |
| Non-monotonic authority-ref movement | Invalidate affected prepared work and enter native bounded currentness/integrity recovery |

For an indeterminate acknowledgement, inspect the current selected ref and bounded lineage/current closure under PCR-6. Current compatible coverage can prove catch-up already considered, but cannot prove that a particular editorial wording/revision was published. Editorial/structural acknowledgement requires the intended representation/write-set or a provably compatible successor closure. An ancestor commit alone proves no current semantic promise. If bounded proof is unavailable, retain `INDETERMINATE`; no blind replay and no durable Story job ID are needed.

## 16. Correction and regeneration

### 16.1 Same-ID editorial revision

When the independently addressable unit retains identity, revise the same ID under an expected-representation check. Revalidate source compatibility, availability, exactness and affected lookup/editorial metadata. Ordinary coverage is not rewound. A new body cannot inherit an old exact certification. A title-only edit still requires availability validation but does not by itself change the body bound by `exact_text_ref`.

### 16.2 Structural rewrite

A split, merge or repartition allocates fresh IDs where the old addressable units cease to exist. The draft explicitly names retirement targets and replacement keys. All inbound Story refs, reveal prerequisites and chapter memberships affected by retirement must be discovered and updated coherently.

For the cross-layer case, deterministic control constructs a transient `StoryMaintenanceSet` with required fields `exchange_schema_version`, `maintenance_ref: string`, `campaign_pin: string`, `bundles: StorySourceBundle[]`, and `drafts: StoryProjectionDraft[]`. There is exactly one bundle per affected layer and one matching draft per bundle, with at most four layers. Every bundle uses that same maintenance reference and verified campaign pin, names its own exact expected layer representation, and has operation STRUCTURAL_REWRITE. This value uses the existing exchange schema and is not a durable job, extra publication owner or mandatory ordinary-operation wrapper.

All `(bundle_ref, draft_key)` pairs are resolved together by deterministic control. A companion reference must target an actual record in this set, match its prefix-selected layer, and pass the same source/availability/closure validation as a durable target. Proposed NARRATIVE chapter members must still resolve to N IDs. Control constructs one combined write-set and checks all expected representations before a single campaign ref transition. No constituent bundle may publish separately if another is needed for reference closure. If the bounded set cannot be assembled or validated, none of it publishes.

Bounded completeness for this discovery comes from validated current forward-record/lookup closure: read the relevant layer metadata (at most the four Story layers) and targeted matching records, including editorial chapter membership. No missing/stale derived table is accepted as proof of no inbound refs. If a complete affected closure cannot fit the maintenance envelope, refuse that structural operation until a separately admitted maintenance/rebuild can establish it. Keep the old structure or exclude incompatible units from reads in the meantime; do not publish a dangling partial rewrite.

Crossref replacement is semantic/editorial work, not automatic multiplication: an old link may correctly target one replacement, several, or need removal, and reveal prerequisites must be re-derived accordingly. Existing `MUST_MATERIALIZE` obligations must remain satisfied by compatible replacement output unless their source contract lawfully ends/migrates them. Retirement cannot silently leave coverage falsely satisfied.

No universal tombstone, permalink or redirect family is introduced. A retired ID is not reused. A reader requesting it receives no automatic replacement claim without retained admissible mapping evidence. Historical Git bytes do not authorize resurrection of the retired unit. External presentation bookmarks can expire after structural regeneration.

### 16.3 Native-source correction

The native owner determines how correction affects evidence: compatible projections may remain; repairable projections regenerate; obsolete projections are retired/excluded; uncertain projections are excluded/degraded and stronger sources used. Accepted history is not silently rewritten to fit Story. A later correction can enter source enumeration after older fictional events, under stable domain ordering.

Read-time compatibility checks protect consumers before background/maintenance repair occurs. No campaign-wide pre-turn repair scan is required. A T1 Actor state change is not automatically a correction to an immutable T0 decision basis. A lower-layer wording edit does not automatically invalidate every Narrative link; structural integrity and actual native factual compatibility are checked separately.

## 17. Exactness and retention

`exact_text_ref` names the native accepted text or an owner-defined slice to which **`content.body`** claims correspondence. The exact-communication capability validates that body against currently retained native exact evidence, including a surviving source/slice digest when permitted by Step 5.11. It may calculate a candidate digest transiently; this specification creates no new stored digest or digest-generation namespace.

The message owner defines accepted text normalization, slice selection, digest and delivery semantics. Implementations must use that codec, not choose a convenient independent hash or normalize punctuation/whitespace opportunistically. Unknown exactness codecs fail closed for exact output. The default whole-message example requires no slice codec.

| Retained state | Verbatim output | Provenance / degradation |
|---|---|---|
| Native exact accepted text retained | Allowed after admission/exact verification | Message/source identity and exact basis accompany the evidence |
| Native text plus verified exact Story copy | Either valid source can supply the text | Story remains presentation, even when equality is verified |
| Raw text compacted; Story body matches surviving source exact evidence | Allowed from the verified Story body | Return `EXACT_COMMUNICATION` with `VERIFIED_STORY_COPY` representation origin |
| Story body edited and no longer matches | Edited body is not an exact quote | Use another retained exact source if present; otherwise return `NOT_RETAINED` for exact text and optionally a separately typed paraphrase |
| No exact text remains | No reconstructed quotation | Retained identity/semantic history may support a paraphrase; exact query reports `NOT_RETAINED` |
| Exact evidence was required to survive but is missing/corrupt | Do not disguise this as lawful compaction | `INTEGRITY_FAILURE` under the retention owner |

A hash alone does not contain text. A message identity alone does not establish its deleted content. Voice exactness is relative to HDM's accepted transcript, not original audio. Outbound exactness is relative to the frozen emission-committed representation and retains Step-5.12's rendering/interruption qualification. An exact communication proves the corresponding admitted communication representation, not objective truth of its proposition or literal human reading. Correctness-critical exact gameplay content remains with the proper native owner; Story alone cannot become its replacement authority. This contract adds no per-message HARD persistence edge; ordinary message/disclosure durability remains Step-5.12/native-save owned.

## 18. Chronology

Keep six orders separate: source enumeration, Story allocation, editorial reading, fictional temporal relation, causal relation, and Git/publication order. A response can order its presentation while explicitly leaving fictional order undetermined.

Temporal/causal source keys refer to owner-supported evidence. WP-15's `CAUSES`, domain-qualified `PRECEDES`, context-qualified `SAME_COORDINATE`, bounded `ELAPSED` and exact/bounded/unknown `POSITION` retain their semantics. This contract does not serialize an invented universal timestamp or infer an order from record IDs.

If two events have no established ordering, a temporal capability returns insufficient/indeterminate relation evidence as appropriate. Absence of precedence does not prove simultaneity, and a temporal relation cannot prove an Actor's motive or historical knowledge. No arbitrary graph walk is authorized to resolve the uncertainty.

## 19. Availability and disclosure boundary

Stored Story requirements are input to admission, never permanent reader grants. Context Runtime resolves current campaign access, role/purpose/subject/recipient eligibility and information/disclosure requirements; a provider performs only the owner-required checks delegated by that admitted route. Minimal internal reads needed to decide eligibility do not become role evidence.

Consumer presentation state may contain reveal anchors, focus and spoiler preference. It may restrict material further, but can never enlarge entitlement. A permissive spoiler setting cannot authorize secret Actor factors. Story body, title, participants, refs, relation labels and chapter text share whole-unit eligibility; split incompatible units instead of introducing field-level Story redaction.

Read-only Commentator output does not persist `runtime.disclosure`, change fictional knowledge or become an accepted world event. New Story cannot feed the same gameplay/Narrator envelope just because it has been generated or committed; ordinary fresh role binding and eligibility remain necessary. Existing gameplay disclosure behavior, where independently required, remains with its original owner.

## 20. Retrospective semantic read capabilities

The consumer-facing entry remains the existing registered `RoleContextRequest`. This specification does not introduce a competing role/purpose/need-profile/packet API. Context Runtime resolves that request, admits typed targets and budgets, and calls the following **internal HDM acquisition boundary**. A host facade may package these operations, but it must preserve that ownership.

The provider never decides final `ASSEMBLED`, `ASSEMBLED_DEGRADED` or `UNSATISFIABLE`. It returns evidence and acquisition limitations. Context Runtime alone decides required closure, representation downgrade, optional allocation and safe alternate behavior.

### 20.1 Capability request

| Field | Type / requirement | Owner / authority / state |
|---|---|---|
| `read_schema_version` | R positive integer, initially `1` | RetrospectiveReadCapability schema; T protocol |
| `admission_ref` | R opaque reference to the current admitted R2.3 request/binding | CR; T, not a consumer-created permission |
| `query` | R one typed variant below | Native/Story capability; T restricted query |
| `limits` | R `{max_items, max_owner_reads, max_payload_bytes}`, positive integers | CR-supplied finite acquisition limits; T, not a second token estimator |
| `basis_ref` | O existing HDM read-basis handle when continuing/reusing a compatible basis | Existing currentness owners through CR; T |
| `continuation_ref` | O opaque continuation handle; requires its matching `basis_ref` | HDM acquisition/CR; T; never access authority |

The three limits constrain returned items, native/Story owner-body acquisitions and the total serialized UTF-8 response bytes, respectively. Internal routing/index acquisition must also fit the R2.3 admitted work/metadata envelope. All work, retries and continuations charge the original registered attempt's remaining budget. A representation that cannot fit its legal floor fails within those bounds. The provider does not choose a new context estimator or silently increase a limit.

`admission_ref` resolves inside HDM to the already selected campaign/routing, approved capability/targets, required native checks, representation permissions and current admission footprint. This document deliberately does not duplicate the fields or eligibility policy owned by R2.3. A caller cannot turn an unknown handle into an admitted request. Read-only operation needs no repository write credential.

### 20.2 Closed query variants

Every query has required `kind` and exactly the corresponding fields. References are already admitted by the R2.3 binder. Arrays below are nonempty and bounded by that registration.

| `kind` | Other fields | Successful evidence kind |
|---|---|---|
| `STORY_LOOKUP` | R `story_refs: StoryRef[]` | `STORY_ORIENTATION` |
| `STORY_EDITORIAL_LOOKUP` | R `chapter_positions: nonempty unique nonnegative integer[]`, admitted through R2.3 index discovery | `STORY_EDITORIAL` |
| `STORY_NAVIGATE` | R `layer`, `order: ID_ASC or EDITORIAL`, `direction: FORWARD or BACKWARD`, `max_candidates: positive integer`; O `after: StoryRef`; O `entity_ref: EntityRef`; O `chapter_position: nonnegative integer` | `STORY_ORIENTATION` |
| `HISTORICAL_OCCURRENCE` | R `event_ref: NativeRef` | `HISTORICAL_OCCURRENCE` |
| `ACTOR_DECISION_BASIS` | R `decision_event_ref: NativeRef`, `actor_ref: EntityRef` | `ACTOR_DECISION_BASIS` |
| `COMMUNICATION` | R `message_ref: NativeRef` | `COMMUNICATION` |
| `EXACT_COMMUNICATION` | R `exact_text_ref: NativeRef`; O `story_copy_ref: StoryRef` with T prefix | `EXACT_COMMUNICATION` |
| `MECHANICAL_EVIDENCE` | R `evidence_ref: NativeRef` | `MECHANICAL_EVIDENCE` |
| `TEMPORAL_EVIDENCE` | R `anchor_refs: NativeRef[]`, `relation_kind: CAUSES or PRECEDES or SAME_COORDINATE or ELAPSED or POSITION`; O `domain_ref: NativeRef` when native relation semantics require it | `TEMPORAL_EVIDENCE` |
| `CURRENT_COMMITTED_STATE` | R `owner_ref: NativeRef` | `CURRENT_COMMITTED_STATE` |

`ID_ASC` compares numeric ID suffixes as integers, reversed by BACKWARD; lexical string order is invalid once width expands. It is never fictional chronology. `EDITORIAL` uses the NARRATIVE chapter list and explicit member order, and is legal only for NARRATIVE. Duplicate chapter appearances are deduplicated at first occurrence for that navigation window. A `chapter_position` is legal only for EDITORIAL and selects one chapter under the pinned layer metadata. `after` must resolve within the admitted window/order; an invalid/ineligible anchor is not an existence oracle. Missing editorial metadata reports insufficient orientation rather than inventing chapter order.

Navigation fixes a finite candidate window at the first call, before eligibility filtering. Later pages do not expand it. Optional entity filtering uses compact lookup only; there is no free-form predicate, recursive query language, whole-campaign eager load or implicit historical scan. Chapter metadata is filtered before use. Additional history discovery follows existing R2.3 `HISTORY_HINT`/index/explicit-ref routes; these capabilities do not create another discovery engine.

For a chronological retelling purpose, CR acquires the registered temporal dependencies of its bounded selected window. Presentation may follow established partial order and choose an editorial order among incomparable items, while preserving that uncertainty. ID navigation alone cannot establish the next event in campaign-wide fictional time. If a materially required relation is unsupported, the registered response qualifies the ordering or fails that requirement; it never invents a global temporal frontier.

### 20.3 Typed result

An available result has required `read_schema_version`, `status: AVAILABLE`, `basis_ref`, `items: EvidenceItem[]`, and `extent`; optional `projection_coverage` and `limitations`. An unavailable result has required `read_schema_version`, `status: UNAVAILABLE`, and `reason`; optional `basis_ref` only if a still-valid basis actually exists. `reason` is one code from §24. Neither form contains an assembly outcome, access grant or durable currentness flag.

`extent` is `{kind: END}` for the admitted finite query window, `{kind: MORE, continuation_ref: string}` when the same window can continue within its remaining budget, or `{kind: LIMIT}` when the registered total work/representation bound terminates acquisition. It is not campaign completeness. Non-navigation single-target native queries return END and have no pagination. Empty available items are not a factual-absence result.

Each `EvidenceItem` has required `item_key: string`, nonempty `basis_components: string[]`, `representation` from the legal R2.3 representation vocabulary, `source_refs: NativeRef[]`, and `evidence` from the following disjoint union. All are T/D values. Native payload semantics are NO; Story payload is NC; admissibility is CR-owned. Keys refer to components of the result's read basis and identify exactly which origins support the item.

| `evidence.kind` | Required payload fields | Enforced semantic restriction |
|---|---|---|
| `STORY_ORIENTATION` | `unit: StoryUnit` | Full compatible admitted unit; cannot satisfy native-fact/exact/current requirements by its presence |
| `STORY_EDITORIAL` | `chapter_position: nonnegative integer`, `chapter: Chapter` | Full admitted NARRATIVE editorial group under its exact layer basis; orientation only; no world/chapter authority |
| `HISTORICAL_OCCURRENCE` | `event_ref: NativeRef`, `value: OwnerValue` | Native SemanticEvent/history codec; no current state substitution |
| `ACTOR_DECISION_BASIS` | `decision_event_ref: NativeRef`, `actor_ref: EntityRef`, `factors: nonempty OwnerValue[]` | WP-19 T0 factor semantics associated with that Actor and event |
| `COMMUNICATION` | `message_ref: NativeRef`, `value: OwnerValue` | Admitted communication evidence; proposition truth and exact wording not implied |
| `EXACT_COMMUNICATION` | `exact_text_ref: NativeRef`, `text: string`, `origin: NATIVE_EXACT or VERIFIED_STORY_COPY`; conditional `story_ref` required for the latter | Deterministic current exact verification; body/source identity bound; representation must be EXACT |
| `MECHANICAL_EVIDENCE` | `evidence_ref: NativeRef`, `value: OwnerValue` | Native event/resolution/receipt codec; Story Mechanics cannot inhabit this variant |
| `TEMPORAL_EVIDENCE` | `relation_kind` from the query enum, `value: OwnerValue` | Native chronology codec must support that relation and domain; no guessed total order |
| `CURRENT_COMMITTED_STATE` | `owner_ref: NativeRef`, `value: OwnerValue` | Latest admitted committed native owner as checked at this response/use boundary; never T0 or unpublished HOT state |

Native `OwnerValue` alternatives are validated by the specified owner's bounded-view codec. A mismatched family/source/claim-class is an integrity/admission failure even if its JSON shape resembles another value. Receipt/query selectors remain embedded native contracts; Story serialization does not define them. Story orientation/editorial lookup returns a complete unit/group only; if its legal size cannot fit, the provider returns a bound limitation. Context Runtime may form a lawful transient summary from that admitted unit under its own representation contract; a provider cannot silently return a truncated persisted unit. Editorial lookup reads NARRATIVE layer metadata; its technical positions never become reader entitlements or public permanent chapter IDs.

`projection_coverage`, when needed and safe, is an array of required `{layer, source_domain, semantic_contract_generation, terminal_coverage, queried_source_basis, relation}`. The final field is `CAUGHT_UP`, `LAGGING` or `UNKNOWN`, derived for that source basis. The source codec supplies the comparison. No global caught-up scalar is emitted. `limitations` is an array of `{reason, item_key?}`; the optional key may address only a requested/admitted item. These are trusted internal results; §27 controls what reaches a reader.

## 21. Historical THEN, current NOW and claim discipline

An Actor's retained T0 decision basis belongs inside native SemanticEvent history. Required factors carry their native owner/family, stable subject/factor identity, recoverable event-time value or immutable evidence, provenance and association with the accepted decision. There is no separate retrospective NPC psychology archive.

Sparse capture means an unrecorded interval or omitted factor cannot be interpolated as established history. Absence of T0 support returns `INSUFFICIENT_EVIDENCE` or `NOT_RETAINED` where the owner proves lawful loss. Current beliefs/goals/relationships at T1 cannot fill that result. T0 capture remains the bounded byproduct of already-required decision work, with WP-19's zero-extra-serial capture/publication rule unchanged.

A comparison may combine an `ACTOR_DECISION_BASIS`/`HISTORICAL_OCCURRENCE` item with a separately acquired `CURRENT_COMMITTED_STATE` item. It must retain both kinds and origins. Different origins need not share an underlying commit or semantic basis. Cross-owner compatibility is still required where the requested comparison relies on a relation between them. There is no automatic historical snapshot of all Actor fields at T0.

Consumer composition must distinguish recorded/established claims, supported interpretation and speculation. Provenance must remain attached to material claims within the consumer's bounded composition contract, even if citations are hidden by normal presentation. Interpretation cannot be relabeled as recorded motive, nor a Transcript statement as objective fact. Visible provenance is itself eligibility-filtered.

This is a narrow explicit extension of the older Step-4 Commentator default: a registered retrospective purpose may ask **Context Runtime** for the named bounded native capabilities when Story is insufficient. It does not grant Commentator unrestricted WORLD/STATE or arbitrary provenance traversal. The older Story-first default remains; the explicit deep-source/debug mode remains a separate future concern. Ordinary Master retrospective uses the same evidence distinctions through its existing registration.

## 22. Basis and coherent-read model

A basis handle identifies a **transient descriptor**, not a sortable revision scalar or durable snapshot. Equal handle strings only identify the same live descriptor; unequal strings do not prove incompatibility, and equal strings do not renew eligibility. No `global_story_revision`, `global_history_revision` or global campaign currentness counter is introduced.

An HDM-internal `ReadBasis` descriptor has:

| Field | Shape / requiredness | Owner / meaning |
|---|---|---|
| `read_schema_version` | R supported read schema integer | This transient contract |
| `campaign_binding_ref` | R opaque admitted campaign-selection binding | Native campaign/routing owner via CR |
| `admission_ref` | R current request registration reference | CR; does not freeze permission forever |
| `query_ref` | R immutable binding to exact typed query, fixed window and admitted limits | CR/acquisition control; no model-authored query expansion |
| `eligibility_check_ref` | R evidence of the latest applicable eligibility evaluation | CR/disclosure owners; evaluation evidence, not lease |
| `components` | R nonempty map from component keys to `BasisComponent` | Actual dependencies used; no whole-campaign snapshot |

`BasisComponent` has required `kind: STORY_LAYER | NATIVE_HISTORY | CURRENT_COMMITTED`, `transport_pin: string`, and `representation: string`. STORY_LAYER additionally requires `layer` and `source_basis: OwnerValue` describing only the relevant layer/domain generation/coverage dependencies. The two native variants require `source_ref: NativeRef` and `owner_basis: OwnerValue` interpreted by that native owner. All component fields are T/D evidence, not new source authority. Native schemas/generations/selection rules required for interpretation are part of the owner basis and must be checked. No single token replaces them.

For Git-backed sources a transport pin identifies the admitted exact source tree/commit; Git identity proves bytes/provenance, not semantic currentness, ongoing authorization or indefinite retention. A native historical item can be loaded from a currently retained record containing T0 evidence. Historical reading does not imply selecting an arbitrary old Git commit as a resurrected source.

One page is coherent when: each item resolves against its declared representation and compatible owner contract; every Story unit/index/coverage used agrees at its layer basis; native routing chooses the right retained/published source; all material cross-source dependencies are compatible; and R2.3 admission remains valid at semantic use. A composed response need not pretend to be a simultaneous campaign-wide snapshot. If its required relationship cannot be established coherently, acquisition/assembly fails for that claim.

Before output/material use, CR revalidates the relevant currentness/eligibility footprint. Disjoint later movement need not trigger a full reread. Relevant movement needs native compatibility proof, reacquisition or failure. A confirmed publication/currentness check is evidence at the observation point, never a lease against later accepted changes.

## 23. Pagination and continuation

The baseline continuation is an opaque local handle. Its HDM-internal descriptor has required `read_schema_version`, `admission_ref`, `query_ref`, `historical_basis_ref`, `position: OwnerValue`, and `remaining_budget: OwnerValue` from the existing CR accounting contract. Position is specific to the selected Story order/window; it cannot be reinterpreted as fictional time. The remaining budget cannot be reset by asking for the next page.

For a future out-of-process transport the handle must remain integrity-protected and confidential; a signed but readable token containing hidden IDs/counts is insufficient. The baseline needs no durable cursor store or cross-chat lease. Lost/expired process state produces a bounded restart under a new admitted request, not campaign mutation.

| Movement between pages | Continuation rule |
|---|---|
| Unrelated native changes | Continue historical window if relevant components remain compatible |
| New source candidates beyond the fixed window | May continue the old finite window; new candidates require a new query |
| Append outside an ID-ordered Story window | May continue if all window/order/availability dependencies remain compatible |
| Same-ID content/source edit, structural rewrite, relevant chapter/order change | Revalidate exact window semantics; incompatible representation/order requires restart; never silently mix pages |
| Native historical correction/retention change | Revalidate through native owner; exclude/fail/restart when the historical window is no longer supported |
| Reader, entitlement, role/purpose or presentation restriction changes materially | Reject the old continuation and create a newly admitted request; do not resume at a hidden offset |
| Current native state advances | Historical continuation can survive if unaffected; NOW must be reacquired and rebound |
| Unsupported generation/schema or non-monotonic selected-ref history | Fail closed; no optimistic token translation |

Eligibility is reevaluated on **every page** even without detected movement, and again at material use where required by CR. A token never preserves a revoked grant. A source becoming ineligible is not explained by exposing its hidden identity or existence.

`CURRENT_COMMITTED_STATE` is deliberately not paginated. A THEN+NOW comparison reacquires the required NOW items when each composed response is assembled, after collecting its historical material. If several NOW owners are necessary, the existing routed currentness/closure contract must validate their compatible composition. Pages from different NOW bases cannot be aggregated under a claim that they all describe the latest state without another currentness check.

## 24. Failure and degradation

These are acquisition distinctions, not a second assembly outcome algebra. The enum is part of RetrospectiveReadCapability schema.

| Reason | Meaning / required behavior |
|---|---|
| `NOT_REQUESTED` | No acquisition was attempted; normally recorded by CR trace, not returned as a source failure |
| `PROJECTION_LAG` | Compatible layer/domain coverage is behind the relevant source basis; says nothing about occurrence absence |
| `OMITTED_BY_PROJECTION_CONTRACT` | Actual lawful omission is provable under §11; allowance to omit alone is insufficient |
| `NOT_RETAINED` | Native retention evidence proves the requested representation was lawfully not kept |
| `INSUFFICIENT_EVIDENCE` | Available admitted support does not establish the requested claim/relationship; includes unknown absence |
| `INELIGIBLE` | Material cannot enter the current role/recipient context; internal reason, sanitized under §27 |
| `STALE_BASIS` | A formerly admitted binding/window no longer establishes the current requested reliance; bounded reacquisition/restart required |
| `INCOMPATIBLE_BASIS` | Known owner/generation/representation meanings cannot be composed as requested |
| `SOURCE_UNAVAILABLE` | Provider/transport currently cannot obtain needed source evidence; not a negative fact |
| `INTEGRITY_FAILURE` | Invalid identity/reference closure, malformed required source, broken promised retention or another owner-proven integrity defect |
| `UNSUPPORTED_SCHEMA_OR_CONTRACT` | Reader lacks explicit support for a schema, generation, family, selector or capability variant |
| `BOUND_EXCEEDED` | Required acquisition/representation cannot fit the admitted finite bounds |

`AVAILABLE` is the successful result status, not a trust score. A partially successful acquisition may carry items plus limitations. CR uses the registered task contract to decide whether those missing items are required: `ASSEMBLED_DEGRADED` still meets every required semantic floor; otherwise the attempt is `UNSATISFIABLE`. The provider cannot turn a missing required T0 factor into a summary of current T1.

An unsatisfiable attempt is terminal. A caller may select its registered safe alternate under WP-09; it cannot recursively reprofile, enlarge the original scope or retry an unavailable source indefinitely. Returning a truthful qualified answer or explaining a limitation is often a valid alternate. No read failure grants write permission or activates Chronicler.

An uninitialized optional Story layer is not automatically corruption. Its absence gives no considered coverage; when the source contract proves a nonempty uncovered window it can establish PROJECTION_LAG. Otherwise the orientation remains insufficient/unknown. A missing requested ID, by itself, cannot distinguish never-created from lawfully retired. An entry claiming a required current record whose file is missing is an integrity defect. None of these cases permits inventing a tombstone, event absence or unavailable native fact.

## 25. Versioning and compatibility

| Namespace | Initial value / justification | Bump / incompatible behavior |
|---|---|---|
| StoryUnit `schema_version` | `1`; one tagged persisted envelope plus four mutually exclusive payloads | Breaking shape/interpretation requires local bump and applicable released-data migration; all layer readers use the declared supported union |
| StoryLayerProjectionState `schema_version` | `1`; separately serialized control/lookup/editorial state | Independent of unit payload evolution; preserve allocator/coverage/editorial semantics across migration |
| `exchange_schema_version` | `1`; transient SourceBundle/Draft pair can cross process/language boundaries independently of stored files | A changed exchange must have explicit paired producer/transformer support; no campaign migration solely for exchange version |
| `read_schema_version` | `1`; typed acquisition/result/basis/continuation contract is independent of file layout and producer exchange | Explicit provider/caller support; incompatible continuations expire; no implicit coercion to older evidence kinds |
| `(layer, source_domain).semantic_contract_generation` | Existing Step-5.10 namespace; domain-defined positive integer, fixture uses `1` | Change only for material projection meaning; compatible migration/reprojection/reset before reusing coverage |

Four structural namespaces are sufficient. Layer, query-kind, bundle and draft versions are not separately multiplied. No Story-wide revision, model/prompt coverage epoch, custom content digest or independent index schema is introduced.

Unknown incompatible newer structures fail closed. Additive optional changes may keep a schema version only when the version policy's compatibility conditions and actual reader support hold. Numerical equality across namespaces establishes no semantic relation. Existing external Git hashes retain their external identity semantics.

**Version Impact for this publication: NONE to existing machine/release values.** This DEV-only document specifies initial contracts; it does not change any serialized campaign, executable schema, catalog, runtime module or shipped engine value. First machine realization must conduct its own Version Impact Gate. A breaking released persistent change requiring campaign migration also bumps `campaign_contract_generation`; storage layout/marker incompatibility independently affects `storage_format_generation`. No pre-release compatibility shim is required merely to preserve an obsolete unshipped shape.

## 26. Physical topology and derived-state discipline

`MANIFEST.storage.story_root` supplies the static campaign-root-relative route. The default root is `STORY`. Layer-state and record paths remain exactly:

```text
<story_root>/<layer>/PROJECTION_STATE.yaml
<story_root>/<layer>/<minimum-three-digit floor(sequence/1000)>/<story_id>.yaml
```

For example, `E003562` routes to `STORY/EVENTS/003/E003562.yaml`; `N000001` routes to `STORY/NARRATIVE/000/N000001.yaml`. A loaded body must match the requested ID, prefix/layer and route. Shard width and ID width may expand. Shard directories hold records only. Retrospective consumers never need these physical paths.

Lookup/index/cache data derive from forward records and never contain unique campaign knowledge. Required lookup updates publish with their source records. Missing or invalid lookup means no completeness proof; authorized maintenance can rebuild it. Optional host caches may be discarded and rehydrated from admitted sources, with the same compatibility/eligibility checks as uncached reads. Cache format is not authority.

Allocator/coverage and chapter editorial data are **not** fully reconstructible generic caches. Losing them may damage idempotency, identity continuity or presentation fidelity; their repair follows Story control and surviving evidence, with no ID reuse or invented exact prose. This distinction prevents a supposed cache cleanup from silently deleting unique editorial history.

## 27. Anti-oracle and read-only guarantees

Capability results, routing tables, source coverage and continuation descriptors are internal HDM data. Context Runtime applies its existing eligibility boundary before allocating any part to a role. Error codes, item IDs, titles, source refs, counts, temporal relations and pagination metadata are subject to the same restriction as content.

For a reader who cannot know whether a protected target exists, ineligible/missing/unavailable cases use the same safe outward limitation. Do not echo a secret target, reveal that secret NPC factors exist, expose skipped-item counts or report that hidden material remains after a page. An opaque continuation may be exposed only when its existence/visible progress is itself safe; otherwise the facade returns the registered generic limitation. Full diagnostics remain restricted operator/test trace, not prompt content. Cosmetic hiding of citations is not an access-control mechanism.

The provider path performs reads and ephemeral bookkeeping only. It cannot allocate Story IDs, advance coverage, trigger mandatory materialization, publish index repairs, edit campaign/lifecycle state, or persist disclosure. All Commentator operations work with read-only campaign access. Ordinary Master's existing write authorities are neither used nor enlarged by this retrospective capability family.

## 28. Logical examples and scenario validation

### 28.1 Representative semantic read request/result

The first example is CR's internal acquisition after it has admitted a retrospective Story lookup. The same request shape serves either eligible ordinary Master or Commentator registration; the provider does not choose the role.

```json
{
  "read_schema_version": 1,
  "admission_ref": "admitted-retrospective-1",
  "query": {"kind": "STORY_LOOKUP", "story_refs": ["E000001"]},
  "limits": {"max_items": 1, "max_owner_reads": 4, "max_payload_bytes": 8192}
}
```

```json
{
  "read_schema_version": 1,
  "status": "AVAILABLE",
  "basis_ref": "read-basis-1",
  "items": [{
    "item_key": "opening",
    "basis_components": ["events"],
    "representation": "FULL_STRUCTURED",
    "source_refs": [{"family": "runtime.semantic_event", "identity": ["event-00000001"]}],
    "evidence": {
      "kind": "STORY_ORIENTATION",
      "unit": {
        "schema_version": 1,
        "story_id": "E000001",
        "content": {"title": "The gate opens", "body": "The guard opened the northern gate for the party."},
        "sources": {"event": {"ref": {"family": "runtime.semantic_event", "identity": ["event-00000001"]}}},
        "projection_basis": [{"source_domain": "campaign.semantic_events", "semantic_contract_generation": 1, "candidate_ids": ["event-00000001"]}],
        "entity_refs": [{"family": "world.actor", "identity": ["actor-0042"]}],
        "availability": {"requires_story_refs": []},
        "payload": {"event_source_keys": ["event"]}
      }
    }
  }],
  "extent": {"kind": "END"}
}
```

The handle `read-basis-1` resolves internally to this descriptor. The fixture source codec's basis value retains the domain generation and queried boundary; it is not a campaign-global frontier.

```json
{
  "read_schema_version": 1,
  "campaign_binding_ref": "selected-campaign-1",
  "admission_ref": "admitted-retrospective-1",
  "query_ref": "query-lookup-opening",
  "eligibility_check_ref": "eligibility-evaluation-1",
  "components": {
    "events": {
      "kind": "STORY_LAYER",
      "transport_pin": "published-story-pin-1",
      "representation": "events-closure-opening",
      "layer": "EVENTS",
      "source_basis": {"source_domain": "campaign.semantic_events", "semantic_contract_generation": 1, "through": "semantic-event-position-1"}
    }
  }
}
```

### 28.2 Historical escalation and separate NOW

After Story proves insufficient for the registered motive question, CR may acquire a native T0 basis; a different query obtains NOW. These are two actual typed requests, not two histories or a mandatory two-provider implementation.

```json
{
  "read_schema_version": 1,
  "admission_ref": "admitted-comparison-1",
  "query": {"kind": "ACTOR_DECISION_BASIS", "decision_event_ref": {"family": "runtime.semantic_event", "identity": ["event-00000001"]}, "actor_ref": {"family": "world.actor", "identity": ["actor-0042"]}},
  "limits": {"max_items": 1, "max_owner_reads": 4, "max_payload_bytes": 8192}
}
```

```json
{
  "read_schema_version": 1,
  "admission_ref": "admitted-comparison-1",
  "query": {"kind": "CURRENT_COMMITTED_STATE", "owner_ref": {"family": "world.actor", "identity": ["actor-0042"]}},
  "limits": {"max_items": 1, "max_owner_reads": 4, "max_payload_bytes": 8192}
}
```

The first successful item must be `ACTOR_DECISION_BASIS` with WP-19-valid native factors; the second must be `CURRENT_COMMITTED_STATE`. In the fixture, a retained T0 goal to admit the party and a current T1 goal to keep the gate closed can both be valid. The native basis carries the actual factor identities, values and provenance. The consumer cannot infer missing factors or rewrite T0 from T1.

### 28.3 Failure and continuation

This internal failure contains no invented factual absence and no partial required payload:

```json
{
  "read_schema_version": 1,
  "status": "UNAVAILABLE",
  "reason": "SOURCE_UNAVAILABLE"
}
```

This continuation descriptor is held by HDM behind an opaque `continuation_ref`. `remaining_budget` is an example of CR's accounting value; it is neither a new budget owner nor data that the model may replenish.

```json
{
  "read_schema_version": 1,
  "admission_ref": "admitted-navigation-1",
  "query_ref": "query-events-window-1",
  "historical_basis_ref": "navigation-basis-1",
  "position": {"order": "ID_ASC", "last_examined": "E000001", "window_last": "E000002"},
  "remaining_budget": {"owner_reads": 4, "payload_bytes": 16384}
}
```

A matching continuation request preserves the query and does not exceed the remaining admitted budget:

```json
{
  "read_schema_version": 1,
  "admission_ref": "admitted-navigation-1",
  "query": {"kind": "STORY_NAVIGATE", "layer": "EVENTS", "order": "ID_ASC", "direction": "FORWARD", "max_candidates": 2},
  "limits": {"max_items": 1, "max_owner_reads": 2, "max_payload_bytes": 8192},
  "basis_ref": "navigation-basis-1",
  "continuation_ref": "opaque-continuation-1"
}
```

### 28.4 Required end-to-end scenarios

These are design/scenario acceptance specifications, **not executed runtime test results**. Each row states the required observable outcome and boundary that must eventually be verified.

| # | Scenario | Required outcome / verification target |
|---|---|---|
| 1 | Normal EVENTS materialization | §12 bundle → §13 draft → deterministic E000001 allocation → record plus lookup/high-water/coverage publish atomically; only then readable |
| 2 | EVENTS caught up, NARRATIVE lags | Independent typed coverage; native/Events reads proceed; no rollback or global caught-up claim |
| 3 | Exact Transcript retained | Exact capability validates native accepted text and emits EXACT_COMMUNICATION; statement truth remains separate |
| 4 | Original payload compacted, verified Story copy remains | Surviving message identity/exact evidence validates the copy; return exact text with VERIFIED_STORY_COPY origin |
| 5 | Transcript body edited | Old exactness does not survive mismatch; reacquire native exact text or report NOT_RETAINED; paraphrase stays separately typed |
| 6 | Same-ID editorial revision | Expected representation checked; ID unchanged; availability/exactness/index revalidated; coverage normally unchanged |
| 7 | Structural split | Fresh replacement IDs, contributions retain source candidate; all inbound refs/reveal/chapter entries updated in one bounded closure |
| 8 | Structural merge | Fresh merged ID and combined native provenance; retirement updates all affected closure; no ID reuse or automatic universal redirect |
| 9 | Current Actor T1 differs from historical T0 | ACTOR_DECISION_BASIS resolves retained event-time factors; T1 cannot fill missing historical support |
| 10 | Story insufficient; native escalation needed | CR names the registered unresolved dependency and finite native query; provider returns proper evidence kind; CR alone assembles |
| 11 | THEN compared with latest committed NOW | Separately typed/bound components; current NOW reacquired before composed use; no fabricated common snapshot |
| 12 | Events have no total temporal order | Preserve partial/incomparable relation; no ordering from IDs, Git, page or prose order |
| 13 | Story exists, reader ineligible | No unit/metadata allocated; outward result does not reveal protected existence, ID or counts |
| 14 | Story projection absent, native evidence exists | Relative lag/unknown orientation; native history remains queryable if admitted; absence does not deny occurrence |
| 15 | Source temporarily unavailable | SOURCE_UNAVAILABLE; finite registered fallback or unsatisfiable attempt; no inferred absence or unbounded retry |
| 16 | Unsupported newer schema/generation | Fail closed at relevant codec; no reinterpretation, silent downgrade or stale coverage inheritance |
| 17 | Reader eligibility changes between pages | Reevaluate, invalidate old continuation, admit a new request; no preserved old grant or secret offset leak |
| 18 | Current source moves during pagination | Compatible fixed historical window can continue; NOW is reacquired; relevant historical/order change requires restart |
| 19 | Commentator has no campaign write permission | Every read/pagination/fallback works without writes, catch-up, persisted repair or disclosure mutation |
| 20 | Ordinary Master retrospective | Same capability variants under ordinary Master registration and player/PC eligibility; no Commentator mode switch or alternate history owner |

Additional adversarial obligations: conflicting source generation during allocation, ambiguous acknowledgement after a competing writer, same-ID correction after lost acknowledgement, missing inbound-ref index during split, hidden chapter title leakage, a receipt falsely packaged as occurrence/current state, and a structurally valid but unsupported literary inference. Their dispositions are §§14–17, 20 and 24–27; none may be treated as gameplay authority.

## 29. Machine-realization obligations and decision record

### 29.1 Classification

| Class | Required disposition |
|---|---|
| A — Already accepted architecture, not yet fully machine-realized | Story scaffold/static manifest selector; layer IDs/coverage/publication; Step-5.11 message/exact-retention codecs; R2.3 bounded assembly; WP-19 T0 SemanticEvent factors and ordinary retrospective binding. WP-18 final recovery item 10 provenance is already realized; obligations 1–9 and 11–13 remain substantive implementation later. |
| B — New concrete realization specified here | StoryUnit/state validation and serialization; transient bundle/draft union and deterministic remapping; exact lookup projection; correction closure; typed read/result/basis/continuation validation and owner-specific adapters. Values and behaviors are specified here; executable validators/runtime are not delivered by this document. |
| C — Downstream adapter work | Map consumer controls to registered R2.3 purposes, translate typed evidence while preserving provenance/claim kinds, implement ephemeral continuation handling and currentness reacquisition, remove assumptions of a global frontier/single history basis. Adapt existing consumer APIs when necessary; their present class names do not constrain HDM. |
| D — Optional optimization | In-process hydration/cache, faster derived source/inbound-ref lookup, deterministic projection instead of LLM, batching physical reads. Must be semantically transparent and rebuildable. |
| E — Dormant future work | Index partitioning only on existing measured-scale/tool-limit trigger; external transport only with a concrete deployment need; asynchronous workers only under existing projection law; explicit deep-source/debug consumer mode only under its own admission decision. No default activation. |

Machine implementations must validate the schemas and owner codecs, enforce the negative union/type rules, and exercise §28 plus publication/concurrency/retention/integrity paths. Scenario design is not executable verification, and deterministic validation is not empirical narrative-quality acceptance. No surrogate runtime or model-quality PASS is claimed here. Broad performance claims remain unmeasured; the design guarantees explicit work bounds and truthful failure, not a fabricated latency figure.

### 29.2 Material integration decisions

| Decision | Classification relative to existing owners | Consequence |
|---|---|---|
| One prefix-derived Story identity; four payloads | REALIZES Step 4/5.10 | Minimal persisted identity; layer mismatch becomes mechanically invalid |
| Layer state contains coverage, compact lookup and optional editorial chapters | REALIZES Step 5.10/WP-11 | No extra topology; one layer-state compatibility boundary; metadata remains monolithic |
| Native-ref routing envelope with owner-specific selectors/bases | REALIZES R2.1/WP-10/WP-19 | No universal historical ontology; native codec work stays explicitly owned |
| Typed capabilities below Context Runtime | EXTENDS integration, preserves R2.3 authority | A provider cannot decide assembly/eligibility policy or collapse evidence kinds |
| Narrow registered native escalation for Commentator | EXTENDS older Step-4 default consumer edge under this task's accepted retrospective requirements | Story-first retained; no unrestricted WORLD/STATE or direct role-to-role protocol |
| Transient multi-component basis and protected continuation | REALIZES currentness composition and EXTENDS concrete read protocol | No durable global snapshot; permission and NOW are rechecked |
| Internal detailed failures plus reader-safe projection | REALIZES existing disclosure/CR constraints | Debuggability without a source-existence oracle |

These decisions do not supersede the listed semantic owners or reopen their settled product laws. New native families, universal scans, different retention promises or any ownership transfer would require an explicit separately justified architecture decision.

### 29.3 Risks, confidence and reopen triggers

| Risk / uncertainty | Mitigation / revisit trigger |
|---|---|
| Monolithic layer metadata may reach an operational host limit | Use existing finite envelopes; exact reads remain direct; measure under WP-24 before introducing partitioning |
| Native codec realization may be incomplete | Fail the specific unsupported capability; owner-specific codecs are an explicit implementation obligation, not a guessed default |
| Cross-layer structural rewrite may exceed bounded closure | Keep existing structure/exclude incompatible units; authorize scoped maintenance only after completeness can be proved |
| Generated prose may be wrong despite structural validity | Noncanonical status, typed native escalation, repair lifecycle and later behavioral/empirical evaluation |
| Historical exact/editorial fidelity may be lost after lawful compaction or destructive loss | Preserve only existing retention promises; no regeneration claim without surviving evidence |

Recommendation confidence is high for ownership/semantic boundaries. Implementation cost and large-campaign performance are not measured. Revisit the selected design if a real registered consumer cannot obtain its required finite evidence without global scanning, if native owners cannot supply a compatible bounded basis, or if a new product promise requires perpetual exact history. Do not weaken ownership/type guarantees merely to fit a current consumer API.

**Product Owner decision required: NO.** No new material product trade-off remains within this contract's stated scope. Native codec/storage details can be realized under their existing owners. Independent review and future implementation authorization remain governed by the existing program process; this document changes neither global stage state nor those gates.

## 30. Explicit non-goals and completion boundary

No second truth authority, Context Runtime, native history owner or generic memory database is introduced. There is no mandatory RAG/vector subsystem, universal query/graph traversal, global Story revision, global fictional chronology, durable projection queue/lease/worker registry, mandatory Chronicler LLM or Commentator write capability. Public contracts have no private consumer-runtime dependency.

The delivered artifact is this integration specification and its navigation reference. Story machine/runtime implementation and downstream adaptation are subsequent independent work, after their applicable gates. The document provides schemas, concrete logical exchanges, lifecycle/failure rules and scenario obligations needed to begin that work without redefining the fundamental producer/persistence/read boundaries.
