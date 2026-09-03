# R2.7 WP-16 — Multiplayer / Access Control / Live State — Step-2 Evidence Extraction

Status: **STEP 2 EVIDENCE EXTRACTION COMPLETE — SYNTHESIS GATE PASS**

Date: 2026-09-03

Source Manifest expansion:

- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-step-2-source-manifest-expansion.md`

This ledger records source claims, qualifiers and current dispositions needed for Steps 3–8. It is evidence/provenance, not a new semantic owner.

---

## 1. Principal / binding / authorization chain

### E16-01 — supported Connector principal identity

**Source/evidence:** current supported connected GitHub Connector identity surface.

**Actual claim:** the current authenticated principal can be resolved with a stable numeric GitHub user identifier while mutable login is exposed separately.

**Classification:** CURRENT HOST CAPABILITY EVIDENCE.

**Qualifiers:** session/runtime capability evidence only; the concrete principal value is not architecture data and is not retained in public design artifacts.

**Disposition:** SATISFIED. The supported-host path can supply the stable external identity required by current PLAYER binding law. No login fallback is needed or allowed.

### E16-02 — fixed supported transport

**Sources:** R2.6 host assurance, fixed repository transport clarification, `PROJECT_INSTRUCTIONS.txt`.

**Actual claim:** supported campaign repository communication uses connected GitHub Connector; unavailable required capability is typed capability failure, not permission to substitute native Git/CLI/direct private HTTP/custom token transport.

**Disposition:** INHERITED / BINDING.

### E16-03 — external principal versus gameplay identity

**Sources:** `ACCESS_CONTROL.md`, `player.schema.yaml`, access-control regression cases.

**Actual claim:** multiplayer gameplay authority resolves current authenticated stable GitHub user ID to exactly one current active PLAYER binding; campaign semantic attribution uses stable `player_id`; login is mutable label only.

**Disposition:** INHERITED / BINDING.

### E16-04 — controlled-PC relation

**Sources:** `ACCESS_CONTROL.md`, R2.5 collaboration spec, player schema, membership cases.

**Actual claim:** current PLAYER membership does not by itself grant arbitrary PC control. A gameplay operation requiring PC agency must resolve current controlled-PC relation. Transfer is an explicit persistent semantic change.

**Disposition:** INHERITED / BINDING.

### E16-05 — operation-specific authorization

**Sources:** `ACCESS_CONTROL.md`, R2.6, WP-13, RUNTIME write-routing guard.

**Actual claim:** repository capability and successful transport/CAS do not establish application authorization. Target repository/ref, campaign, membership/creator role, controlled PC, policy grants and operation kind must all be valid under current owner contracts.

**Disposition:** INHERITED / BINDING.

### E16-06 — no authorization lease from cached state

**Sources:** WP-13, WP-14, session/card schemas and CORE modules.

**Actual claim:** session/card/index/cache observations are not durable authorization leases. Mutable authorization dependencies must be refreshed/revalidated at the operation's applicable currentness boundary.

**Disposition:** INHERITED / BINDING.

---

## 2. Currentness domains and write routing

### E16-07 — campaign currentness

**Sources:** Step 5.1/5.6 integration through WP-13/WP-14.

**Actual claim:** campaign currentness is the exact authoritative campaign ref/revision for campaign-owned scope, interpreted in the campaign publication domain.

**Negative:** commit timestamp/SHA lexical order/message text do not define semantic currentness.

**Disposition:** INHERITED / BINDING.

### E16-08 — LIVE currentness

**Source:** Step 5.8.

**Actual claim:** current valid campaign/native routing selects one LIVE epoch/source for each claimed native owner/partition. Exact selected source revision is the mutation fence. Branch existence, branch name, local `revision`, cached head or scene participation do not establish authority.

**Disposition:** INHERITED / BINDING.

### E16-09 — local HOT currentness

**Source:** WP-12.

**Actual claim:** local HOT/SQLite/process state is an adopted working realization and may be coherent/current locally without being the establishment authority for a remote LIVE transition. Pre-CAS LIVE mutation is prospective; post-CAS local adoption may lag or fail without undoing remote accepted state.

**Disposition:** INHERITED / BINDING.

### E16-10 — write authority lookup

**Source:** Step 5.8.

**Actual claim:** bounded owner-specific lookup decides `CAMPAIGN | LIVE(epoch/ref) | INTEGRITY_CONFLICT` for admitted live-mutable owner/partition classes. A composed read view never merges writable authority.

**Disposition:** INHERITED / REQUIRED MACHINE REALIZATION.

---

## 3. Typed immutable claims

### E16-11 — claim semantics

**Source:** Step 5.8.

**Actual claim:** LIVE claim is a typed native owner or owner-defined writable-partition reference. Claim membership/containment/non-overlap must be machine-decidable. Claim set is immutable for one epoch.

**Negative:** physical scene membership, participant lists, paths, touched entities or references do not imply claim closure.

**Disposition:** INHERITED / REQUIRED MACHINE REALIZATION.

### E16-12 — current schema gap

**Sources:** `live_scene.schema.yaml`, `scene.schema.yaml`, `LIVE_SCENE.md`.

**Actual evidence:** current live representation is scene-centric and carries participants, PC IDs, overlays, touched paths/entities and a local integer revision, but does not expose the Step-5.8 typed immutable claim contract directly.

**Disposition:** MACHINE DEBT. Later implementation must materialize typed claims/currentness without promoting LIVE storage into semantic mega-owner.

### E16-13 — native owner class boundary

**Sources:** `CATALOG_CONTRACTS.md`, `ENTITY_STRUCTURES.md`.

**Actual claim:** independent record/class admission follows semantic responsibility/lifecycle. Physical co-location does not make LIVE a new semantic class owner. Existing world/runtime owners remain authoritative.

**Disposition:** INHERITED / BINDING.

---

## 4. ACTIVE / CLOSED_UNABSORBED / transfer

### E16-14 — ACTIVE

**Source:** Step 5.8.

**Actual claim:** selected ACTIVE epoch is current truth for its claims and admits authorized ordinary exact-source CAS writes.

**Disposition:** INHERITED.

### E16-15 — CLOSED_UNABSORBED

**Sources:** Step 5.8, WP-14, LIVE runtime/tests.

**Actual claim:** selected CLOSED epoch remains current truth for its claims while admitting zero ordinary gameplay writers. Campaign base is not fallback current truth. Recovery may resume absorption/transfer only.

**Disposition:** INHERITED / BINDING.

### E16-16 — route-away / absorption

**Source:** Step 5.8.

**Actual claim:** normal route-away requires exact confirmed final CLOSED source. Authority changes forward through campaign transfer/absorption; old epoch never reopens. Optional successor opens only after new campaign authority state exists.

**Disposition:** INHERITED.

### E16-17 — live ref cleanup

**Source:** Step 5.13.

**Actual claim:** deleting/retiring live ref is post-authority cleanup. Ref deletion never establishes non-authority and cannot substitute for route/absorption state.

**Disposition:** INHERITED / BINDING.

---

## 5. Revocation / deactivation

### E16-18 — current membership semantics

**Sources:** access owner, player schema, membership tests.

**Actual claim:** deactivation makes PLAYER inactive while retaining stable identity/control history; rejoin may reactivate same binding under owner rules; creator removal cannot be bypassed by open enrollment.

**Disposition:** INHERITED.

### E16-19 — stale current shipped sequence

**Sources:** `MULTIPLAYER.md`, test M10.

**Actual evidence:** current sequence says close live epoch, compact, then persist deactivation.

**Problem:** after absorption restores campaign write route but before deactivation becomes authoritative, a stale participant can remain application-authorized long enough to attempt a campaign write. Exact LIVE close alone removes LIVE writes but does not remove membership authorization.

**Disposition:** SIGNIFICANT MACHINE/PROSE DEBT, mechanically resolvable from existing owner law.

### E16-20 — owner-conforming revocation closure

**Sources:** Step 5.8 revocation semantics + WP-13 campaign publication closure.

**Derived required result:** close/freeze first; then when membership removal and final absorption/route release share one campaign authority boundary, establish them in one coherent campaign transition before any successor ordinary write route becomes available.

**Qualifier:** already accepted write that wins before close remains accepted; close winning rejects stale ordinary LIVE write. No retroactive rollback/replay.

**Disposition:** REQUIRED CANDIDATE LAW; no human decision.

---

## 6. Multi-LIVE / cross-scope composition

### E16-21 — no distributed transaction

**Sources:** Step 5.8, Step 5.14, WP-12/WP-13.

**Actual claim:** cross-scope event may require sequentially closing/fencing multiple native sources, followed by one campaign-domain transfer/reconciliation. Partial freeze is recoverable technical state, not a fraction of fictional transition. There is no global rollback/distributed transaction requirement.

**Disposition:** INHERITED / BINDING.

### E16-22 — accepted execution continuity during freeze

**Sources:** Step 3, Step 5.8, WP-12/WP-14/WP-15.

**Actual claim:** close/freeze/retry/source movement does not cancel or recreate already accepted RuntimeCommand/Resolution/Procedure/Continuation/fixed RNG/idempotency evidence. Recovery resumes the accepted identity.

**Disposition:** INHERITED / BINDING.

---

## 7. CAS, authorization and chronology

### E16-23 — exact-source CAS fence

**Source:** Step 5.8.

**Actual claim:** exact current source revision is the optimistic concurrency fence for LIVE authoritative transition.

**Disposition:** INHERITED.

### E16-24 — CAS not application auth

**Sources:** Step 5.8, WP-13, access owner.

**Actual claim:** a technically successful write path is insufficient without current application authorization and current write-route admission.

**Disposition:** INHERITED / BINDING.

### E16-25 — no fiction from technical order

**Sources:** Step 5.1, WP-15.

**Actual claim:** Git/ref/CAS/freeze/publication/storage/ID order never becomes fictional chronology merely by technical ordering. Contested/simultaneous fiction uses its semantic rules/chronology owner.

**Disposition:** INHERITED / BINDING.

---

## 8. Identity realization

### E16-26 — live-born durable identity

**Sources:** Step 5.8, WP-11, `CATALOG_CONTRACTS.md`.

**Actual claim:** independently writable live sources require collision-safe source-native stable identities for accepted records that escape durable references; epoch-qualified namespace/local accepted creation coordinate is an accepted conceptual shape. Accepted identities survive absorption.

**Disposition:** INHERITED / WP-16 MACHINE-REALIZATION CONTRACT.

### E16-27 — provisional current schema field

**Source:** `live_scene.schema.yaml`.

**Actual evidence:** generic `provisional_id` exists for created live entities.

**Disposition:** narrow/retire according to owner contract. It may not be the default for any accepted identity that escapes the epoch or participates in idempotency/causal/external references.

---

## 9. Information / observation / disclosure

### E16-28 — knowledge separation

**Sources:** `INFORMATION.md`, Step-4/WP-07 inherited owner law, WP-15.

**Actual claim:** objective state, fictional subject knowledge and human PLAYER disclosure are distinct owners.

**Disposition:** INHERITED.

### E16-29 — LIVE observable/known fields

**Sources:** `LIVE_SCENE.md`, live schema.

**Actual evidence:** LIVE currently carries observable events, `known_by_pc_ids`-style projections and per-PC information for cross-session hot operation.

**Disposition:** DERIVED/ROUTING/EVIDENCE ONLY unless normalized into the canonical owner in the same accepted semantic closure. LIVE storage must not become a parallel durable `world.knowledge`/`runtime.disclosure` authority.

---

## 10. Card / manifest / session / indexes / caches

### E16-30 — campaign card

**Sources:** `CAMPAIGN_CARD.md`, card schema/template.

**Actual claim:** card fields are menu/display projection. Creator/participant GitHub logins and join-policy-derived lock/join presentation are hints only.

**Disposition:** SR16-02 SATISFIED. Revalidate source owners after selection.

### E16-31 — MANIFEST

**Source:** campaign manifest schema.

**Actual claim:** owns declared mode/join-policy/configuration fields only; explicitly does not duplicate creator owner. Player ID listing is routing/configuration, not stable external binding or PC-control authority.

**Disposition:** PROVEN OWNER-BOUNDED ROLE.

### E16-32 — session

**Sources:** WP-14, `SESSION.md`, session schema.

**Actual claim:** session stores navigation/coordination/currentness observations; it cannot authorize writes or select current truth after concurrent/source movement without owner revalidation.

**Disposition:** PROJECTION/OBSERVATION ONLY.

### E16-33 — indexes/caches/CURRENT

**Sources:** WP-11/WP-12/WP-14, current schemas/runtime.

**Actual claim:** derived indexes and cached HEAD/live/current records may support bounded lookup/fast path but never independently establish membership, control, claims or authority.

**Disposition:** DERIVED ONLY.

---

## 11. Agency / absence

### E16-34 — absence has no voluntary agency semantics

**Source:** R2.5 collaboration/multiplayer owner.

**Actual claim:** timeout, disconnect, host absence or inactive human does not grant consent, choose actions, transfer control or allow another participant to exercise voluntary PC agency. Native procedure/collaboration semantics determine whether progress waits or may proceed without that participant.

**Disposition:** INHERITED / BINDING.

### E16-35 — membership removal is technical/access transition, not fictional movement

**Sources:** membership cases M11, access/runtime owner law.

**Actual claim:** removing/deactivating player does not teleport, kill, erase or voluntarily act for their PC.

**Disposition:** INHERITED.

---

## 12. Regression accounting

### E16-36 — stale test: M10

Current M10 orders close -> compact -> deactivation -> successor. Final architecture must replace this with no-window revocation closure.

### E16-37 — stale test: L04

Current L04 requires one live write per logical user action. Step 5.8 says atomicity is per native durability edge; one user interaction can legally contain several edges. Final architecture must mark L04 stale.

### E16-38 — current test support

A09/A20/A25, L09-L13/L17-L27, PT19/PT20, integrity cases and manual live smoke-test TODO provide useful downstream verification routes once rewritten against current owner law.

**Disposition:** downstream WP-22 test coverage and WP-26 documentation/schema consistency; not implementation now.

---

## 13. Analytical challenge before synthesis

### Challenge A — should LIVE own the whole scene because that simplifies CAS?

No. Step 5.8 explicitly preserves native semantic owners and permits claims only for typed writable owners/partitions. Physical one-file packing is an optimization, not authority.

### Challenge B — can cached authenticated login avoid a principal lookup on every operation?

A cache may avoid redundant host work only under an explicit trusted-currentness contract. No current architecture authorizes mutable login as stable PLAYER identity. Current stable external ID remains the binding key, and mutable authorization dependencies still require operation-appropriate revalidation.

### Challenge C — does exact LIVE CAS make authorization races harmless?

No. CAS only serializes source revision. A stale but technically valid writer must still fail application authorization/current route checks. Revocation therefore needs an authority transition that prevents a route/membership gap.

### Challenge D — should CLOSED fall back to campaign to keep play moving?

No. That would create two conflicting current-truth interpretations and discard unabsorbed accepted state. CLOSED_UNABSORBED is intentionally current truth with zero ordinary writers.

### Challenge E — should multi-LIVE transfer use a distributed transaction?

No. Existing architecture deliberately uses technical freeze/fence prerequisites followed by a forward campaign transfer. Partial freeze is recoverable and has no partial fictional meaning.

### Challenge F — can transport/order resolve fictional races?

No. CAS determines which source transition was accepted, not automatically which fictional action should win when the fiction requires another ordering/adjudication rule. Technical order cannot be promoted to chronology.

### Challenge G — does removing a human let HDM continue controlling the PC?

No. Membership/access maintenance does not grant voluntary agency. Only existing world/procedure rules can cause non-voluntary consequences; voluntary PC actions remain player-owned.

---

## 14. Step-2 synthesis result

Recommended architecture direction for Step 3:

> **STABLE-PRINCIPAL AUTHORIZATION CHAIN + OWNER-TYPED IMMUTABLE LIVE CLAIMS + DOMAIN-SEPARATED CURRENTNESS + EXACT-SOURCE CAS + FORWARD NO-WINDOW AUTHORITY TRANSFER**

No alternative remains equally credible after current owner reconciliation. Centralized scene/global LIVE ownership and global transaction/coordinator approaches contradict accepted Step-5.8/WP-11..15 laws; login-based identity contradicts current access/player schema and supported Connector evidence.

```text
STEP_2_COMPLETE: YES
SOURCE_MANIFEST_COMPLETENESS_GATE: PASS
ANALYTICAL_CHALLENGE: PASS
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
STEP_3_READY: YES
```
