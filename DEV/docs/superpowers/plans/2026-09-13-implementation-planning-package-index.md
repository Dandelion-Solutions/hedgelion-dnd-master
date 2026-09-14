# HDM Implementation Planning Package — Index

Status: **AUTHOR ADVERSARIAL CLOSURE ACTIVE**
Date: 2026-09-14
Production implementation: **NO**.

Current base routes: RD-01..RD-16. RD-08, RD-10 and RD-11 use v2 plans. RD-15 owns catalog runtime binding. RD-16 owns world-family machine integration.

Mandatory overlays, low to high precedence:
1. `2026-09-13-implementation-planning-sirr-repair-amendments.md`
2. `2026-09-13-implementation-planning-author-self-review-repair-addendum.md`
3. `2026-09-13-implementation-planning-author-second-pass-repair-addendum.md`
4. `2026-09-14-implementation-planning-sirr2-consumer-cutover-repair-addendum.md`
5. `2026-09-14-implementation-planning-checkpoint-coherence-addendum.md`
6. `2026-09-14-implementation-planning-scene-routing-addendum.md`
7. `2026-09-14-implementation-planning-wp15-thread-catalog-addendum.md`
8. `2026-09-14-implementation-planning-wp17-shipped-consumer-addendum.md`
9. `2026-09-14-implementation-planning-temporal-completeness-routing-addendum.md`
10. `2026-09-14-implementation-planning-family-reconciliation-addendum.md`
11. `2026-09-14-implementation-planning-principal-player-routing-addendum.md`
12. `2026-09-14-implementation-planning-mechanical-event-identity-addendum.md`
13. `2026-09-14-implementation-planning-wp16-executable-closure-addendum.md`
14. `2026-09-14-implementation-planning-wp16-proof-ledger-post-graph-amendment.md`
15. `2026-09-14-implementation-planning-catalog-binding-shipped-consumer-addendum.md`
16. `2026-09-14-implementation-planning-post-graph-integration-addendum.md`
17. `2026-09-14-implementation-planning-catalog-context-reconstruction-addendum.md`
18. `2026-09-14-implementation-planning-source-native-live-id-encoding-addendum.md`
19. `2026-09-14-implementation-planning-live-campaign-identity-routing-addendum.md`
20. `2026-09-14-implementation-planning-live-source-creation-order-addendum.md`
21. `2026-09-14-implementation-planning-live-epoch-route-identity-addendum.md`
22. `2026-09-14-implementation-planning-live-opening-routing-native-state-addendum.md`
23. `2026-09-14-implementation-planning-runtime-family-r018-proof-closure-amendment.md`
24. `2026-09-14-implementation-planning-player-collaboration-strict-state-integration-amendment.md`
25. `2026-09-14-implementation-planning-live-temporal-companion-handoff-amendment.md`

Current execution graph: `2026-09-14-implementation-planning-execution-waves-v2-post-graph.md`, amended for F27–F31 by `2026-09-14-implementation-planning-f27-f31-control-amendment.md`; F34 adds only a proof-checkpoint join; F35 adds `RD12_PLAYER_COLLABORATION_ROUTE_LOCAL_SEMANTIC_READY -> RD16_PLAYER_STRICT_STATE_INTEGRATION_JOIN`; F36 adds bounded campaign<->LIVE temporal-companion handoff joins around RD-06 publication.
Current coverage: `2026-09-14-implementation-planning-bidirectional-coverage-v3-post-graph.md`, amended by the F27–F31 control amendment, the F34 runtime-family R018 amendment, the F35 PLAYER collaboration strict-state amendment and the F36 LIVE/temporal companion handoff amendment.
Current proof: historical v2 ledger/appendices + `2026-09-14-implementation-planning-lossless-proof-ledger-v3-post-graph.md` + F27–F31 control amendment + mandatory exact witness matrix + F34/F35/F36 later-precedence proof amendments.

Findings 16–36 current dispositions:
- F16: native `world.player` uses enclosing world-record `id` as its single campaign key; strict PLAYER state has no second persisted `player_id`.
- F17: RD-15/RD-16 obey overlay 5; later-task tests appear only in their own RED-to-GREEN task and are GREEN before publication.
- F18: catalog-backed RD-05 command acceptance requires RD-15 same-context validated binding and preserves its accepted catalog basis.
- F19: coverage v3 is current for the 16-RD / 17+17-family package.
- F20: proof-ledger v3 makes RD-15/RD-16 mandatory for R018 and adds post-WP27 proof rows.
- F21: execution-wave v2 is the current 16-RD dependency graph; older 14-RD wave documents are historical except for explicitly preserved edge semantics.
- F22: post-graph proof rows require exact named witnesses and primary proof channels from the current witness matrix; a thematic test reference is insufficient.
- F23: accepted catalog-backed execution carries one reconstructive `CatalogContextBasis` from RD-15 through RD-05 durable execution, RD-06 retention/publication and RD-07 exact recovery. Fingerprint-only or ambient/current rebinding is forbidden.
- F24: every `SOURCE_NATIVE_LIVE` family uses one exact v1 cursor/encoding realization: CAS-owned `uint64` source-local creation ordinal + `framed_base32hex_v1`; accepted IDs freeze in the same exact-source CAS as creation, survive absorption unchanged, and never use the campaign allocator. F25–F31 refine its source/route/opening/handoff realization.
- F25: canonical semantic LIVE campaign identity is `campaign_id`; physical campaign routing uses derived fixed-length `c1-<sha256>` token with LIVE-body identity verification.
- F26: multiple source-native creations in one frozen LIVE mutation use exact deterministic family/index/slot normalization; ambiguous owner output blocks.
- F27: LIVE epoch identity and route components are exact (`c1`/`s1`/`e1`), opening-basis equality is mandatory, and prepared source existence never establishes authority.
- F28: deterministic candidate preparation is idempotent and ambiguity-aware; incompatible deterministic-ref occupant blocks and lost acknowledgement is reconciled.
- F29: pre-existing claimed owners are seeded into initial LIVE state from one exact pinned campaign revision `H`; `EPOCH_LOCAL_CREATION` seeds nothing.
- F30: campaign `STATE/RUNTIME/LIVE_ROUTING.yaml` is the completeness-protected selected-route/claim companion; missing/stale/inconsistent companion cannot prove CAMPAIGN routing.
- F31: final v1 LIVE source uses typed native-state packing and lossless/idempotent forward absorption with stable IDs and required companions.
- F32: negative finding — accepted publication/deployment owners already supply the required testable exact-source CAS capability boundary; planning must not invent a REST/GraphQL primitive.
- F33: blocking control-plane regression repaired — `CURRENT_PROGRESS.md` again carries all markers required by maintenance-audit current-progress validation.
- F34: significant proof/coverage gap repaired — R018 runtime-family closure requires an exact 17-row schema/root matrix and `R018RuntimeFamilyProofTests`; count/catalog/world-only proof cannot close R018.
- F35: significant shared-schema/integration-order gap repaired — WP-17 `PLAYER.collaboration_route_refs` must survive final strict `world.player`; RD-12 supplies the delta and RD-16 is the final integrating writer/checkpoint.
- F36: significant cross-companion atomicity gap repaired — campaign->LIVE selection atomically moves affected current temporal enrollment from campaign `TEMPORAL_ROUTING` to the already-prepared selected LIVE source while adding `LIVE_ROUTING`; absorption atomically restores campaign temporal enrollment while removing `LIVE_ROUTING`. Duplicate/missing cross-domain current enrollment is an integrity conflict; no distributed transaction is introduced.

Final census: 17 world families and 17 runtime families; `world.faction` is not an independent v1 family. Counts are not proof.

Accounting: 133 active = 116 direct + 9 proof + 8 composite; 12 trigger-gated; 79 no-work; R004 absent; 16 RD units; 25 overlays.

Author Findings 1–31 and F34–F36 are planning-repaired at the package-router level; F32 is a negative finding and F33 is a repaired control-plane defect. All author-side dispositions remain independently unconfirmed. Independent review remains blocked until the broader adversarial graph audit reaches a fresh zero-open author closure and exact-final-HEAD hosted validation.
