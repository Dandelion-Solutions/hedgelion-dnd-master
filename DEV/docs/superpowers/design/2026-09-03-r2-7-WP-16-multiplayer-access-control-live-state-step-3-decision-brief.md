# R2.7 WP-16 — Multiplayer / Access Control / Live State — Step-3 Decision Brief

Status: **STEP 3 DECISION BRIEF — DECISION MECHANICALLY DERIVED / NO HUMAN DECISION REQUIRED**

Date: 2026-09-03

Evidence basis:

- repaired WP-16 Step-1 package;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-16-step-1-senior-recovery-SR16-01-SR16-02.md`;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-step-2-source-manifest-expansion.md`;
- `DEV/docs/superpowers/design/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-step-2-evidence-extraction.md`.

---

## 1. Decision question

What implementation-facing WP-16 realization contract makes multiplayer authorization and LIVE currentness machine-decidable while preserving current native owners, supported Connector identity capability, exact-source concurrency, deterministic accepted execution and bounded ordinary-turn cost?

The question is constrained by already accepted architecture; WP-16 does not choose a new multiplayer product model.

---

## 2. Established facts

1. The supported connected GitHub Connector can expose the current authenticated principal with a stable external GitHub numeric user ID distinct from mutable login.
2. Current access architecture already requires stable external user ID -> active PLAYER binding and rejects repository permission/login as gameplay authority.
3. Controlled-PC relation and operation-specific authorization remain separate from membership.
4. Step 5.8 already fixes routed immutable typed LIVE claims, exact-source CAS, `ACTIVE -> CLOSED`, `CLOSED_UNABSORBED`, no campaign fallback, source-native identities and no distributed transaction.
5. WP-12/13/14 distinguish campaign currentness, LIVE currentness and local HOT currentness, and prohibit local/transport state from becoming semantic authority.
6. WP-15 prohibits deriving fictional chronology from Git/ref/CAS/freeze/storage/ID order and preserves accepted execution/RNG/Continuation identity across source movement/retry.
7. Current scene-centric LIVE schema/runtime/tests are incomplete realization evidence, not authority over those owners.
8. Card/session/MANIFEST/index/cache surfaces have narrower proven roles and cannot authorize gameplay merely by containing similar fields.
9. R2.5 leaves async collaboration to WP-17 and forbids absence from assigning voluntary PC agency.

---

## 3. Alternatives

### Alternative A — preserve scene-centric LIVE as the effective authority

Treat one `LIVE_STATE` scene envelope as the current owner for all mutable scene state, use participant lists/touched entities as practical claim scope, and rely on live revision/blob CAS plus current session identity.

**Benefits:** closest to shipped prose/schema; simple physical implementation.

**Rejected because:**

- contradicts Step-5.8 physical-packing non-authority law;
- does not prove typed claim containment/non-overlap;
- risks participant/touched-set leakage into write authority;
- permits local revision/blob mechanics to substitute for exact-source currentness;
- blurs knowledge/disclosure and native owner state;
- cannot safely express owners spanning or crossing scene partitions.

### Alternative B — owner-typed fixed-claim realization with stable-principal authorization

Use the supported Connector stable principal identity to resolve current PLAYER membership/control, then apply operation-specific authorization and current owner-specific `WriteAuthorityLookup`. LIVE is a physical source selected by campaign/native routing for an immutable typed claim set; exact-source CAS establishes LIVE mutation; authority transfers only through forward close/freeze + campaign transition.

**Benefits:** directly realizes accepted owners; bounded; fail-closed; supports independent live epochs and recovery; preserves deterministic execution and no-login-fallback rule; machine-decidable.

**Cost:** current scene-centric schema/runtime/test material must later be reshaped; claim/currentness validation becomes explicit.

**Recommendation:** SELECT.

### Alternative C — global multiplayer coordinator / LIVE registry / distributed transaction

Introduce a campaign-wide owner that tracks sessions, claims, leases, current LIVE state, revocation and cross-LIVE transfers, with global transaction/rollback semantics.

**Benefits:** superficially centralizes coordination.

**Rejected because:**

- duplicates current native ownership/currentness;
- violates Step-5.8 no long-lived leader/global fencing owner;
- adds background liveness/lease semantics not supported by product contract;
- introduces a distributed transaction/global rollback model explicitly rejected upstream;
- creates unnecessary campaign-wide contention and recovery coupling.

---

## 4. Selected architecture direction

> **STABLE-PRINCIPAL AUTHORIZATION CHAIN / OWNER-TYPED IMMUTABLE LIVE CLAIMS / DOMAIN-SEPARATED CURRENTNESS / EXACT-SOURCE CAS / FORWARD NO-WINDOW AUTHORITY TRANSFER**

Conceptually:

```text
SUPPORTED HOST
  -> CONNECTED GITHUB CONNECTOR
  -> trusted current authenticated principal
  -> stable external GitHub user ID
  -> current PLAYER binding + current membership
  -> current controlled-PC relation when applicable
  -> operation-specific authorization
  -> owner-specific WriteAuthorityLookup(target)
       -> CAMPAIGN @ exact current campaign basis
       -> LIVE(E) @ exact selected source revision
       -> INTEGRITY_CONFLICT
  -> authorized native transition
```

A LIVE epoch is not another semantic owner. It is a selected physical/currentness partition for exactly the immutable typed native claims admitted to it.

---

## 5. Required consequences

### 5.1 Principal identity

- Stable external GitHub user ID is the multiplayer binding key.
- Mutable login remains display/audit/owner-specific metadata and cannot substitute for `user_id`.
- If trustworthy principal identity is unavailable for an operation requiring it, fail closed with typed capability/authorization failure; no transport or login fallback.

### 5.2 Authorization

- Repository permission is necessary infrastructure evidence where an operation requires it, never sufficient gameplay authority.
- PLAYER active/inactive status, controlled-PC relation, policy grants and target operation are current owner inputs.
- Cached card/session/index/HOT state does not create an authorization lease.

### 5.3 LIVE claims

- one epoch claim set is immutable;
- each claim is typed native owner/owner-defined partition reference;
- membership/containment/non-overlap are deterministic;
- participant/touched/path/overlay sets do not become claims automatically;
- one claimed native owner/partition has exactly one current truth authority and at most one ordinary writer.

### 5.4 Currentness

Campaign ref/revision, LIVE exact source revision and local HOT view are different currentness domains. No numeric/string/order comparison crosses them unless an owner defines the relation.

### 5.5 Exact-source CAS

- CAS is the establishment/fencing edge for LIVE transition;
- CAS success still requires application authorization and valid current route/claims;
- pre-CAS state is prospective;
- post-CAS local adoption cannot rollback/replay accepted remote transition.

### 5.6 CLOSED_UNABSORBED

Selected CLOSED source remains current truth for its claims and admits zero ordinary writers until valid forward absorption/transfer changes routing.

### 5.7 Revocation

When deactivation/revocation touches an active LIVE participant/claim domain:

```text
exact-source close/freeze
-> prove exact final CLOSED source
-> one campaign authority transition, where same campaign boundary applies,
   establishes absorption/survivor + deactivation/authorization removal + route/index update
-> optional successor for remaining authorized participants
```

This closes the stale authorization/write window in current shipped wording.

### 5.8 Multi-LIVE transfer

Sequential source freezes are technical prerequisites. Only the owner-defined forward campaign transfer establishes the cross-scope semantic result. Partial freeze is recoverable technical state, never partial fiction; no distributed rollback.

### 5.9 Accepted execution / RNG

Close, CAS conflict, absorption, revocation, source movement or local adoption failure never authorize replay/reroll/rematerialization of accepted execution. Stable Step-3 identity governs resume/retry.

### 5.10 Chronology

Git/ref/CAS/freeze/publication/storage/index/ID order is technical currentness/provenance only unless a chronology owner explicitly admits a relation. A CAS winner does not automatically become the fictionally earlier action.

### 5.11 Agency

Absence/disconnect/deactivation does not make voluntary PC choices, transfer voluntary control or imply consent. Existing world/procedure rules may still cause non-voluntary consequences without borrowing PC agency.

### 5.12 Projection surfaces

CAMPAIGN_CARD, session, MANIFEST, CURRENT, indexes, cached HEAD/live state and menu classifications remain only in their proven owner/projection roles. Authorization-sensitive mutation must resolve current owner evidence.

### 5.13 Async collaboration

WP-17 remains downstream. WP-16 supplies identity/currentness/write-authority substrate only and does not create collaboration obligation/order semantics.

---

## 6. Machine-realization implications

Later implementation planning must, at minimum:

- expose stable authenticated-principal ID through the supported Connector adapter;
- resolve active PLAYER/control/policy current state before protected mutation;
- materialize machine-decidable typed LIVE claim identity/containment/non-overlap;
- define current route lookup and exact-source fence evidence;
- replace scene-mega-owner wording with native owner routing;
- narrow/remove generic provisional IDs where accepted identity escapes;
- fix live knowledge/disclosure projections against existing information owners;
- repair revocation transaction ordering;
- repair per-user-action LIVE write assumptions to native durability-edge granularity;
- preserve bounded fast-path performance.

No implementation is authorized by this Decision Brief.

---

## 7. Decision status

```text
SELECTED: ALTERNATIVE B
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
CONFIDENCE: HIGH
STEP_4_READY: YES
```

The selected result is mechanically implied by closed upstream authority plus verified supported-host capability. There is no remaining product-semantic or material trade-off requiring human judgment.