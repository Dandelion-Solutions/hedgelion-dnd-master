# S6D-10 — Campaign Rulings / House-Rule Mechanical Boundary — Research & Architecture Draft

Status: **STEP 2 COMPLETE / NO MATERIAL HUMAN DECISION OPEN**

Date: 2026-08-27

## 1. Research result

The accepted House-Rules architecture and the current S6D-01…09 deterministic surface already establish the correct responsibility split. S6D-10 does not need a new policy engine or a new product choice.

The remaining work is a narrow machine-conformance closure:

```text
one-off or policy-guided semantic judgment
-> exact typed accepted input
-> exact current consumer
-> deterministic existing owner execution

durable formalizable policy
-> exact current policy revision
-> typed realization linkage
-> current catalog + exact consumer validation
-> the same deterministic owner execution
```

Recommendation confidence: **HIGH**

Human decision required: **NO**

Evidence that would change the recommendation: a current supported policy requiring semantics that cannot lower to an admitted typed input or existing typed capability; a current owner requiring prose execution; or a material product decision to ship campaign-authored executable packages now. No such evidence exists.

## 2. Source Manifest and authority roles

### Canonical/owning

- `DEV/ARCHITECTURE/CAMPAIGN_HOUSE_RULES.md` — semantic policy/adjudication boundary.
- `DEV/ARCHITECTURE/ACCESS_CONTROL.md` — creator/PLAYER/adoption authority.
- `GAME/CORE/ADJUDICATION.md` — one-off ruling and deterministic handoff.
- Step-3 canonical execution specification — accepted Resolution/Continuation/segment/event/receipt ownership.
- Step-4 canonical truth/knowledge/context specification plus the single-context amendment — information eligibility.
- R2.3 canonical Context Runtime — bounded discovery/currentness/eligibility.
- R2.4 canonical single-context execution — typed gateways and instruction containment.
- Step-5.6/5.7/5.8 canonical owners — publication, recovery and multiplayer currentness.
- `RULESET_PACKAGE_IDENTITY.md`, `CATALOG_RESOLUTION.md`, `CATALOG_ADMISSION.md` — selected package/context/ref admission.
- S6D-04 `MECHANICAL_CONTEXT.md`, S6D-05 `PORTABLE_ACTIVITY_VALUES.md`, S6D-06 `ACTIVITY_PRIMITIVE_CONTRACTS.md` and S6D-09 `DOMAIN_RULES_COVERAGE.md` — exact input/value/consumer authority.

### Canonical amendment / explicit owner decision

- repaired House-Rules Step-3 owner decision and Step-8 canonicalization v2;
- Step-4 single-context role-containment amendment;
- S6D-09 Decision C owner decision and later spatial repair Step-8 canonicalization.

### Derivative locator / assurance / historical

- `DEV/PROJECT_MAP.md`, `CANONICAL_ARCHITECTURE_INDEX.md`, roadmap and umbrella S6D plan are routing/status only;
- House-Rules Step-2 evidence delta and Steps 4–7 are assurance/derivation;
- the pre-repair S6D-09 candidate/collaborative spatial statements are superseded by the later repair.

### Machine/test evidence

- House-Rules Markdown/sidecar templates and `house_rules_policy.schema.yaml` / `player.schema.yaml`;
- `activity-parameter-spec.schema.json`, `activity-parameter-binding.schema.json`, `invocation-fact.schema.json`, ActionRequest/Resolution/Continuation schemas;
- selected package `character-capabilities.json` and its three identity-bound content members;
- `mechanical-surfaces.json`, `activity-primitive-contracts.json`, `domain-rules-coverage.json` and their validators/tests;
- focused House-Rules, S6D-04/05/09 and Step-3 accepted-work tests.

All correctness claims below were reconciled against actual owners rather than locator summaries.

## 3. Exact current boundary census

### 3.1 Active richer parameter edges

The selected package contains exactly two active `INVOCATION_ADJUDICATED` parameter declarations:

| Edge | Type/bounds | Consumer route |
|---|---|---|
| `activity.check.generic -> dc` | single required integer, `1..30` | `op.roll -> op.resolve_check` |
| `activity.save.generic -> dc` | single required integer, `1..30` | `op.roll -> op.resolve_save` |

No adjudicated parameter exists in `character-mvp-seed.json` or `health-effects-recovery-seed.json`.

### 3.2 Active boolean fact edges

`fiction.target_reachable` is active only for seven exact `op.select_targets` consumers:

1. `activity.attack.ranged_weapon`;
2. `activity.spell.fire_bolt`;
3. `activity.spell.poison_spray`;
4. `activity.spell.thunderclap`;
5. `activity.spell.acid_splash`;
6. `activity.spell.magic_missile`;
7. `activity.spell.burning_hands`.

`fiction.target_visible` remains dormant/nonselectable.

Therefore:

```text
ACTIVE_ADJUDICATED_CONSUMER_KEYS = 9
```

### 3.3 Current supported policy-realization set

The shipped campaign template contains:

```yaml
policies: []
```

No current campaign policy or realization edge is shipped by the built-in package.

```text
CURRENT_SUPPORTED_POLICY_REALIZATION_KEYS = 0
```

Positive realization examples are necessarily `CONFORMANCE_ONLY_NONSELECTABLE`. They prove linkage and rejection rules but do not become policy, package content or product support.

## 4. Evidence ledger

| ID | Current evidence | Disposition |
|---|---|---|
| HRB-01 | One-off Master ruling may proceed without durable adoption. | INHERITED / prove typed handoff. |
| HRB-02 | Engine-owned facts/RNG/state cannot enter through adjudication. | INHERITED / negative test. |
| HRB-03 | Richer input uses declared bounded Activity parameters. | ACTIVE / two exact DC edges. |
| HRB-04 | Registered facts stay boolean and exact-consumer-bound. | ACTIVE / seven reachability edges. |
| HRB-05 | Accepted inputs freeze across retry/suspension/recovery. | INHERITED / Resolution+Continuation proof. |
| HRB-06 | Live adjudication authority differs from policy adoption. | INHERITED / authority walkthrough. |
| HRB-07 | Durable policy is exact Markdown+sidecar at one campaign revision. | INHERITED / exact-reference gap below. |
| HRB-08 | `realization_refs` are linkage, not execution authority. | ACTIVE CONTRACT / no current supported edge. |
| HRB-09 | Missing/stale/incompatible realization fails finitely. | ACTIVE CONTRACT / conformance proof missing. |
| HRB-10 | Contextual policy may stay prose-native and lower through typed input. | INHERITED / no DSL. |
| HRB-11 | Later policy publication is forward-looking. | INHERITED / recovery walkthrough. |
| HRB-12 | Policy is eligible data, not higher instruction authority. | INHERITED / negative walkthrough. |
| HRB-13 | No duplicate owner, policy frontier, scheduler or campaign scan. | INHERITED / negative contract. |

Unaccounted obligations: **0**.

## 5. Concrete contract gaps

### G1 — no finite bidirectional integration ledger

The nine active consumer edges are derivable from package/catalog sources, but no S6D-10 machine artifact states and verifies the equality. This permits future drift between the House-Rules boundary and active S6D consumers.

Resolution: create a non-owner integration ledger and strict schema/validator. The ledger cites owners; it does not become policy or execution authority.

### G2 — policy basis references do not prove exact revision

`activity-parameter-binding.schema.json` currently accepts arbitrary nonempty strings such as `house-rule.social-leverage@rev-3`. The accepted House-Rules owner requires stable `policy_id` plus exact campaign revision. `rev-3` is neither mechanically exact nor currentness-verifiable.

Resolution: retain the accepted `array[string]` shape but define one strict `policy-basis-ref` string contract:

```text
<stable policy_id>@<exact 40- or 64-hex campaign revision>
```

This is a causal reference, not copied policy authority.

### G3 — boolean facts cannot explicitly retain an applied policy basis

`invocation-fact.schema.json` retains provenance, consumer/binding and rules-context fingerprints but has no explicit policy-basis reference. A fingerprint proves equality but cannot by itself identify the exact durable policy basis required for historical explanation/recovery when policy materially influenced the fact.

Resolution: require `policy_basis_refs` on every accepted invocation fact. The array is empty for a one-off fact with no durable policy and contains strict exact references when current policy materially contributed. The fact remains boolean, embedded and nonauthoritative.

### G4 — realization linkage lacks fail-closed machine conformance proof

The sidecar intentionally keeps `realization_refs: array[string]`, but current tests prove only field presence and prose invariants. They do not prove current selected-context resolution, definition kind, exact active consumer admission or rejection of missing/dormant/quarantined targets.

Resolution: the integration validator checks conformance fixtures against the selected package closure and active exact consumers. Current supported set remains empty. No generic realization-status registry or authoring subsystem is introduced.

### G5 — stale Step-3 invocation-fact fixture

`test_step3_execution_value_schemas.py` still constructs the pre-S6D-09 fact shape and therefore no longer matches current required consumer/binding/rules-context fields.

Resolution: update the fixture while touching this contract. This is conformance maintenance, not a semantic change.

## 6. Alternatives

### A — documentation/test assertions only

Keep current schemas and add prose explaining exact policy revisions.

Benefit: smallest edit.

Failure: arbitrary policy ref strings and policy-influenced fact recovery remain underconstrained; the test would assert intent rather than contract.

### B — narrow typed reference + integration ledger/validator (recommended)

Add a strict reusable policy-basis reference, extend embedded facts with explicit policy refs, and add one non-owner integration ledger/schema/validator/test.

Benefit: closes exact identity, equality, negative realization and retry/recovery proof without changing product semantics or execution authority.

Cost: a small schema amendment and one integration contract family.

### C — structured policy engine / homebrew package subsystem

Compile prose or persist generalized policy execution state.

Rejected: duplicates existing owners, exceeds current product scope, creates an arbitrary execution surface and violates YAGNI.

## 7. Analytical challenge

Strongest opposing case against B: `rules_context_fingerprint` already freezes effective context, so explicit policy refs and a ledger may look redundant.

Response: a fingerprint provides equality/currentness detection but not an inspectable reference to the exact policy revision required by the accepted House-Rules causal/evidence model. The narrow ref adds dereferenceability without copying policy. The ledger is verification-only and prevents active-consumer drift; it owns no runtime state.

Simplest viable comparison: A is simpler but fails G2/G3/G4. B is the least complex option that satisfies the accepted exact-revision and finite-gap laws. C is speculative.

Failure attacks:

- same policy ID at a different campaign revision;
- policy ref using `rev-3` or a mutable label;
- exact ref to absent definition;
- exact ref to quarantined primitive ID;
- cross-consumer reuse of a reachability fact;
- later policy supersession during suspension;
- empty policy refs for lawful one-off adjudication;
- policy-like imperative text attempting instruction escalation.

No attack requires new product semantics.

## 8. Step-2 gate

Source Manifest complete: **YES**

Enumerated boundary obligations accounted: **13/13**

Active adjudicated consumer edges accounted: **9/9**

Current supported realization edges accounted: **0/0**

Conformance-only realization fixtures separated: **YES**

Material human decision required: **NO**

Step 3 may record the no-decision result and recommend Alternative B.

