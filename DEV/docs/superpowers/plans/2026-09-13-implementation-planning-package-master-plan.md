# HDM Implementation Planning Package — Master Plan

Status: **AUTHOR ADVERSARIAL CLOSURE ACTIVE**
Date: 2026-09-14

Current executable routing is defined by `2026-09-13-implementation-planning-package-index.md`.

Current package: RD-01 through RD-16; 24 mandatory overlays. Author Findings 1–31, F34 and F35 are planning-repaired and independently unconfirmed; F32 is a negative finding; F33 is a repaired control-plane defect.

Current execution authority: `2026-09-14-implementation-planning-execution-waves-v2-post-graph.md` plus later-precedence F27–F31 routing in `2026-09-14-implementation-planning-f27-f31-control-amendment.md`; F34 adds a proof-checkpoint join; F35 adds the RD-12 PLAYER collaboration local-semantic-ready -> RD-16 strict PLAYER integration edge and amends the final shared-machine join.
Current bidirectional coverage authority: `2026-09-14-implementation-planning-bidirectional-coverage-v3-post-graph.md` plus the F27–F31 control amendment, the F34 runtime-family R018 amendment and the F35 PLAYER collaboration strict-state integration amendment.
Current post-graph proof authority: `2026-09-14-implementation-planning-lossless-proof-ledger-v3-post-graph.md` + F27–F31 control amendment + `2026-09-14-implementation-planning-post-graph-proof-witness-matrix.md` + F34 runtime-family R018 proof amendment + F35 PLAYER collaboration strict-state integration amendment.

Highest-precedence mandatory LIVE realization repairs remain:

```text
F24  source-native cursor / exact printable identity
F25  canonical campaign identity / physical c1 route token
F26  deterministic multiple-creation ordering
F27  exact epoch identity / s1 scene token / complete opening basis
F28–F31 LIVE opening idempotency, exact initial seeding,
        completeness-protected LIVE routing and native-state packing/absorption
```

The highest-precedence LIVE execution overlay for F28–F31 is `2026-09-14-implementation-planning-live-opening-routing-native-state-addendum.md`. The later-precedence control/proof/coverage/execution routing amendment is `2026-09-14-implementation-planning-f27-f31-control-amendment.md`.

Finding 23 requires one reconstructive accepted `CatalogContextBasis` across RD-15 deterministic binding, RD-05 accepted RuntimeCommand/Resolution/Continuation evidence, RD-06 durability/retention closure and RD-07 exact recovery. Fingerprint-only, ambient/current/latest rebinding and durable dependence on unpublished session-only definitions are forbidden.

Findings 24–27 require exact source-native LIVE identity/opening realization: semantic source key `(campaign_id, scene_id, epoch_id)`; bounded `c1` and `s1` physical route tokens; exact `e1` epoch identity derived from immutable opening basis; CAS-owned nonreused uint64 source-local cursor; deterministic attempt-local multi-creation normalization; injective `framed_base32hex_v1`; no campaign allocator fallback and no accepted-ID rekey on absorption.

Findings 28–31 close the remaining opening/handoff worker-readiness seams:

- deterministic candidate preparation is idempotent and acknowledgement-aware; equivalent prepared source is reusable but not authority, incompatible deterministic-ref occupant blocks;
- initial LIVE native state for existing claims is seeded exactly from one pinned campaign revision `H`, while `EPOCH_LOCAL_CREATION` seeds no fabricated owner;
- `STATE/RUNTIME/LIVE_ROUTING.yaml` is the completeness-protected campaign route/claim companion used by bounded `WriteAuthorityLookup`; scene/current/index/ref projections cannot prove claim absence;
- final v1 LIVE packing contains typed native-owner state rather than legacy generic overlays, and exact CLOSED state is materialized forward into campaign native routes with stable IDs, required companions and route removal in one campaign publication closure.

Finding 34 closes the R018 runtime-family proof asymmetry: package proof requires an exact 17-row runtime-family schema/root matrix and `R018RuntimeFamilyProofTests` in addition to world-family proof and the separate RD-15 catalog-gap behavioral witness. Count/catalog presence is not proof.

Finding 35 closes the PLAYER shared-schema integration hole: WP-17 `collaboration_route_refs` is durable completeness-protected PLAYER state and must be integrated by RD-16 into final strict `world.player` state. RD-12 supplies the owner-local collaboration delta; RD-16 becomes the final physical integrating writer/checkpoint for the strict/shipped PLAYER machine generation. Final RD-16 PLAYER integration waits on the named RD-12 local semantic-ready checkpoint, without creating a whole-RD serial barrier.

Current block: continue fresh graph-based adversarial review of the complete 16-RD / 24-overlay package. F34/F35 publication does not constitute zero-open author closure.

Independent Senior review remains blocked until the adversarial graph audit reaches fresh zero-open author closure and the exact final HEAD passes hosted maintenance audit plus full DEV unittest discovery.

Production implementation is not authorized.
