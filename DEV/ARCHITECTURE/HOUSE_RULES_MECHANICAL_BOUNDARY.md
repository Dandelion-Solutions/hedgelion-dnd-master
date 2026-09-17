# House-Rules Mechanical Boundary Integration

Status: **CANONICAL S6D-10 OWNER — STEPS 1–8 COMPLETE / WHOLE-PROJECT REVIEW PASS**

## 1. Authority

This document owns only the integration contract between accepted Campaign House-Rules/adjudication semantics and current typed deterministic consumers. Policy meaning/adoption remains in `CAMPAIGN_HOUSE_RULES.md` and `ACCESS_CONTROL.md`; execution, catalog, state, RNG, publication and recovery remain with their existing owners.

## 2. Central law

```text
eligible semantic judgment
-> exact declared typed accepted input
-> exact current consumer/catalog/native-owner validation
-> deterministic result or finite typed failure
```

Policy prose, sidecar entries and realization references never execute code, select RNG, manufacture capability or mutate canonical state.

## 3. Exact policy basis

Every durable policy materially used by an accepted adjudicated parameter or fact is retained as:

```text
policy_id@exact_campaign_commit
```

The exact grammar is owned by `policy-basis-ref.schema.json`; it proves locator shape, not policy existence. Before acceptance a production `PolicyBasisResolver` boundary must prove the exact revision, paired sidecar/normative anchor, policy ID, adoption authority and applicability. The resolver is a verifier/adapter over existing campaign-currentness, House-Rules and Access-Control owners; it is **not** a new policy, publication, authorization or currentness authority.

The accepted runtime realization is:

```text
trusted selected campaign + exact pinned authoritative revision H
+ authenticated RepositoryPort-equivalent exact commit/tree/path reads at H
+ trustworthy acting-principal evidence
+ current creator/PLAYER policy-adoption evidence when required
+ selected BoundCatalogContext when realization_refs are mechanically material
-> exact-read RULES/HOUSE_RULES.yaml and its source_path at H
-> validate unique active policy_id, matching normative anchor, authority class,
   adoption basis, adopter attribution, applicability and required realization linkage
-> ephemeral verified ResolvedPolicyBasis
-> accepted policy_id@H refs + accepted parameter/fact values participate in RuntimeCommand identity
```

Raw caller assertions such as `authority_validated=true`, `applicable=true`, caller-selected source paths or an asserted campaign revision are never authority evidence. `DEV/TOOLS/validate_house_rules_mechanical_boundary.py` remains development/conformance proof and must not be promoted into the gameplay trust boundary.

The verified resolver result is ephemeral. It does not create a persistent policy-proof registry, policy epoch, ACL copy or additional policy owner. Python object/type construction alone never proves trust; trust derives from exact pinned owner reads plus the owning authorization/currentness checks on the supported runtime path.

The accepted array is empty when no durable policy materially contributed. Retry/recovery resolves the frozen historical revision from the accepted `policy_id@H` basis and does not rebind accepted work to current/latest policy or current grants. Later publication or grant changes are forward-looking and do not rewrite accepted work.

This contract assumes supported HDM campaign publication/currentness paths are the admitted authority-changing paths. Arbitrary out-of-band repository mutation is integrity/tamper evidence requiring normal currentness/integrity handling; technical Git write capability does not become gameplay policy authority.

## 4. Active adjudicated surface

The identity-bound built-in package candidate has exactly two bounded DC parameter contracts and the mechanical-surface owner admits seven exact `fiction.target_reachable` consumer edges. Runtime selection remains blocked until S6D-11. `house-rules-mechanical-boundary.json` must equal the complete source-derived normalized rows bidirectionally after candidate identity and every declared content-member digest are verified. Three exact route profiles carry the full cross-owner evidence obligations. The ledger is verification evidence only and grants no authority.

## 5. Policy realization

The built-in template ships no adopted policy; the current supported realization set is empty. Conformance-only fixtures remain nonselectable.

`realization_refs` are linkage only. A current realization must resolve in the selected compatible catalog context to an admitted exact capability/consumer. The built-in package remains subject to its S6D-11 activation gate. A conformance fixture proves only typed link shape against identity-verified candidate bytes; it proves neither admission nor exact-consumer realization and is explicitly nonselectable. Primitive fixtures inspect both selection and realization state. Missing, stale, incompatible, dormant or quarantined references fail finitely. ID resolution alone does not prove semantic equivalence and never invokes the target.

## 6. Retention and failure

Resolution/Continuation retain accepted binding/fact evidence and exact policy refs across suspension/retry/recovery. Binders emit unique policy refs in ascending Unicode code-point order. Their complete accepted value participates in the Step-3-owned retry/idempotency identity; changing any policy ref cannot silently reuse accepted work. The S6D-10 hash helper is conformance evidence only. Missing is not false. Later policy changes are forward-looking. Unauthorized/stale/invalid/conflicting/gap paths use the registered failure vocabulary and fail before RNG or mutation.

## 7. Forbidden authority

No policy engine, prose compiler, generic homebrew subsystem, arbitrary query/payload/path/patch, persistent realization status, global policy frontier, background worker, Signal/StateDelta lifecycle or dormant activation is admitted.

## 8. Verification and deferred trigger

The machine proof must remain exactly equal to the identity-bound candidate parameter contracts and active fact-consumer edges, with route-profile proof coverage and zero current built-in realizations. S6D-11 owns runtime package selection/loader verification. Implementation Planning owns production RuntimeCommand/idempotency realization; acceptance must reproduce the exact-consumer retry/recovery fixtures without rereading HEAD, rerolling or mutating before validation.

## 9. S6D-11 activation

The prior identity-bound package candidate is now a resolved_ruleset_identity bound to canonical `ruleset_set_sha256`. ACTIVE_VERIFIED_MACHINE_CONTRACT means only that the exact built-in package/lock and this boundary's complete source-derived rows passed S6D-11 validation. It does not grant realization, primitive or execution authority. The former candidate `content_set_sha256` and blocked-until-S6D-11 carrier are invalid.
+
