# Campaign House Rules — Step 3 Owner Decision

Status: **OWNER APPROVED — STEP 3 HUMAN GATE CLOSED / STEP 4 NEXT**

Date: 2026-08-25

Governing amended Decision Brief:

- `DEV/docs/superpowers/design/2026-08-25-campaign-house-rules-step-3-decision-brief-amended.md`

This decision closes only the material human choices reopened by the Senior whole-project audit. Step 1 remains closed. Preserved House-Rules directions remain unchanged.

---

## 1. H1 — responsibility shape

**APPROVED: A + narrow C.**

```text
existing runtime owners keep behavioral/authority responsibilities
+
narrow structured policy identity/currentness/adoption evidence
```

No dedicated generic House-Rules runtime owner, predominantly structured rules engine, universal semantic-value language, or prose-only/no-linkage architecture is introduced.

---

## 2. H2 — policy-adoption authority

The campaign distinguishes live situational adjudication from adoption of reusable campaign-wide normative policy.

### 2.1 `INTERPRETIVE_POLICY`

Examples include contextual applicability, stable interpretive precedent and semantic campaign rulings that do not themselves grant prose execution authority.

**Owner decision:** every currently active campaign `PLAYER` may adopt `INTERPRETIVE_POLICY` by default in multiplayer.

Inherited access law still applies:

- repository Write/Admin permission alone is insufficient;
- an unbound or inactive PLAYER does not receive this authority;
- the acting authenticated principal must resolve to the active PLAYER under current campaign authorization/currentness rules;
- in singleplayer, existing creator-only gameplay publication authority remains the effective writer boundary.

No stored interpretive-policy grant is required.

### 2.2 `MECHANICAL_OVERRIDE_POLICY`

This class is a deliberate campaign rule that changes baseline mechanical semantics such as cost, threshold, activation or consequence policy and may require a matching typed deterministic realization.

**Owner decision:** campaign creator owns this authority by default.

The campaign creator may explicitly grant or revoke `MECHANICAL_OVERRIDE_POLICY` adoption authority for a specific campaign PLAYER.

For a non-creator, effective mechanical-override adoption authority requires both:

```text
current active PLAYER binding
AND
explicit current creator-issued mechanical-override grant for that PLAYER
```

The grant does not bypass deterministic realization, policy currentness, information eligibility, RNG, native owner validation or publication/CAS law.

### 2.3 Creator identity remains inherited Git provenance

`creator` means the author of the campaign itself: `author.login` of the first campaign-specific initialization commit in the campaign branch, as already owned by `ACCESS_CONTROL.md` / `CAMPAIGN_SETUP.md` / `BOOTSTRAP_RUNTIME.md`.

This decision does **not** move creator authority into `MANIFEST` and does not duplicate creator identity there.

Normal gameplay shall not perform history lookup per turn. Once creator identity is authoritatively resolved for an applicable session/authority operation, it may be retained as immutable session-local derived authorization evidence. Git history remains the authority/audit source when creator resolution is actually required.

---

## 3. Policy-change notification semantics

There is no background push, polling worker, delivery queue or House-Rules notification subsystem.

Existing multiplayer/session repository-currentness mechanisms remain the transport/discovery basis:

```text
cached campaign base HEAD
-> ordinary required campaign ref refresh
-> if HEAD changed, bounded base..HEAD changed-path comparison
-> if current House-Rules policy paths changed, acquire/revalidate exact current policy at the new pinned HEAD
-> continue under the new current basis for new affected work
```

When a Master discovers a newly published House-Rule/Ruling change through that normal refresh, the Master appends a concise out-of-character notice to the end of the current ordinary Master output for that session's player, for example that Player B changed specified campaign rules.

The notice is presentation/catch-up behavior, not policy authority and not a second publication acknowledgement protocol.

Accepted/frozen prior Resolution generations remain historically stable. A later policy publication is forward-looking.

No exactly-once notification guarantee or persistent notification cursor is introduced by this decision. Repetition after context loss is preferable to inventing a heavyweight delivery-ack subsystem unless later evidence proves a stronger consumer requirement.

---

## 4. Derivable machine consequences

The following are now authorized derivations, subject to existing owner/supersession inspection and TDD:

1. add the smallest per-PLAYER machine-readable grant required for non-creator `MECHANICAL_OVERRIDE_POLICY` adoption;
2. keep missing grant equivalent to `false` and keep inactive PLAYER non-authoritative;
3. do not add a stored `INTERPRETIVE_POLICY` grant because active PLAYER authority is the default law;
4. do not add creator identity to MANIFEST;
5. materialize the already-approved narrow policy identity/currentness/adoption sidecar without duplicating normative prose;
6. preserve campaign commit/current source as the exact policy revision/publication basis rather than inventing a global policy epoch;
7. reuse existing session/campaign HEAD currentness for policy-change discovery and player notification; do not add a notification frontier/cursor absent a proven stronger requirement.

---

## 5. Gate transition

```text
STEP 1: CLOSED / PRESERVED
STEP 2: REPAIRED / COMPLETE
STEP 3: OWNER DECISION COMPLETE
STEP 4: UNBLOCKED / NEXT
S6D: BLOCKED UNTIL VALID HOUSE-RULES STEP 8
R2.7 WP-06: PAUSED
```
