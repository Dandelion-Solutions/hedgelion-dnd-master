# R2.7 WP-16 Step-1 — Senior Recovery SR16-01 / SR16-02

Status: **SENIOR REPAIR COMPLETE — MANDATORY SENIOR REVIEW REQUIRED**

Date: 2026-09-03

Domain: `WP-16 — multiplayer / access control / live state`

Repair basis public HEAD:

- `914bd955544834260841b2428a3014462e780fb4`

This artifact records a narrow Senior recovery of the already completed WP-16 Step-1 package. It does not reopen Step-1 architecture decisions, does not start Step 2, and does not alter runtime/schema/template/catalog/test implementation.

Historical Task-Brief critic findings `C01-C16` and their original counts remain historical evidence and are not renumbered or recomputed by this repair.

---

## 1. Senior findings

### SR16-01 — BLOCKING — supported-host / principal-acquisition owner gap

The Step-1 Task Brief correctly began the authorization chain with authenticated external identity, but the Source Manifest did not directly include the current owners/consumers that establish the supported host, fixed Connector transport and acquisition of the current GitHub principal.

Missing mandatory Step-2 inputs:

- `DEV/docs/superpowers/specs/2026-08-24-r2-6-mvp-host-assurance-canonical-spec.md`;
- `DEV/docs/superpowers/design/2026-08-24-r2-6-fixed-repository-transport-owner-clarification.md`;
- `GAME/INSTALL/PROJECT_INSTRUCTIONS.txt`;
- `GAME/INSTALL/00_DND_BOOTSTRAP.md`.

Repair requirement:

```text
supported ChatGPT host
-> connected GitHub Connector identity/metadata surface
-> current authenticated GitHub principal
-> stable external GitHub user identity
-> current PLAYER binding/membership
-> controlled-PC relation
-> operation-specific authorization
-> current native write route/currentness
```

Binding boundaries preserved by the repair:

- Connector authentication/repository capability is an infrastructure prerequisite, not gameplay authorization;
- GitHub login is mutable metadata, not stable PLAYER identity;
- repository Write/Admin/collaborator status does not itself grant campaign, PC, policy or LIVE authority;
- unsupported alternate `git`, `gh`, direct HTTP, credential/token, MCP/custom-service or equivalent fallback is not allowed;
- failure to establish a trusted current principal for a write-sensitive operation means deny/block/capability failure under the owning contract, not guessed identity;
- R2.6 transport selection remains closed and is consumed only as a constraint.

Disposition: **CLOSED** by the repaired open-world Source Manifest.

---

### SR16-02 — SIGNIFICANT — direct campaign-card surfaces omitted

Historical critic C15 correctly identified the semantic danger of cached card/menu login hints becoming premature authority, but its original resolution overstated direct Source-Manifest coverage. The original manifest referenced bootstrap/card behavior indirectly while omitting the direct surfaces:

- `GAME/CORE/CAMPAIGN_CARD.md`;
- `GAME/SCHEMA/campaign_card.schema.yaml`;
- `GAME/CAMPAIGN/CAMPAIGN_CARD.yaml`.

The repair adds these as mandatory Step-2 inputs and requires explicit disposition of at least:

- `creator_github_login`;
- `multiplayer.participant_github_logins`;
- `multiplayer.join_policy` where used for menu hints;
- derived lock/join/menu classifications.

Binding boundary:

- campaign-card values are presentation/discovery/access-hint projections;
- they do not establish creator identity, active membership, PLAYER binding, controlled-PC authority or write permission;
- login strings are mutable labels rather than stable identity keys;
- after campaign selection, authority revalidates against actual Git provenance plus current PLAYER/access owners and current native write route/currentness;
- stale/tampered card values may affect presentation only and cannot expand authority.

Disposition: **CLOSED** by the repaired Source Manifest and explicit critic correction note.

---

## 2. Provenance correction

The historical whole-project Task-Brief critic remains a historical record:

```text
C01-C04 BLOCKING:       4
C05-C16 SIGNIFICANT:   12
```

Those counts are not changed by Senior review.

C15's original resolution said the then-published manifest included the campaign-card consumer coverage. Senior review demonstrated that the claim was too broad: the direct `CAMPAIGN_CARD` core/schema/scaffold surfaces were missing.

The critic now carries a superseding note that:

1. preserves C15 as originally found and counted;
2. does not pretend the original critic directly read sources it had omitted;
3. records SR16-02 as the later Senior discovery;
4. points to the repaired Source Manifest as the current Step-1 coverage authority.

---

## 3. Step-2 mandatory inputs after repair

If and only if Senior GO later authorizes Step 2, evidence extraction must include the newly enrolled inputs alongside the existing open-world manifest.

Principal acquisition / authorization chain:

```text
SUPPORTED CHATGPT HOST
-> CONNECTED GITHUB CONNECTOR IDENTITY/METADATA SURFACE
-> CURRENT AUTHENTICATED GITHUB PRINCIPAL
-> STABLE EXTERNAL GITHUB USER IDENTITY
-> CURRENT PLAYER BINDING/MEMBERSHIP
-> CURRENT CONTROLLED-PC RELATION
-> OPERATION-SPECIFIC AUTHORIZATION
-> CURRENT NATIVE WRITE ROUTE/CURRENTNESS
```

Campaign-card disposition:

```text
CARD CREATOR LOGIN / PARTICIPANT LOGIN LABELS / JOIN-LOCK-MENU CLASSIFICATION
    = presentation/discovery/access hints only
    != creator authority
    != membership authority
    != PLAYER binding
    != controlled-PC authority
    != write authorization
```

Post-selection authority revalidation remains mandatory.

---

## 4. Reopen and downstream boundaries

This Senior repair found no:

- contradiction between current accepted owners;
- newly unsatisfied product consumer requiring a product decision;
- material insufficiency requiring R2.6, R2.5, Step-5.8 or WP-11..WP-15 reopening.

R2.6 transport selection remains closed.

WP-17 async collaboration remains downstream and not started.

No implementation planning is authorized.

---

## 5. Repair disposition

```text
SR16-01:                       CLOSED
SR16-02:                       CLOSED
HISTORICAL_C01_C16:            PRESERVED
HISTORICAL_CRITIC_BLOCKING:    4
HISTORICAL_CRITIC_SIGNIFICANT: 12
UNRESOLVED_BLOCKING:           0
UNRESOLVED_SIGNIFICANT:        0
HUMAN_DECISION_REQUIRED:       NO
UPSTREAM_REOPEN_REQUIRED:      NO
STEP_2_AUTHORIZED:             NO
WP17_STARTED:                  NO
IMPLEMENTATION_PLANNING:       NO
NEXT_GATE:                     MANDATORY SENIOR REVIEW
```
