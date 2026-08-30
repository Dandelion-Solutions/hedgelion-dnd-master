# Campaign House Rules and Rulings

Status: **CANONICAL ARCHITECTURE — HOUSE-RULES DESIGN CLOSED / S6D-10 INTEGRATION COMPLETE**

Date: 2026-08-25

Current canonicalization basis:

- `DEV/docs/superpowers/design/2026-08-24-campaign-rulings-house-rules-architecture-task-brief.md`;
- `DEV/docs/superpowers/design/2026-08-25-campaign-house-rules-step-2-auditor-reopen-evidence-delta.md`;
- `DEV/docs/superpowers/design/2026-08-25-campaign-house-rules-step-3-decision-brief-amended.md`;
- `DEV/docs/superpowers/specs/2026-08-25-campaign-house-rules-step-3-owner-decision.md`;
- `DEV/docs/superpowers/design/2026-08-25-campaign-house-rules-step-4-collaborative-review-v2.md`;
- `DEV/docs/superpowers/design/2026-08-25-campaign-house-rules-step-5-candidate-spec-v2.md`;
- `DEV/docs/superpowers/design/2026-08-25-campaign-house-rules-step-6-adversarial-review-v2.md`;
- `DEV/docs/superpowers/design/2026-08-25-campaign-house-rules-step-7-resolution-gate-v2.md`.

The earlier attempted Step-3..8 closure artifacts are historical derivation only where they conflict with this repaired chain.

Primary inherited owners remain Step-4 truth/knowledge/role-context + single-context amendment, R2.3 Context Runtime, R2.4 LLM/instruction boundary, Step-3 execution owners, Step-5.6 publication, Step-5.7 recovery, Step-5.8 multiplayer currentness, R2.5 collaboration, `ACCESS_CONTROL.md`, `ACTIVITY_MODEL.md` and `RULE_ELEMENT_MODEL.md`.

---

# 1. Central invariant

House Rules / established Rulings are a **campaign-persistent, LLM-interpreted game-rule/adjudication policy layer**.

They provide a legal home for Dungeon-Master reasoning that depends on meaning, fictional context, causal judgment and analogy and therefore cannot or should not be forced into a universal Python/Rule-Element language.

Canonical shape:

```text
current eligible fiction/state
+ current admitted campaign policy
        -> LLM/Master semantic adjudication
        -> bounded accepted/frozen semantic inputs
        -> existing deterministic owner validation/execution
        -> canonical consequence / RNG / state transition / no-op
```

## LAW HR-1 — SEMANTIC AUTHORITY IS REAL BUT BOUNDED

The LLM/Master may make substantive fiction-dependent adjudications. It is not reduced to a Boolean classifier.

## LAW HR-2 — SEMANTIC AUTHORITY IS NOT STATE/EXECUTION AUTHORITY

Policy/LLM never directly owns RNG, arithmetic, HP/resources/effects/assets, canonical mutations, idempotency, repository publication or native-owner acceptance.

---

# 2. Scope

House Rules owns **campaign game-rule/adjudication policy** only.

Valid examples include contextual interpretation, stable precedent, hybrid semantic+mechanical policy and deliberate campaign mechanical overrides.

It does not own world truth/lore, specific NPC/PC knowledge, disclosure, transcript/history, player preferences, safety/session governance, deployment/storage/repository behavior, prompts/system instructions or duplicate deterministic mechanics state.

## LAW HR-3 — NO SHADOW WORLD / NO GENERIC POLICY WAREHOUSE

Putting prose into the House-Rules surface does not transfer ownership from an existing semantic owner.

---

# 3. Information and instruction boundaries

Every adjudication consumes only information eligible for its exact role/subject/player/purpose under the existing Step-4/R2.3 contracts.

Physical availability in the one-model context is not semantic eligibility. An NPC ruling cannot use DM-only truth merely because the runtime loaded it.

Authorized House-Rule text is scoped policy data, not a higher instruction tier. Imperative wording cannot override project/CORE/role/tool/authority restrictions.

## LAW HR-4 — POLICY CANNOT ESCALATE INFORMATION OR INSTRUCTION AUTHORITY

Policy may constrain adjudication only inside its admitted gameplay-policy scope.

---

# 4. Semantic adjudication versus engine facts

The Master may decide fiction-dependent feasibility, fictional positioning, meaningful uncertainty, AUTOMATIC/IMPOSSIBLE/uncertain status, applicable admitted test/capability, stakes, leverage, fair DC/opposition and other reviewed bounded semantic inputs.

Deterministic owners retain authority over established state-derived facts and legality: prepared/known capability, current resource balance, ownership, current conditions and admitted engine primitives.

## LAW HR-5 — CURRENT RULE CONTEXT DEFINES LEGALITY

`engine-established legality` means authoritative state + current validated campaign rules context, not merely whatever old executable definition is currently present.

Current authorized campaign policy may invalidate a stale baseline realization. Stale executable mechanics do not defeat current policy merely because Python can run them.

---

# 5. One-off ruling versus durable policy

A Master may make the smallest lawful situational ruling needed for current play without first creating campaign-wide policy.

The resulting accepted roll/world/state consequence persists through ordinary owners even if the ruling itself remains one-off.

A reusable House Rule/Ruling becomes campaign-wide normative only through explicit authorized adoption and current campaign publication.

## LAW HR-6 — LIVE ADJUDICATION AUTHORITY != POLICY-ADOPTION AUTHORITY

Campaign publication/consensus is never a prerequisite for the current bounded ruling itself.

---

# 6. Policy-adoption authority

Two adoption authority classes exist. They classify **authority to adopt policy**, not execution mechanism.

## 6.1 `INTERPRETIVE_POLICY`

Contextual applicability, semantic interpretation and stable precedent that do not deliberately replace adopted baseline mechanical semantics.

### LAW HR-7 — ACTIVE PLAYER DEFAULT

In multiplayer, every authenticated principal resolving to one current active PLAYER may adopt `INTERPRETIVE_POLICY` by default.

No stored interpretive grant exists. Inactive/unbound users and repository permission alone are insufficient.

Singleplayer retains its existing creator-only gameplay publication boundary.

An interpretive policy may guide an admitted DC/classification/selection without becoming a mechanical override merely because the eventual deterministic execution consumes that bounded adjudication result.

## 6.2 `MECHANICAL_OVERRIDE_POLICY`

Deliberate campaign policy that changes adopted baseline mechanical semantics such as action/resource cost, threshold, activation, capability or consequence semantics.

### LAW HR-8 — CREATOR ROOT + NARROW PER-PLAYER GRANT

Campaign creator has this authority by inherited creator identity.

A non-creator requires:

```text
current authenticated principal
-> one active PLAYER
-> PLAYER.policy_authority.mechanical_override_policy == true
```

Missing/null is false.

Only campaign creator may grant/revoke this field. Grant/revoke is a creator-only HARD access-control persistence boundary.

Later deactivation or grant revocation is prospective; it does not retroactively invalidate policy revisions that were lawfully published while authorized.

## LAW HR-9 — AUTHORITY CLASS FOLLOWS SEMANTIC EFFECT

A writer cannot downgrade required authority by labeling a mechanical override “interpretive”. Mixed indivisible policy requires the stronger authority. Material ambiguity is denied under the weaker class until safely resolved/separated.

---

# 7. Creator ownership

Creator semantics remain exactly the existing campaign ownership contract: the author of the first campaign-specific initialization commit.

## LAW HR-10 — HOUSE RULES DOES NOT MOVE CREATOR INTO MANIFEST

Creator identity is not duplicated in MANIFEST. Ordinary turns do not reread history; once authoritatively resolved for a session/authority operation, immutable creator identity may be retained as derived session authorization evidence.

---

# 8. Normative prose + narrow structured companion

Normative human/LLM policy lives in:

```text
RULES/HOUSE_RULES.md
```

Narrow machine-readable supporting evidence lives in:

```text
RULES/HOUSE_RULES.yaml
```

The sidecar carries stable policy ID, House-Rule/Ruling kind, authority class, lifecycle, source anchor, routing hints, adoption basis, stable PLAYER attribution where available, supersession and optional `realization_refs`.

## LAW HR-11 — SIDECAR IS NOT THE NORMATIVE OWNER

It does not copy full normative prose and does not contain an executable predicate/expression/query language.

## LAW HR-12 — EVERY DURABLE NORMATIVE POLICY ENTRY IS ADMITTED EXACTLY ONCE

Every current durable normative House Rule/Ruling has exactly one current sidecar entry with a unique stable policy ID and resolvable source anchor.

Unindexed normative prose is not admitted as durable campaign-policy authority. Duplicate IDs/anchors, orphan sidecar entries or unresolved normative sections are malformed/integrity defects at the affected policy boundary.

## LAW HR-13 — EXACT REVISION IS DOMAIN-NATIVE

A concrete policy revision is:

```text
stable policy_id
+
exact campaign revision/current source selecting Markdown + sidecar
```

No self-referential SHA, global policy epoch or scalar policy frontier is introduced.

Routing keys/indexes/caches are routing-only.

---

# 9. Precedence, conflict and supersession

Semantic precedence is:

```text
HDM constitutional/native-owner invariants
    > current applicable explicit House Rule
    > current applicable established Ruling
    > adopted baseline/structured rules
    > lawful local Master adjudication
```

Same-precedence material conflict is explicit: supersession/retirement, an already-authoritative higher rule, or finite `POLICY_CONFLICT` behavior. Hidden model preference is forbidden.

Later policy publication is forward-looking. Accepted historical Resolution generations and canonical consequences are not replayed/reinterpreted automatically.

---

# 10. Bounded discovery/currentness

R2.3 Context Runtime owns bounded policy discovery/eligibility/allocation. House Rules creates no independent retrieval engine/vector authority/policy graph.

Normal multiplayer publication/currentness remains Step-5/R2.5-owned.

## LAW HR-14 — POLICY PATHS PARTICIPATE IN EXISTING CURRENTNESS

On an ordinary required campaign refresh, HEAD movement is followed by the existing bounded changed-path compare. Changed House-Rules normative/sidecar paths are currentness-relevant to sessions that can consume campaign policy and are fetched/revalidated at one pinned campaign revision.

No background policy polling or chat copying is introduced.

## LAW HR-15 — NEW AFFECTED WORK USES THE REFRESHED CURRENT BASIS

Prepared/unaccepted work whose rules/authorization basis moved must revalidate. Already accepted/frozen work retains its causal basis.

---

# 11. Multiplayer policy-change notification

When a Master discovers a newly published House-Rules change through the normal campaign refresh:

1. acquire/revalidate the current policy;
2. use it for new affected work;
3. append a concise OOC change notice to the end of the current ordinary Master output for that session's player;
4. attribute the adopting PLAYER when accepted provenance supplies one.

## LAW HR-16 — NOTIFICATION IS PIGGYBACK PRESENTATION, NOT A DELIVERY SUBSYSTEM

No background push, separate queue, extra Git transaction, read receipt, exactly-once ledger or policy notification cursor is required.

A repeated notice after context loss is acceptable. The OOC notice is not a fictional event and does not create PC knowledge.

---

# 12. Richer semantic input machine contract

Registered `INVOCATION_ADJUDICATED` context facts remain boolean.

Richer invocation adjudication uses only explicitly declared Activity parameters with `source_class = INVOCATION_ADJUDICATED`.

Initial value classes are closed to:

- boolean;
- bounded integer;
- bounded number;
- bounded/admitted machine_id.

Free-form string, `many`, arbitrary objects/JSON, unbounded numeric domain and unbounded machine namespace are forbidden until a later proven consumer extends the contract.

Accepted richer binding carries:

```text
value
provenance_ref
eligibility_basis_fingerprint
rules_context_fingerprint
policy_basis_refs[]
candidate_set_fingerprint? when applicable
```

## LAW HR-17 — ACCEPTED ADJUDICATION INPUTS FREEZE

The full accepted binding participates in RuntimeCommand input identity and is preserved by Resolution/Continuation. Retry, narration failure or later model pass does not silently change accepted DC/classification/selection for that generation.

No arbitrary JSON path, eval/query/expression DSL, free-form state injection or prose bypass is admitted.

---

# 13. Policy ↔ typed realization

Formalizable policy may use existing typed realization while contextual policy may remain LLM-native forever.

The sidecar field:

```text
realization_refs[]
```

is an explicit declaration of typed capabilities intended to realize the formalizable portion of policy.

## LAW HR-18 — REALIZATION REFS ARE LINKAGE, NOT EXECUTION AUTHORITY

Every ref remains subject to current catalog/currentness/validation. Resolving an ID does not prove semantic equivalence by itself.

## LAW HR-19 — DIVERGENCE/GAP IS FINITE

Mechanically material policy requiring realization with no admitted current realization -> `POLICY_REALIZATION_GAP`.

Missing/stale/incompatible declared realization -> finite mismatch/gap, never stale baseline preference and never prose execution.

Contextual policy may have no realization refs indefinitely.

---

# 14. Publication and authorization

Any normative change to a stable policy ID is a new policy revision and must satisfy current adoption authority before publication.

When coherent revision requires prose + sidecar updates, Step-5.6 publishes them in one campaign transaction. Technical Git ability/CAS success is necessary transport evidence but not semantic adoption authority.

A non-creator cannot self-grant mechanical override authority in the same transaction; complete resulting-state authorization rejects the grant itself.

Grant/revoke/current PLAYER state are authorization dependencies and participate in stale-write revalidation.

---

# 15. Recovery/historical stability

Step-5.7 remains owner.

New work recovers current campaign policy/current authorization. Old accepted work recovers the frozen causal policy/input basis used by that Resolution generation.

Later policy publication never justifies RNG replay or accepted mechanics replay.

---

# 16. Current materialized machine/runtime surfaces

The settled architecture is already reflected in the current pre-release contracts:

- `DEV/SCHEMAS/activity-parameter-binding.schema.json` and related Step-3 execution schemas/tests;
- `GAME/SCHEMA/player.schema.yaml` narrow `mechanical_override_policy` grant;
- `GAME/SCHEMA/house_rules_policy.schema.yaml`;
- `GAME/CAMPAIGN/RULES/HOUSE_RULES.yaml` empty structured companion template;
- `GAME/CAMPAIGN/RULES/HOUSE_RULES.md` runtime-facing business-policy contract;
- `GAME/CORE/ADJUDICATION.md` live-ruling/adoption/frozen-input boundary;
- `DEV/ARCHITECTURE/ACCESS_CONTROL.md` policy-adoption authority;
- `DEV/TESTS/test_house_rules_adjudicated_input_contract.py`;
- `DEV/TESTS/test_house_rules_policy_authority_contract.py`.

Explicitly unchanged by House Rules:

- MANIFEST creator model;
- registered boolean invocation-fact catalog;
- global frontier model;
- session notification cursor (none exists);
- deterministic native state ownership.

---

# 17. Finite runtime outcomes

Existing richer input failures include:

```text
failure.adjudication_input_missing
failure.adjudication_input_unauthorized
failure.adjudication_input_invalid
failure.adjudication_context_stale
failure.policy_conflict
failure.policy_realization_gap
```

Unauthorized policy adoption is rejected before campaign policy publication; it need not masquerade as a mechanics failure.

---

# 18. Closure

The repaired House-Rules architecture closes the Senior-audit blockers:

- real Step-3 human owner decision occurred;
- A–E responsibility shapes were explicitly dispositioned;
- richer adjudication consumer contract is materialized;
- policy-adoption authority is explicit;
- creator ownership remains consistent with current project architecture;
- policy identity/currentness/realization linkage is machine-readable without becoming a rules DSL;
- multiplayer notification uses existing synchronization/currentness without another distributed subsystem.

House Rules is therefore architecturally closed.

**S6D-10 integration is complete. R2.7 WP-06 remains paused.**

# 19. S6D-10 exact mechanical integration

Durable policy materially used by an accepted richer binding or invocation fact is retained as a unique lexicographically sorted `policy_id@exact_campaign_revision` reference. Locator shape alone proves nothing: before Resolution construction the existing campaign publication/history resolver must prove the exact revision, paired sidecar/normative anchor, authority and applicability. One-off adjudication uses an empty array.

The exact integration owner is `HOUSE_RULES_MECHANICAL_BOUNDARY.md`. The built-in package remains an identity-bound candidate blocked until S6D-11. The current built-in realization set is empty; conformance fixtures are nonselectable and never execute their targets.
