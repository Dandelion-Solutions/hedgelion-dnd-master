# Campaign House Rules — Step 4 Collaborative Architecture Review v2

Status: **STEP 4 COMPLETE / NO MATERIAL HUMAN DECISION REMAINS / STEP 5 NEXT**

Date: 2026-08-25

Basis:

- preserved Step-1 Task Brief;
- repaired Step-2 evidence delta;
- amended Step-3 Decision Brief;
- `2026-08-25-campaign-house-rules-step-3-owner-decision.md`;
- current materialized richer adjudication contracts;
- current `ACCESS_CONTROL.md`, `PLAYER` schema, campaign/session currentness contracts.

This review supersedes the earlier attempted Step-4 closure for the reopened design path.

---

## 1. Owner decisions now fixed

### Responsibility

`A + narrow C`:

- existing runtime owners retain behavior/authority;
- structured policy data is supporting identity/currentness/adoption evidence only.

### Adoption authority

```text
INTERPRETIVE_POLICY
    multiplayer active PLAYER by default

MECHANICAL_OVERRIDE_POLICY
    campaign creator by default
    OR active non-creator PLAYER with explicit creator-issued grant
```

Creator remains the existing Git-provenance campaign creator; MANIFEST is not modified to duplicate creator identity.

### Notification

No push/outbox/notification service. On an ordinary required campaign refresh, changed House-Rules policy paths are currentness-relevant; after acquiring the new current policy, the Master appends a concise OOC notice to its ordinary response.

---

## 2. Review finding CR4-1 — creator lookup does not justify MANIFEST mutation

Current owners intentionally derive creator from the first campaign initialization commit and prohibit duplicate creator authority in MANIFEST.

`RUNTIME.md` already forbids ordinary-turn history reads. Creator is immutable, so a session may retain the already-proven creator as derived authorization evidence after a legitimate lookup.

**Resolution:** preserve existing creator ownership. No MANIFEST/schema/init change.

---

## 3. Review finding CR4-2 — per-player mechanical delegation has a real storage gap

Current PLAYER binding is the stable campaign principal used for multiplayer authorization, but previously had no scoped policy grant.

**Resolution:** add only:

```text
PLAYER.policy_authority.mechanical_override_policy: boolean|null
```

Rules:

- missing/null = false for non-creator;
- active PLAYER required;
- creator may grant/revoke;
- no stored interpretive grant;
- grant is policy-adoption authority only, not mechanics/state authority.

No generic role/ACL graph is introduced.

---

## 4. Review finding CR4-3 — structured policy linkage must not duplicate prose

Stable identity/currentness/adoption evidence is required, but copying full normative text into YAML would create dual-source drift.

**Resolution:** `RULES/HOUSE_RULES.md` remains normative human/LLM-readable policy. `RULES/HOUSE_RULES.yaml` is a narrow companion containing stable policy identity, authority class, lifecycle, source anchor, routing hints, adoption basis/PLAYER attribution, supersession and optional capability references.

Exact revision is:

```text
stable policy_id
+
exact current campaign revision selecting both files
```

No self-referential commit SHA is stored inside the same commit and no global policy epoch is introduced.

---

## 5. Review finding CR4-4 — authority class must not be self-declared bypass

A participant could otherwise label a mechanical override as `INTERPRETIVE_POLICY` and exploit the default active-PLAYER authority.

**Resolution:** authority classification follows semantic effect, not author-provided label.

- a rule that only guides contextual interpretation/adjudication without changing adopted baseline mechanical semantics may be `INTERPRETIVE_POLICY`;
- a rule that changes baseline cost, threshold, activation, resource/capability/consequence semantics is `MECHANICAL_OVERRIDE_POLICY`;
- if one indivisible policy has both components, the stronger `MECHANICAL_OVERRIDE_POLICY` authority is required;
- if uncertainty about classification is material to authorization, deny adoption under the weaker class until classified under the stronger authority or safely separated.

This classification is an authorization guard, not a new mechanical taxonomy/DSL.

---

## 6. Review finding CR4-5 — policy revision/adoption is an atomic campaign publication concern

Changing normative policy text is adoption of a new policy revision even when the stable policy ID stays the same.

**Resolution:** before campaign publication, application authorization is evaluated against the resulting policy revision and its authority class. When sidecar/prose changes are jointly required for a coherent result, they enter the same Step-5.6 campaign transaction. CAS success is necessary but never substitutes for semantic adoption authorization.

A stale writer rebases/revalidates from current policy before publication. Blind text merge is forbidden.

---

## 7. Review finding CR4-6 — grant revocation/currentness uses existing authorization dependencies

A revoked non-creator grant must not remain usable by a stale session.

Step 5.6 already includes authorization dependencies in the publication conflict footprint; multiplayer currentness already refreshes relevant PLAYER/access changes.

**Resolution:** mechanical-override grant/revoke is creator-only authorization state and a HARD access-control persistence boundary. A stale prepared policy adoption must revalidate current PLAYER/grant state before publication when its authorization basis moved.

No House-Rules-specific revocation protocol is required.

---

## 8. Review finding CR4-7 — notification needs no durable cursor

Existing session/campaign currentness already tracks a cached base HEAD and changed-path refresh. A separate policy-notification cursor would create another progress domain without a proven correctness consumer.

**Resolution:** when a normal refresh discovers a House-Rules source/sidecar change, emit one concise OOC notice in the current response after acquiring/revalidating the new policy. In-memory session base movement naturally avoids repeated detection during uninterrupted play. After context loss, a repeat notice is acceptable.

No exactly-once promise, acknowledgement ledger, background worker or global frontier.

---

## 9. Review finding CR4-8 — accepted consequences remain separate from policy durability

A one-off ruling may remain non-policy while its accepted roll/state/world consequence is durable under normal owners.

**Resolution:** preserve this distinction in candidate/runtime wording. Policy adoption is never required merely to persist the consequence of the current ruling.

---

## 10. Step-4 exit

```text
NEW MATERIAL HUMAN DECISIONS: 0
BLOCKING ARCHITECTURE CONFLICTS: 0
DERIVABLE STRUCTURAL CHANGES: IDENTIFIED / MATERIALIZATION IN PROGRESS
STEP 5: READY
S6D: BLOCKED
R2.7 WP-06: PAUSED
```
