# Implementation Planning — Lossless Proof Ledger v3

Status: **CURRENT POST-GRAPH PROOF ROUTE — PLANNING ONLY**
Date: 2026-09-14
Finding origin: **AUTHOR FINDING 20 — SIGNIFICANT**, extended through Finding 26, with F58/PG35 operational-root and F59/PG36 access-policy integration.

Historical readiness/proof semantics remain in v2 and its appendices. This v3 adds the mandatory post-graph joins; it creates no readiness IDs. Exact executable witnesses and primary proof channels are defined by `2026-09-14-implementation-planning-post-graph-proof-witness-matrix.md` and are part of this ledger's closure condition.

## R018 current closure

The historical R018 slices remain required, but closure now also requires:

- RD-15 `runtime.catalog_gap_report` family schema/route/producer/publication/recovery witness;
- RD-16 exact 17-world-family schema/route/identity matrix;
- RD-16 final shared catalog/identifier integration.

`CompositeR018ProofTests` may close only after `R018WorldFamilyProofTests` and the RD-15 catalog-gap family witness are green. Exact 17-world and 17-runtime members are checked item-by-item; count-only proof is invalid. `world.faction` must be absent as an independent family.

Findings 23–26 add embedded accepted-execution/LIVE identity/routing/allocation evidence and do not add native families; the 17+17 census therefore remains unchanged.

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
- PG24 source-native LIVE cursor/printable-ID realization -> RD-09 exact cursor/encoding/CAS + RD-16 shared policy integration + RD-07 selected-LIVE recovery; PG25/PG26 supply the corrected campaign source key and deterministic multi-creation allocation order.
- PG25 LIVE campaign semantic-identity / physical-route separation -> RD-14 exact `campaign_id` creation projection + RD-06 identity immutability + RD-09 derived bounded route token/body validation/corrected ID frame + RD-07 selected-LIVE campaign identity recovery.
- PG26 deterministic attempt-local source-native creation order -> RD-09 per-family owner-order normalization + exact slot/ordinal allocation + original frozen-attempt ambiguity handling + RD-07 accepted allocation recovery.

- PG35 F58 operational-root enrollment/publication/recovery -> RD-05 native producer + RD-07 active-only contract and complete cold hydration + RD-06 campaign closure + RD-09 current LIVE handoff + RD-14 generated scaffold + F41/F47/F46 final integrated projections.

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

PG24 cannot close from the semantic phrase "epoch-qualified source-native ID" alone. Worker-visible machine realization must be exact and is refined by PG25/PG26.

Closure requires all of:

1. stable semantic `LiveSourceKey = (campaign_id, scene_id, epoch_id)` under PG25; mutable transport refs, physical campaign-route tokens, exact source revisions, clocks, hosts and sessions are excluded from semantic identity;
2. one persisted `uint64 next_source_native_creation_ordinal` per LIVE source, initialized to 1, never wrapped/reused, and used only as uniqueness allocation state rather than chronology/currentness/priority;
3. exact injective `framed_base32hex_v1` encoding over length-framed canonical semantic source key + native family + accepted source-local ordinal, with the family's final identifier-policy prefix;
4. when one attempt creates multiple SOURCE_NATIVE_LIVE records, PG26 supplies the exact normalized slot order used to map the frozen cursor to individual ordinals;
5. final canonical IDs, all transition-internal references to them, exact allocation evidence and the cursor advance are established by the same accepted exact-source CAS as creation;
6. confirmed stale/rejected prospective IDs are noncanonical and a refreshed attempt rereads the current cursor;
7. `INDETERMINATE` publication reconciles the original frozen allocation/lineage before any new coordinate/ID may be allocated;
8. accepted source-native IDs never rekey merely because LIVE later closes/absorbs into campaign;
9. legacy generic `provisional_id -> compaction rekey` semantics are not the baseline representation for current `SOURCE_NATIVE_LIVE` families;
10. RD-16's one shared identifier-policy write records the closed `source_native_live` + `framed_base32hex_v1` disposition and does not apply it to owner-equivalent/composite/forbidden families;
11. RD-07 selected-LIVE recovery validates exact source-native IDs/cursor/allocation from the selected exact source and cannot use campaign allocator, directory/index ordering or latest-looking branches as reconstruction authority.

Primary witnesses:

- RD-09 `SourceNativeLiveIdEncodingTests`;
- RD-09 `LiveSourceCreationCursorTests`;
- RD-09 `SourceNativeAmbiguousPublicationTests`;
- RD-09 `LiveSourceNativeSchemaCutoverTests`;
- RD-16 `SourceNativeIdentifierPolicyIntegrationTests`;
- RD-07 `SourceNativeLiveRecoveryTests`.

## PG25 exact closure law

PG25 closes only when semantic campaign identity and physical LIVE routing are mechanically separated.

Closure requires all of:

1. WP-19 frozen `campaign_id` is the sole semantic campaign component of `LiveSourceKey` and of the F24 printable source-native ID frame;
2. no second semantic `campaign_technical_id` is persisted or accepted as campaign identity;
3. WP-11 `<campaign-technical-id>` is realized only as `encode_live_campaign_route_token(campaign_id)` using domain-separated length-framed UTF-8 input and full lowercase SHA-256 hexadecimal with `c1-` prefix;
4. the repaired LIVE envelope carries canonical `campaign_id` and selection/recovery validates `(campaign_id, scene_id, epoch_id)` against the selected route/source;
5. physical-token equality alone is never semantic identity proof; token/body mismatch is a typed integrity failure with no search/random-suffix/alternate-route repair;
6. RD-14 initial materialization propagates exact frozen `campaign_id` into admitted scaffold projections and does not generate a second semantic campaign identity;
7. RD-06 ordinary post-initialization publication rejects a change to `MANIFEST.campaign_id` before remote mutation;
8. RD-07 selected-LIVE recovery resolves current canonical campaign identity, derives route token, loads exact source, then validates the LIVE body tuple before adopting LIVE owner/currentness evidence;
9. branch/ref name, current revision, creator login, card projection and route token never substitute for canonical campaign identity.

Primary witnesses:

- RD-14 `CreationIdentityTests` / `GeneratorScaffoldTests` campaign-ID cases;
- RD-06 `CampaignIdentityImmutabilityTests`;
- RD-09 `LiveCampaignRouteIdentityTests`;
- RD-09 corrected `SourceNativeLiveIdEncodingTests`;
- RD-07 `SelectedLiveCampaignIdentityRecoveryTests`.

## PG26 exact closure law

PG26 closes only when multiple source-native creations in one frozen LIVE mutation have an exact reproducible technical slot mapping without inventing cross-owner chronology.

Closure requires all of:

1. only `SOURCE_NATIVE_LIVE` families participate in the allocation list;
2. each participating native-family adapter supplies one deterministic ordered sequence with contiguous unique `owner_local_creation_index = 0..m-1` for that family;
3. unordered/ambiguous owner output with no deterministic native sequence blocks the attempt rather than being arbitrarily enumerated;
4. global attempt normalization orders family groups by raw UTF-8 bytes of canonical native-family ID and preserves ascending owner-local creation index within a family;
5. `creation_slot_index` is exactly the zero-based position in the normalized array;
6. for frozen cursor `start`, `source_local_creation_ordinal = start + creation_slot_index` and resulting cursor is exactly `start + n`;
7. allocation order never comes from final native ID, payload/hash/serialization, dictionary/set iteration, wall clock or randomness and carries no fictional chronology/priority semantics;
8. the frozen attempt retains exact `(native_family, owner_local_creation_index, creation_slot_index, source_local_creation_ordinal, native_id)` mapping;
9. a definite stale/not-applied attempt may rebuild from refreshed current source because its prospective IDs were noncanonical;
10. an indeterminate attempt must reconcile the original frozen allocation before any second allocation range may be created;
11. RD-07 recovery validates accepted source-native identity/allocation from exact source evidence and never regenerates IDs from current container iteration.

Primary witnesses:

- RD-09 `SourceNativeCreationOrderingTests`;
- RD-09 `SourceNativeAmbiguousPublicationTests`;
- RD-09 `SourceNativeLiveIdEncodingTests`;
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

## PG35 exact closure law — F58 operational roots

Mandatory overlay `2026-09-15-implementation-planning-operational-root-routing-addendum.md` owns the exact physical contract, interfaces, lifecycle cases, failure behavior, module/class placement and checkpoint joins. PG35 requires actual A/B/C native producer output, same-closure campaign/LIVE routing, exact selection/absorption, complete bounded cold recovery without checkpoint/HOT/remembered IDs, generated blank format and actual final projection bytes. Its active-Procedure-after-Command-settlement case is mandatory. Marker syntax or a partial namespace listing never proves completeness. R072 and the applicable R038/R074 item-bound duties remain separately routed; PG35 is not a new readiness ID or replacement aggregate proof.

Primary integration witnesses: DEV/TESTS/test_rd06_durability_publication.py::OperationalRootPublicationTests, DEV/TESTS/test_rd09_access_live.py::LiveOperationalRootHandoffTests and DEV/TESTS/test_rd07_recovery.py::OperationalRootRecoveryTests. Focused contract/enrollment/generated-scaffold and static final-file witnesses are mandatory at the exact locations in overlay 37. OPERATIONAL_ROOT_ROUTING_PROOF_READY follows every target; it feeds no semantic producer. No future runtime witness is claimed executed by this planning amendment.


## PG36 exact closure law — F59 access-policy mutations

Mandatory overlay `2026-09-15-implementation-planning-campaign-access-policy-transition-addendum.md` supplies the three existing policy-operation producers, exact typed field scope, complete bounded impact, one collaboration after-authority view, current LIVE/campaign/companion acceptance and separate actual-admission/catch-up consumer proof. The four exact task-owned classes/channels and checkpoint order in that overlay are mandatory. R080 items 3/4/11/12 and R083 theme16 retain their individual owner duties and consume the applicable F59 cases; neither a class name nor aggregate PG count closes them. Join-policy non-revocation, prospective grant change and creator-unresolved denial are required negatives. This row does not resolve the creator architecture decision or replace PG35.
