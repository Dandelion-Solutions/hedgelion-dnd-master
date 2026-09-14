# Implementation Planning — Lossless Proof Ledger v3

Status: **CURRENT POST-GRAPH PROOF ROUTE — PLANNING ONLY**
Date: 2026-09-14
Finding origin: **AUTHOR FINDING 20 — SIGNIFICANT**, extended through Finding 24.

Historical readiness/proof semantics remain in v2 and its appendices. This v3 adds the mandatory post-graph joins; it creates no readiness IDs. Exact executable witnesses and primary proof channels are defined by `2026-09-14-implementation-planning-post-graph-proof-witness-matrix.md` and are part of this ledger's closure condition.

## R018 current closure

The historical R018 slices remain required, but closure now also requires:

- RD-15 `runtime.catalog_gap_report` family schema/route/producer/publication/recovery witness;
- RD-16 exact 17-world-family schema/route/identity matrix;
- RD-16 final shared catalog/identifier integration.

`CompositeR018ProofTests` may close only after `R018WorldFamilyProofTests` and the RD-15 catalog-gap family witness are green. Exact 17-world and 17-runtime members are checked item-by-item; count-only proof is invalid. `world.faction` must be absent as an independent family.

Findings 23–24 add embedded accepted-execution/LIVE identity evidence and do not add native families; the 17+17 census therefore remains unchanged.

## Post-WP27 proof rows

These are proof obligations, not readiness identities:

- PG06 temporal completeness routing -> RD-08 routing tests + RD-06/RD-09 publication joins + RD-07 recovery reconstruction.
- PG07 WP-16 additive/live-birth/multi-LIVE closure -> current amended WP-16 witnesses.
- PG08 player/faction/thread reconciliation -> RD-16 family census/no-faction proof.
- PG09 bounded principal route -> exact nomination + owner-reload tests.
- PG10 MechanicalEvent composite identity -> RD-05 identity + RD-16 policy integration.
- PG11 catalog runtime binding/gap evidence -> RD-15 full seam tests.
- PG12 strict world schemas/closed dispatch -> RD-16 schema/dispatch tests.
- PG13 shared catalog/identity writer closure -> RD-16 shared integration tests.
- PG14 shipped catalog-binding consumer cutover -> RD-15 instruction tests.
- PG15 current package routing -> static package-router proof.
- PG16 one native `world.player` record key -> RD-16 native-record proof.
- PG17 RD-15/RD-16 checkpoint coherence -> checkpoint static proof plus full discovery at every future checkpoint.
- PG18 RD-15 validated binding required by catalog-backed RD-05 acceptance -> integration seam tests.
- PG19 current 16-RD bidirectional coverage -> coverage/currentness static proof.
- PG20 current proof routing -> static proof that R018 requires RD-15/RD-16 and every post-WP27 mechanism row is routed.
- PG21 current execution graph -> static acyclicity and RD-01..RD-16 dependency/join proof.
- PG23 reconstructive accepted catalog basis -> RD-15 exact basis producer/session-only guard + RD-05 accepted carrier equality + RD-06 retention/publication join + RD-07 exact reconstruction/no-ambient-rebind proof.
- PG24 exact source-native LIVE identity -> RD-09 stable source key/ordinal/encoding + same-CAS allocation/ambiguity handling + RD-16 shared policy integration + RD-07 selected-LIVE recovery validation.

`PG22` is deliberately not a second semantic mechanism row. Finding 22 is the exact-witness routing rule embodied by the mandatory witness matrix. `PostGraphProofRoutingTests` closes that meta-obligation only when every semantic PG row has a named executable/static witness and primary channel.

A named test without the corresponding executable mechanism is RED. A mechanism without its named current proof route is also RED.

## PG23 exact closure law

PG23 cannot close from fingerprint equality alone.

Closure requires all of:

1. one typed reconstructive `CatalogContextBasis` contract containing exact ruleset-set identity, catalog-context fingerprint identity and bounded owner-local campaign/session definition dependency refs;
2. RD-15 deterministic construction of that basis from one exact logical `ResolvedCatalogContext`;
3. RD-15 rejection/blocking of durable `SUPPORTED` binding when a material session-only definition lacks owner-approved durable publication/promotion basis;
4. RuntimeCommand persistence of that exact basis for catalog-backed accepted execution;
5. Resolution and Continuation exact-basis equality with the root accepted command;
6. `runtime.catalog_gap_report` retention of the exact basis in which deterministic unsupported validation occurred;
7. RD-06 correctness-required durability/protection evidence proving required owner-local definition sources cannot be stranded by accepted unsettled execution;
8. RD-07 reconstruction of the exact accepted ruleset set and owner-local definition dependencies before retry/resume;
9. typed block/compatibility/integrity failure on missing, incompatible, unpinned or mismatched dependencies;
10. explicit negative proof that current/latest/search/model-memory rebinding and silent definition-ID rewrite/promotion are forbidden.

Primary witnesses:

- RD-15 `CatalogContextBasisContractTests` and `CatalogGapContextEvidenceTests`;
- RD-05 `AcceptedExecutionCatalogBasisTests`;
- RD-06 `CatalogDependencyDurabilityTests`;
- RD-07 `CatalogBasisRecoveryTests`.

## PG24 exact closure law

PG24 cannot close from the semantic phrase "epoch-qualified source-native ID" alone. Worker-visible machine realization must be exact.

Closure requires all of:

1. stable `LiveSourceKey = (campaign_technical_id, scene_id, epoch_id)`; mutable transport refs, exact source revisions, clocks, hosts and sessions are excluded from semantic identity;
2. one persisted `uint64 next_source_native_creation_ordinal` per LIVE source, initialized to 1, never wrapped/reused, and used only as uniqueness allocation state rather than chronology/currentness/priority;
3. exact injective `framed_base32hex_v1` encoding over length-framed stable source key + native family + accepted source-local ordinal, with the family's final identifier-policy prefix;
4. the final canonical IDs, all transition-internal references to them and the cursor advance are established by the same accepted exact-source CAS as creation;
5. confirmed stale/rejected prospective IDs are noncanonical and a retry rereads the current cursor;
6. `INDETERMINATE` publication reconciles the original frozen allocation/lineage before any new coordinate/ID may be allocated;
7. accepted source-native IDs never rekey merely because LIVE later closes/absorbs into campaign;
8. legacy generic `provisional_id -> compaction rekey` semantics are not the baseline representation for current `SOURCE_NATIVE_LIVE` families;
9. RD-16's one shared identifier-policy write records the closed `source_native_live` + `framed_base32hex_v1` disposition and does not apply it to owner-equivalent/composite/forbidden families;
10. RD-07 selected-LIVE recovery validates exact source-native IDs/cursor from the selected exact source and cannot use campaign allocator, directory/index ordering or latest-looking branches as reconstruction authority.

Primary witnesses:

- RD-09 `SourceNativeLiveIdEncodingTests`;
- RD-09 `LiveSourceCreationCursorTests`;
- RD-09 `SourceNativeAmbiguousPublicationTests`;
- RD-09 `LiveSourceNativeSchemaCutoverTests`;
- RD-16 `SourceNativeIdentifierPolicyIntegrationTests`;
- RD-07 `SourceNativeLiveRecoveryTests`.

## Current proof law

Current proof routing requires:

1. v2 historical readiness rows/appendices as provenance;
2. this v3 post-graph override;
3. the current WP-16 proof amendment;
4. the current exact witness matrix;
5. coverage v3 and execution-wave v2 currentness agreement.

Behavioral obligations require behavioral/integration proof; static evidence cannot substitute. Package/currentness obligations may use static proof where no runtime behavior is implicated. Deferred empirical rows remain dormant until their owner-defined trigger fires.

Final author closure additionally requires proof-ledger v3, witness matrix, coverage v3 and execution-wave v2 to agree on RD count, exact family census, overlay routing and all post-WP27 atoms through the latest author finding, followed by exact-head maintenance audit, full DEV discovery, hosted CI and independent Senior review.

Production implementation remains unauthorized.
