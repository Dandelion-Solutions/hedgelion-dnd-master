# R2.7 WP-13 — Durability / SAVE / Publication — Step 7 Resolution Gate

Status: **STEP 7 COMPLETE — ALL BLOCKING/SIGNIFICANT FINDINGS RESOLVED**

Date: 2026-09-02

Reviewed Step-6 critic:

- `DEV/docs/superpowers/design/2026-09-02-r2-7-WP-13-durability-save-publication-step-6-whole-project-adversarial-review.md`

This resolution gate records binding amendments to the Step-5 candidate. Where this file is more precise than the Step-5 candidate, this resolution controls the Step-8 canonicalization. It does not alter closed upstream semantics.

---

# 1. F01 resolution — final current compatible source composition

Finding: **BLOCKING**

Disposition: **CLOSED**

Binding amendment:

> A composed SAVE/HARD promise is satisfied only when, at its success/acknowledgement boundary, the runtime proves one current compatible composition of every required native durable source under each participating owner's currentness/routing rules.

Consequences:

- a domain's earlier confirmed publication remains real durable/lineage evidence;
- historical success of A1 plus B1 does not prove current success if current authority has materially moved to incompatible A2/B2;
- final proof is bounded to participating native sources and required dependency/authorization/routing footprint;
- no scalar cross-domain frontier, total order or persistent source-cut owner is created;
- if a participating current source moves during the composed operation, revalidate only the affected compatibility/dependency portion according to the native owner;
- acknowledgement is withheld until the current composition satisfies the promised RRC/durability closure.

This is direct Step-5.2/5.5/5.7 current-authority composition, not a new transaction layer.

---

# 2. F02 resolution — operation-current `NO_WRITE_NEEDED`

Finding: **BLOCKING**

Disposition: **CLOSED**

Binding amendment:

> `NO_WRITE_NEEDED` is valid only when the current durability operation has sufficient lawful currentness evidence to prove that the relevant native domain's required source closure is currently compatible/durable.

Consequences:

- zero local dirty paths or an old cached `known_head` is not proof;
- currentness may be reused without a new remote read only when the applicable native protocol already establishes that basis for this operation;
- when native currentness policy requires a refresh/ref probe, the no-write path performs that bounded validation before promise success;
- if current authority moved over relevant recovery/authorization/routing/dependency state, revalidate before returning no-write;
- no gratuitous confirmation read is introduced after a current confirmed own publication when that currentness evidence is already sufficient.

Thus clean SAVE remains genuinely zero-write but never stale-authority-blind.

---

# 3. F03 resolution — trustworthy acting principal/delegation

Finding: **SIGNIFICANT**

Disposition: **CLOSED**

Binding amendment:

> Every publication requiring application authorization must consume a trustworthy resolved acting-principal/delegation identity from the admitted authentication/identity boundary. Technical write capability and caller-supplied Git commit author/login fields are not authorization evidence.

Consequences:

- creator/player/policy semantics remain owned by Access Control / native authority contracts;
- frozen publication attempts carry the trustworthy resolved principal and the exact authorization basis needed by the operation;
- mutable authorization dependencies remain revalidated at their owning boundary;
- if the supported host/Connector profile cannot supply the required trustworthy principal/delegation evidence, publication returns typed `CAPABILITY_FAILURE` / `AUTHORIZATION_UNAVAILABLE` or equivalent and does not write;
- no runtime transport fallback is attempted;
- WP-13 does not change campaign-creator semantics or invent a second identity system.

---

# 4. F04 resolution — confirmed rejection cause classification

Finding: **SIGNIFICANT**

Disposition: **CLOSED**

Binding amendment:

A `CONFIRMED_REJECTED` final ref outcome is classified before any retry disposition:

```text
STALE_OR_NON_FAST_FORWARD
    -> bounded currentness/footprint revalidation
    -> transport-only rebuild if proven disjoint
    -> owner-specific reconciliation/revalidation if relevant

AUTHORIZATION_REJECTED
    -> typed authorization failure
    -> no automatic semantic retry until authority changes/revalidates

CONFIGURATION_OR_RULE_REJECTED
    -> typed repository/profile configuration failure
    -> no force / hidden ref / per-file bypass

CAPABILITY_OR_INFRASTRUCTURE_REJECTED
    -> typed supported-profile/infrastructure failure
    -> no alternate transport

UNCLASSIFIED_CONFIRMED_REJECTION
    -> fail closed as unresolved infrastructure/publication rejection
    -> do not assume stale conflict
```

`INDETERMINATE` remains a different epistemic class and still uses ambiguity verification rather than this rejection table.

---

# 5. F05 resolution — quiescence release / safe abandonment

Finding: **SIGNIFICANT**

Disposition: **CLOSED**

Binding amendment:

SAVE quiescence is ephemeral local operation state with explicit terminal dispositions.

### Success

After final current compatible source-composition proof succeeds:

- adopt confirmed source bases/generations;
- release the affected SAVE quiescence;
- subsequent gameplay uses the accepted current basis.

### Confirmed failure / safe abandonment while host survives

If completeness/publication fails and:

- coherent established local/private HOT remains valid;
- current native authority/dependency basis can be revalidated as required; and
- no independent named HARD edge remains unresolved,

then the runtime may abandon the explicit SAVE attempt, release the local SAVE freeze after that revalidation and continue under Step-5.5 failure semantics. It must not claim `saved`.

### Indeterminate or unresolved current authority

If current authority remains indeterminate for a participating correctness-critical scope:

- do not release the affected dependent edge as successful;
- keep only the affected dependency scope gated as required by owner semantics;
- unrelated independent scopes/OOC are not globally locked;
- once currentness is proven or the owner permits safe abandonment against an accepted current basis, release the ephemeral freeze.

No persistent lock, lease, host generation or SAVE owner is introduced.

---

# 6. F06 resolution — risk-control exposure remains MAY_DEFER protection

Finding: **SIGNIFICANT**

Disposition: **CLOSED**

Binding amendment:

> Scope-relative unpublished-exposure risk control does not itself create `MUST_BE_DURABLE_BEFORE(edge)`.

When a policy threshold/condition requests a risk-control flush:

- evaluate from the actual oldest still-relevant unpublished basis for that scope;
- attempt opportunistic publication at a suitable safe established-state point;
- on success, update only the actually covered owner generations/exposure basis;
- on failure while coherent local/private HOT survives, mark protection degraded/retry-due as local operational state and allow ordinary local/private continuation;
- a separate owner-defined named HARD edge still blocks its own dependent continuation;
- no threshold, elapsed time or retry condition silently upgrades deferrable state to HARD.

WP-13 selects no numeric threshold or cadence.

This explicitly prevents the current one-hour blocking contract from being preserved under a renamed scope-relative clock.

---

# 7. Cross-finding consistency review

The amendments were checked together against the accepted architecture.

| Cross-check | Result |
|---|---|
| final source-composition proof vs no global frontier | CONSISTENT — proof is ephemeral/bounded/domain-typed |
| operation-current no-write vs zero-I/O/no-heartbeat | CONSISTENT — no write required; remote read only when currentness owner requires it |
| trusted principal vs Access Control | CONSISTENT — consumes existing authority, creates none |
| rejection classification vs fixed R2.6 transport | CONSISTENT — no alternate fallback |
| quiescence release vs Step-5.4/5.5 | CONSISTENT — local scoped barrier only |
| risk-control failure vs named HARD | CONSISTENT — MAY_DEFER remains distinct from HARD |
| partial multi-domain success vs final current proof | CONSISTENT — accepted native publications remain real, overall promise waits for current compatible closure |
| G-specific adoption vs final current proof | CONSISTENT — only proven covered frozen G adopts; newer G+1 remains dirty |
| live exact-source CAS | CONSISTENT — live currentness remains native and participates only through its current selected source |
| checkpoint/storage/engine maintenance boundaries | CONSISTENT — no owner transfer |

No amendment requires upstream reopening.

---

# 8. Resolution status

```text
F01 BLOCKING:     CLOSED
F02 BLOCKING:     CLOSED
F03 SIGNIFICANT:  CLOSED
F04 SIGNIFICANT:  CLOSED
F05 SIGNIFICANT:  CLOSED
F06 SIGNIFICANT:  CLOSED

UNRESOLVED_BLOCKING:      0
UNRESOLVED_SIGNIFICANT:   0
HUMAN_DECISION_REQUIRED:  NO
UPSTREAM_REOPEN_REQUIRED: NO
STEP_8_MAY_PROCEED:       YES
```

Step 8 must incorporate these binding amendments into the final canonical WP-13 source of truth and perform final consistency/impact verification.