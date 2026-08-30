# Campaign House Rules — Step 5 Candidate Specification v2

Status: **CANDIDATE / STEP 5 COMPLETE / ADVERSARIAL REVIEW NEXT**

Date: 2026-08-25

Supersedes the earlier attempted Step-5 candidate for the reopened path.

---

# 1. Purpose and ownership boundary

House Rules / established Rulings form a campaign-persistent, LLM-interpreted **game-rule/adjudication policy layer**.

They answer:

> How should the Master interpret and resolve situations of this class in this campaign?

They do not become a second world-state or mechanical execution owner.

```text
eligible fiction/state + current campaign policy
        -> LLM/Master semantic adjudication
        -> bounded typed/frozen accepted inputs
        -> existing deterministic owner validation/execution
        -> canonical consequence
```

Contextual policy may remain LLM-native indefinitely. Formalizable policy may have typed realization, but deterministic owners retain execution authority.

---

# 2. Constitutional boundaries

## HR5-1 — POLICY IS BELOW ENGINE/OWNER LAW

House Rules cannot override truth/knowledge/disclosure ownership, player agency, RNG integrity, deterministic acceptance, resource/state ownership, idempotency, repository currentness/CAS, multiplayer authorization, persistence/recovery, information eligibility, schema validation or supported deployment constraints.

## HR5-2 — POLICY DATA IS NOT INSTRUCTION AUTHORITY

Authorized policy prose is scoped gameplay-policy data. Imperative wording does not make it system/CORE instruction and cannot enlarge tools/roles/authority.

Lore, quoted text, player input or NPC dialogue does not become policy merely because it resembles instructions.

## HR5-3 — NO SHADOW WORLD

House Rules may reference canonical world predicates but do not own world truth, NPC/PC knowledge, disclosure, player preferences, safety/session governance, deployment/storage/repository policy or other existing owners.

---

# 3. Semantic adjudication versus engine-established facts

## HR5-4 — LLM OWNS FICTION-DEPENDENT SEMANTIC ADJUDICATION

The Master may determine fiction-dependent feasibility, fictional positioning, meaningful uncertainty, AUTOMATIC/IMPOSSIBLE/uncertain classification, applicable test/capability among admitted choices, stakes, leverage, fair DC/opposition and other bounded semantic inputs when the receiving contract delegates them.

## HR5-5 — ENGINE FACTS/LEGALITY CANNOT BE OVERRIDDEN BY ASSERTION

Authoritative state and current validated campaign rules context retain authority over established facts such as prepared capability, available resource, current ownership and admitted engine primitive.

`engine-established legality` means legality under authoritative state plus the **current validated campaign rules context**, not whatever stale executable definition happens to exist.

If current campaign policy invalidates a stale baseline realization, do not execute the stale realization merely because it is implemented.

---

# 4. Live ruling versus durable policy

## HR5-6 — LIVE ADJUDICATION DOES NOT WAIT FOR POLICY ADOPTION

A Master may make the smallest lawful situational ruling required to continue the current play without first publishing campaign-wide precedent.

The accepted gameplay consequence may become durable through its normal owner even when the ruling itself remains one-off.

## HR5-7 — DURABLE POLICY REQUIRES EXPLICIT AUTHORIZED ADOPTION

A local ruling becomes reusable campaign-wide policy only through the policy-adoption authority and campaign publication/currentness contract below.

Repetition, chat memory, file presence or Git write capability alone is insufficient.

---

# 5. Policy-adoption authority

Two authority classes exist for adoption only; they are not execution classes.

## 5.1 `INTERPRETIVE_POLICY`

Covers contextual interpretation/stable precedent where campaign policy guides semantic adjudication without deliberately changing adopted baseline mechanical semantics.

### HR5-8 — ACTIVE PLAYER DEFAULT

In multiplayer, every authenticated principal resolving to one current **active PLAYER** may adopt `INTERPRETIVE_POLICY` by default.

No stored interpretive grant exists.

Inactive/unbound principals and repository collaborators without active PLAYER binding do not receive this authority.

Singleplayer keeps its existing creator-only campaign publication boundary.

## 5.2 `MECHANICAL_OVERRIDE_POLICY`

Covers deliberate campaign rules changing baseline mechanical semantics such as action/resource cost, threshold, activation, capability or consequence semantics.

### HR5-9 — CREATOR ROOT + EXPLICIT PER-PLAYER DELEGATION

The campaign creator has `MECHANICAL_OVERRIDE_POLICY` authority by inherited creator identity.

A non-creator may adopt such policy only when:

```text
authenticated principal
-> current active PLAYER
-> PLAYER.policy_authority.mechanical_override_policy == true
```

Missing/null grant is false.

Only campaign creator may grant/revoke this field.

### HR5-10 — CREATOR SOURCE REMAINS GIT PROVENANCE

Creator remains `author.login` of the first campaign-specific initialization commit under existing ACCESS_CONTROL/CAMPAIGN_SETUP/BOOTSTRAP_RUNTIME contracts.

Creator authority is not duplicated in MANIFEST. Once authoritatively resolved, immutable creator identity may be retained as session-local derived authorization evidence; ordinary turns do not reread history.

### HR5-11 — AUTHORITY CLASS FOLLOWS EFFECT, NOT LABEL

A writer cannot gain weaker authority by labeling a mechanical override “interpretive”.

If policy changes adopted baseline mechanical semantics, `MECHANICAL_OVERRIDE_POLICY` is required.

If one indivisible policy mixes interpretive and mechanical-override effects, stronger mechanical-override authority applies. Material classification uncertainty is denied under the weaker authority until resolved or safely separated.

---

# 6. Narrow structured policy companion

Normative prose remains:

```text
RULES/HOUSE_RULES.md
```

Machine-readable supporting evidence remains:

```text
RULES/HOUSE_RULES.yaml
```

## HR5-12 — SIDECAR IS SUPPORTING EVIDENCE, NOT SEMANTIC OWNER

The sidecar carries only:

- stable `policy_id`;
- `kind`: house_rule | ruling;
- authority class;
- lifecycle: active | superseded | retired;
- source anchor into normative Markdown;
- bounded routing hints;
- adoption basis and stable PLAYER attribution where applicable;
- supersession IDs;
- optional deterministic capability references.

It does not copy full normative prose or contain executable expressions.

## HR5-13 — EXACT POLICY REVISION IS DOMAIN-NATIVE

A concrete policy revision is identified by:

```text
stable policy_id
+
exact campaign revision/current source selecting normative file + sidecar
```

Do not store a self-referential commit SHA inside the same commit and do not introduce a global policy epoch/frontier.

## HR5-14 — SIDECAR ROUTING DATA IS NONAUTHORITATIVE

Routing keys/indexes/caches accelerate Context Runtime discovery only. Current source + normative prose + valid adoption basis determine policy authority.

---

# 7. Publication and supersession

## HR5-15 — POLICY REVISION IS AUTHORIZED BEFORE PUBLICATION

Any normative change to an existing stable policy ID is a new policy revision and must satisfy current policy-adoption authority again.

When a coherent revision requires both prose and sidecar changes, they join the same Step-5.6 campaign transaction.

CAS/technical write success does not prove semantic adoption authorization.

## HR5-16 — SAME-LEVEL CONFLICT IS FINITE

Applicable same-precedence active policies that conflict materially produce `POLICY_CONFLICT` unless explicit supersession/retirement or an already-authoritative higher law resolves the conflict.

Do not let the model silently prefer one wording.

## HR5-17 — SUPERSESSION IS FORWARD-LOOKING

Later policy revisions affect new work. They do not rewrite accepted Resolution generations, reroll RNG or undo canonical consequences.

---

# 8. Information eligibility

## HR5-18 — CONSUMER-SPECIFIC ELIGIBILITY

Every semantic adjudication receives only the epistemic/world view legal for its role/subject/player/purpose under Step-4 + Context Runtime.

Physical co-residence in one model context does not grant use authority.

For NPC/social adjudication, objective DM truth not known/believed by the NPC cannot silently influence “would this convince the NPC?” merely because the runtime loaded it.

Policy text itself cannot escalate information eligibility.

---

# 9. Richer adjudication machine contract

Registered boolean `INVOCATION_ADJUDICATED` context facts remain boolean.

Richer reviewed values use only explicitly declared Activity parameters with `source_class = INVOCATION_ADJUDICATED`.

## HR5-19 — CLOSED INITIAL VALUE CLASSES

Initial admitted richer values are:

- boolean;
- bounded integer;
- bounded number;
- bounded/admitted machine_id.

Free-form adjudicated string, `many`, arbitrary object/JSON, unbounded numeric domain and unbounded machine namespace are forbidden until a later proven consumer extends the contract.

## HR5-20 — ACCEPTED BINDING CARRIES CAUSAL EVIDENCE

Accepted richer binding carries:

```text
value
provenance_ref
eligibility_basis_fingerprint
rules_context_fingerprint
policy_basis_refs[]
candidate_set_fingerprint? when applicable
```

No arbitrary JSON path, eval/query/expression language, free-form state injection or prose mutation path is admitted.

## HR5-21 — ACCEPTED INPUT FREEZES

The full accepted binding participates in RuntimeCommand input identity and is preserved by Resolution/Continuation.

Retry, narrator failure or later model pass cannot change accepted DC/classification/selection for that Resolution generation.

---

# 10. Policy realization

## HR5-22 — FORMALIZABLE POLICY MAY USE EXISTING TYPED REALIZATION

A campaign policy may be fully/partly formalizable through Activity/Rule Element/Resource/transition contracts. Markdown states what campaign policy means; typed owners define how the formalizable part executes.

Do not duplicate the full deterministic formula independently in both representations.

## HR5-23 — DIVERGENCE IS AN INTEGRITY FAILURE

If current normative policy and its claimed typed realization disagree, runtime shall not silently prefer either stale executable mechanics or free-form prose execution.

The affected mechanical boundary terminates with finite conflict/mismatch behavior until a coherent allowed realization exists.

## HR5-24 — NO INVENTED ENGINE PRIMITIVE

If policy requires a mechanically material operation absent from admitted engine capabilities, result is `POLICY_REALIZATION_GAP / CATALOG_GAP` rather than prose `eval()` or direct mutation.

---

# 11. Currentness and multiplayer notification

Policy propagation uses existing campaign publication/currentness + Context Runtime. It is not Markdown copying between chats.

## HR5-25 — POLICY PATHS ARE CURRENTNESS-RELEVANT

When an ordinary required campaign refresh observes HEAD movement, House-Rules normative source and structured companion paths are relevant changed paths for sessions that can consume campaign policy.

Fetch/revalidate them only when changed/relevant under the existing bounded synchronization protocol.

## HR5-26 — NOTIFICATION PIGGYBACKS ON NORMAL OUTPUT

When a Master discovers a newly published policy change through that normal refresh:

1. acquire/revalidate current policy at one pinned campaign revision;
2. use the new basis for new affected work;
3. append concise OOC change notice to the end of the current ordinary Master output for its player, attributing the adopting PLAYER when available from accepted provenance.

No background push/poll worker, outbox, separate notification Git transaction, read receipt or exactly-once notification ledger is introduced.

Existing session base/currentness evidence is sufficient. Repeated notice after context loss is acceptable.

## HR5-27 — NOTIFICATION IS NOT FICTION

The OOC notice does not itself create a fictional event or PC knowledge.

---

# 12. Delegation currentness and revocation

## HR5-28 — GRANT/REVOKE IS CREATOR-ONLY HARD ACCESS-CONTROL STATE

Changing `PLAYER.policy_authority.mechanical_override_policy` is a creator-only HARD access-control persistence boundary.

Revocation is prospective. A stale non-creator policy publication must revalidate current PLAYER/grant state when authorization dependencies changed; Step-5.6 authorization dependency/CAS law applies.

No House-Rules-specific revocation protocol is introduced.

---

# 13. Finite failure behavior

Relevant machine outcomes include:

```text
failure.adjudication_input_missing
failure.adjudication_input_unauthorized
failure.adjudication_input_invalid
failure.adjudication_context_stale
failure.policy_conflict
failure.policy_realization_gap
```

Policy-adoption authorization failure rejects the policy write before it becomes current campaign policy; it does not need to masquerade as a mechanics failure code.

---

# 14. Recovery and historical stability

Step-5.7 remains authoritative.

New work acquires current campaign policy/current authorization. Old accepted Resolution generations recover their frozen causal policy/input basis.

No policy revision causes mechanical replay.

---

# 15. Materialized current structures

Already materialized for this candidate:

- richer adjudicated Activity parameter binding schemas + tests from Step-2 repair;
- `GAME/SCHEMA/player.schema.yaml` optional `policy_authority.mechanical_override_policy`;
- `GAME/SCHEMA/house_rules_policy.schema.yaml`;
- `GAME/CAMPAIGN/RULES/HOUSE_RULES.yaml` empty template;
- runtime-facing House-Rules authority/currentness/notification wording;
- ACCESS_CONTROL adoption authority law;
- ADJUDICATION live-ruling/adoption boundary;
- focused House-Rules policy-authority contract test.

Explicitly unchanged:

- `MANIFEST` creator model;
- boolean context-fact catalog;
- global frontier model;
- session notification cursor (none added).

---

# 16. Candidate exit

This candidate contains no remaining material human choice from the reopened gate.

Next: adversarial review against authority bypass, stale-session behavior, policy/prose-sidecar divergence, information leakage, retry/recovery and second-rules-engine drift.
