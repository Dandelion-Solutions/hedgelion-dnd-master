# Story / Commentator Self-Contained Historical Corpus — Product Owner Decision

Status: **OWNER-APPROVED PRODUCT / CONSUMER SEMANTICS — IMPLEMENTATION NOT ACTIVATED**

Date: 2026-09-09

## 1. Purpose and relationship to existing architecture

This decision fixes a newly explicit Commentator consumer requirement over the already accepted Story, historical Actor-basis and information-eligibility architecture.

It supplements and, only where stated below, supersedes parts of:

- `2026-09-05-hdm-historical-actor-decision-basis-owner-decision.md`;
- `2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-canonical-spec.md`;
- `2026-09-07-story-producer-persistence-retrospective-consumer-contract.md`;
- `2026-09-08-story-baseline-projection-source-contracts.md`;
- `2026-09-08-story-persistence-growth-sharding-consumer-decoupling-owner-decision.md`.

The current Step-4 truth / knowledge / disclosure owners, R2.3 bounded-context principles, Story non-authority relative to gameplay truth, and WP-19 bounded historical Actor decision-basis owner remain intact.

This decision does **not** activate runtime implementation, Story schema implementation, Commentator cache implementation, a new roadmap stage, WP-26, implementation planning or gameplay bootstrap.

## 2. Product model

For baseline Commentator operation, the imported Story corpus is the Commentator's **local factual canon**: the closed factual-support surface from which Commentator may state established historical claims.

This term is consumer-scoped. It does not promote Story into HDM gameplay canon, current world authority, mechanical authority, SAVE/recovery authority or a writable history owner.

The distinction is:

```text
HDM gameplay / Master
    current native owners remain authoritative
    Story remains durable noncanonical projection

Commentator
    Story corpus + its Commentator eligibility/control projection
    form the complete baseline factual-support universe
```

If a claim is not established by that Commentator corpus at the applicable basis, Commentator must qualify it as unsupported/insufficient rather than silently consulting unrestricted Master-native truth or reconstructing it from current state.

## 3. Commentator cache is not HDM HOT

Any local database/cache used by a Commentator implementation is a downstream consumer read model. Its physical schema, tables, indexes, search representation, embeddings, navigation structures, compaction and lifecycle are not HDM HOT/SQLite semantics and are not owned by WP-12.

A campaign may therefore have separate local environments, for example:

```text
campaign X
    Commentator read cache
        optimized for history/navigation/search/retelling

    Master HOT/runtime cache
        optimized for current gameplay/mechanics/runtime work
```

No format, table or migration compatibility between these two local stores is required.

A user may enter a campaign read-only through Commentator and later gain gameplay participation authority. That role/entry change does not convert the Commentator cache into Master HOT or make it gameplay authority. Normal Master hydration/currentness rules establish the gameplay working environment separately.

This public contract remains storage-topology-neutral: no particular Commentator SQL schema, database file, table family or indexing algorithm is prescribed here.

## 4. Historical Actor decision basis must be Story-self-contained

PO-003 and WP-19 already require sparse, bounded event-time Actor decision basis for qualifying material decisions or cognitive transitions.

That retained basis may include the situation-specific subset of then-current:

- knowledge / belief / suspicion / rejection state;
- goals / objectives / intentions / commitments;
- directed relationship facets;
- relevant resources / constraints / circumstances;
- causal/source event or fact references;
- other admitted Actor-private factors that materially affected the decision.

The existing negative boundaries remain:

```text
NO full NPC-psychology history
NO per-turn full Actor snapshots
NO hidden chain-of-thought retention
NO raw prompt/reasoning retention
NO T1-current-state substitution for missing T0 evidence
```

### LAW SCC-1 — Required retained T0 basis enters the Story corpus

When WP-19 requires a bounded T0 decision basis for an accepted material Actor decision/transition, Story projection must preserve the retained material factor set in a Story-local recoverable representation.

A native reference that merely points outside the Story corpus is not sufficient discharge for this Commentator requirement.

### LAW SCC-2 — EVENTS carries structured recoverable basis

For a qualifying SemanticEvent, the EVENTS representation must contain or Story-locally bind the complete retained bounded T0 factor set needed to recover the accepted historical decision basis, including factor identity, event-time value/stance or equivalent immutable recoverable meaning, provenance/source binding and availability classification.

The exact persisted field layout and schema version are downstream realization decisions.

### LAW SCC-3 — NARRATIVE remains readable without native escalation

NARRATIVE must preserve the readable historical/causal account of the qualifying decision. It need not duplicate every structured factor field when the required detailed basis is available through a valid Story-local EVENTS/cross-reference path.

It may not require a native-only lookup to recover a T0 factor that the baseline Commentator product promises to use.

### LAW SCC-4 — Private/off-screen basis is retained, not omitted

A T0 factor does not become optional merely because it is secret, private, NPC-local, off-screen or unavailable to a current reader.

Required historical material remains in the comprehensive Story corpus with correct protection metadata. Reader eligibility controls use, not projection existence.

## 5. Supersession of the earlier T0 projection allowance

The following earlier Story baseline allowance is superseded for WP-19-required T0 factors:

> retaining only navigation to native decision-basis evidence while omitting the retained material factor values from the Story corpus.

Specifically, the `2026-09-08-story-baseline-projection-source-contracts.md` E-EVT statement that Story need not duplicate all private T0 factor values, and the N-EVT statement that detailed T0 evidence may remain behind native navigation refs, no longer satisfy baseline Commentator self-containment for factors retained under WP-19.

The intended replacement is:

```text
native SemanticEvent owns historical evidence
    -> Story projection copies a bounded source-bound representation
    -> Commentator corpus can answer from Story alone
```

Native ownership remains unchanged. Projection is not authority transfer.

## 6. Commentator eligibility/control projection

Story-unit `availability` requirements alone are insufficient for an autonomous Commentator read model when resolving them would require live reads from Master-native knowledge/disclosure/access owners.

A Commentator-importable campaign snapshot must therefore include a **self-contained eligibility/control projection** sufficient to evaluate the supported Commentator information boundary at its declared basis.

The exact physical representation may be embedded in Story control metadata or supplied as a companion persisted projection. This decision does not choose that storage shape.

### LAW SCC-5 — Eligibility projection is derived, comprehensive and secret-bearing

The projection may contain protected information needed to decide access. It may include, as required by current HDM information owners:

- campaign readability/visibility and relevant principal/binding facts;
- current player/PC/recipient relationships needed by Commentator admission;
- relevant `world.knowledge` relations;
- relevant `runtime.disclosure` relations;
- Story availability/reveal prerequisites;
- other narrowly required information-owner values needed to apply the current Commentator no-spoiler/eligibility contract.

It may contain information unavailable to the current reader. Physical possession by the trusted Commentator cache is not permission to expose it.

### LAW SCC-6 — No second ACL or knowledge authority

The eligibility/control projection is a source-bound derived projection of existing HDM owners. It does not become:

- a second `world.knowledge` owner;
- a second `runtime.disclosure` owner;
- a gameplay access-control authority;
- a mutable permission database independent of campaign owners;
- a mechanism for Commentator to grant itself broader access.

The owning HDM state determines the projection when it is produced. Commentator deterministically enforces the imported projection and may narrow it further for spoiler preference, but never widen it.

### LAW SCC-7 — Story availability must be locally decidable for baseline Commentator use

For every Story item admitted into the baseline Commentator corpus, the imported snapshot must contain enough eligibility/control information to determine whether that item, its title/body, relevant refs, protected factors and navigation metadata may enter the current Commentator retrieval bundle.

A baseline Commentator request must not require Master HOT or arbitrary native owner acquisition solely to decide that Story item's visibility.

If the required eligibility state is absent, incompatible or unsupported, fail closed for the affected material. Do not interpret missing control data as permission.

### LAW SCC-8 — Anti-oracle protection applies before LLM materialization

The deterministic Commentator filter must protect not only prose but also IDs, titles, entity associations, counts, chapter membership, relation labels, T0 factors, search hits and pagination/navigation metadata whose existence is itself ineligible.

Protected material may exist in the local comprehensive cache while remaining absent from the LLM-visible retrieval bundle.

## 7. Content basis and access basis are independent

The Commentator snapshot has two logically distinct currentness concerns:

```text
CONTENT BASIS
    Story/history representation and content completeness

ELIGIBILITY / CONTROL BASIS
    current readable/access/knowledge/disclosure state used to filter it
```

They may share one transport revision when produced together, but they are not the same semantic frontier.

### LAW SCC-9 — CONTENT_FINAL does not mean ACCESS_FINAL

A campaign becoming content-final may stop future content catch-up when the applicable lifecycle/content owner proves no further Story content can arrive.

It does not freeze campaign readability, principal bindings, knowledge/disclosure control state or other access-relevant information by implication.

Access/control changes may therefore require a refreshed Commentator eligibility projection even when Story content itself is final and unchanged.

### LAW SCC-10 — Local cache generations may reuse immutable content with refreshed control

A downstream Commentator implementation may retain the same imported content generation while rebuilding or replacing its local control/eligibility generation from a newer compatible projection.

This is consumer cache behavior, not a new HDM global revision or mixed gameplay snapshot authority.

## 8. Native escalation boundary after this decision

The existing retrospective native evidence capabilities remain valid for owners/consumers that require them, including ordinary Master retrospective use, implementation diagnostics, maintenance, or a separately authorized future deep-source mode.

They are no longer a required baseline dependency for Commentator claims that this decision requires the Story corpus to preserve.

In particular:

```text
baseline Commentator historical decision explanation
    MUST NOT depend on native-only ACTOR_DECISION_BASIS retrieval
    when the qualifying WP-19 basis was retained
```

Projection-time Story production may and should read the admitted native evidence necessary to build the self-contained Story representation. The prohibition is against making baseline Commentator use depend on a second Master-native retrieval path after import.

## 9. Completeness and failure semantics

A Commentator snapshot/corpus is ready for a supported use only when:

1. the required Story content is present at a compatible content basis;
2. required WP-19 T0 factors are Story-locally recoverable for qualifying material decisions;
3. the required Commentator eligibility/control projection is present at a compatible control basis;
4. protected material can be deterministically filtered before LLM exposure;
5. provenance/availability distinctions remain intact.

A Story coverage claim for a qualifying event must not treat a native-only T0 pointer as full Commentator materialization after this decision.

If the corpus lacks support for an exact motive, exact communication, mechanical detail or other claim outside the admitted Story promise, Commentator reports the limitation rather than inventing or reaching into unrestricted current Master state.

## 10. Storage, sharding and implementation neutrality

The existing Story growth/sharding decision remains controlling.

This decision does not require one monolithic Story snapshot file, one SQL file, one eligibility file or one physical partition. Any persisted projection introduced by realization must remain bounded/partitionable under existing GitHub mutable-artifact and Story sharding laws.

A downstream Commentator cache may freely reorganize the imported corpus for fast search/navigation/retelling as long as:

- the transformation is deterministic/rebuildable from admitted snapshot input;
- source/availability semantics are preserved;
- filtering occurs before LLM materialization;
- local cache structure does not become HDM authority.

Later Story repartitioning must remain transparent to the Commentator semantic contract.

## 11. Downstream architecture / realization obligations

When Story/Chronicler/retrospective realization is next designed or implemented, its Source Manifest must include this decision.

That work must determine the minimum concrete machine representation for:

1. Story-local structured T0 decision-basis evidence;
2. Story-local linkage from NARRATIVE to required structured EVENTS evidence where used;
3. a versioned self-contained Commentator eligibility/control projection;
4. content-basis vs control-basis currentness and refresh rules;
5. deterministic anti-oracle filtering before Commentator LLM materialization;
6. bounded/sharded persistence under current Story storage constraints;
7. tests proving that secret material may be cached comprehensively but cannot leak to an ineligible retrieval bundle;
8. tests proving that a retained historical Actor basis remains explainable after current Actor T1 has changed, without native fallback.

No new Story layer, generic history database, global ACL registry, global currentness scalar or Master/Commentator shared SQLite schema is implied.

## 12. Version and current-stage impact

```text
VERSION_IMPACT: NONE FOR THIS DOCUMENT-ONLY OWNER DECISION
```

No currently implemented Story schema, projection schema, storage generation, engine version or runtime module is changed by publishing this decision.

Future realization that changes a persisted StoryUnit shape or introduces a new persisted Commentator control-projection schema must perform its own Version Impact Gate. The current pre-release clean-slate policy permits replacement when accepted architecture requires it; this decision itself performs no migration.

`DEV/CURRENT_PROGRESS.md` is unchanged. WP-26 remains unauthorized until its separate explicit stage-entry gate. This decision records a cross-cutting product/consumer requirement and does not activate the next numbered architecture stage.
