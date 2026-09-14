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

Current execution graph: `2026-09-14-implementation-planning-execution-waves-v2-post-graph.md`, with overlay 17 adding the explicit accepted catalog-basis propagation/retention/recovery joins.
Current coverage: `2026-09-14-implementation-planning-bidirectional-coverage-v3-post-graph.md`, extended by F23 before author closure.
Current proof: historical v2 ledger/appendices + `2026-09-14-implementation-planning-lossless-proof-ledger-v3-post-graph.md` + mandatory exact witness matrix `2026-09-14-implementation-planning-post-graph-proof-witness-matrix.md`; F23 exact proof must be added before author closure.

Findings 16–23 mandatory deltas:
- F16: native `world.player` uses enclosing world-record `id` as its single campaign key; strict PLAYER state has no second persisted `player_id`.
- F17: RD-15/RD-16 obey overlay 5; later-task tests appear only in their own RED-to-GREEN task and are GREEN before publication.
- F18: catalog-backed RD-05 command acceptance requires RD-15 same-context validated binding and preserves its accepted catalog basis.
- F19: coverage v3 is current for the 16-RD / 17+17-family package.
- F20: proof-ledger v3 makes RD-15/RD-16 mandatory for R018 and adds post-WP27 proof rows.
- F21: execution-wave v2 is the current 16-RD dependency graph; older 14-RD wave documents are historical except for explicitly preserved edge semantics.
- F22: post-graph proof rows require exact named witnesses and primary proof channels from the current witness matrix; a thematic test reference is insufficient.
- F23: accepted catalog-backed execution carries one reconstructive `CatalogContextBasis` (exact ruleset-set identity + catalog fingerprint identity + bounded owner-local campaign/session definition dependency refs) from RD-15 through RD-05 durable execution, RD-06 retention/publication and RD-07 exact recovery. Fingerprint-only or ambient/current rebinding is forbidden; unpublished session-only definitions cannot become durable accepted dependencies without owner-approved promotion/publication basis.

Final census: 17 world families and 17 runtime families; `world.faction` is not an independent v1 family. Counts are not proof.

Accounting: 133 active = 116 direct + 9 proof + 8 composite; 12 trigger-gated; 79 no-work; R004 absent; 16 RD units; 17 overlays.

Author Findings 1–23 are planning-repaired once F23 coverage/proof/witness/execution/currentness routing updates are published and read back; all remain independently unconfirmed. Independent review remains blocked until fresh zero-open author closure and exact-head hosted validation.
