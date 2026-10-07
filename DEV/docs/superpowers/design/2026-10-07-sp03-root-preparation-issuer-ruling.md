# SP03 source-bound root preparation issuer — independent Senior ruling

Status: **BOUNDED GO; CANDIDATE REPAIR REQUIRED**
Reviewed source: `5e9b678ef9b32282c02112de4b74a1a8d0f7cffb`
Independent Senior: `ses_ee7c842a8ffeT1mWXHVxVVA1bq`
Date: 2026-10-07

This resolves the selector review's F1 technical gap within the accepted SP03
preparation contract. It grants no native acceptance, mutation, RNG, publication,
production activation or full SP03 readiness. NEEDS_PO: NONE.

## Finding

The plan permits source-backed conformance before SP04 but the actual
`NativePreparationContext` has no authentic issuing factory/lineage. Its reusable
module seal and arbitrary builder token validate structure, not issuance. DAG
registration from `__post_init__` lets `dataclasses.replace` invent occurrence,
child Resolution and observation provenance. A compiler nested consumer is not
proof that a distinct child Resolution was accepted.

Anchors on the reviewed base: `activity_contracts.py:432–438,1848–1932`;
`runtime_execution.py:1115–1307`; `runtime_host.py:1669–1685`;
`current_owner.py:192–331`; stable plan:1452–1473,1615–1621.
Actual constructor shortcuts occur in `test_local_spell_context_cast.py`,
`test_sp03_native_membership.py` and the unaccepted DAG test, rather than in the
pinned `sp02_installed_test_support.py`.

## Minimum permitted route

Add an internal read adapter on the existing bound `CurrentOwnerView`, for example
`_prepare_root_context(catalog, compiled, *, command_id, consumer_id,
adjudication_basis=None)`. Preserve the planned public `evaluate_selector` ABI.

The adapter obtains the existing host operation internally, reads native
`runtime.command`, derives and reads its root `runtime.resolution`, and reacquires
the required exact subject union through the existing P0 source route. Validate
owner envelope/state, applicable accepted action, retained catalog/candidate and
acceptance fingerprints, command/root/Activity/Actor/source/targets/parameters and
typed identities/generations together. Initial unadvanced roots may be supported;
unproved resumed/segmented/fixed-roll cases hold.

Derive the exact compiler occurrence and native role bindings from accepted
invocation and compiled contracts; do not accept arbitrary occurrence strings,
ExecutionRefs or caller role mappings. Ambiguous target/source/payer or arbitrary
Asset bindings hold. Genuine resolver-issued applicable adjudication must agree
with retained command parameters/facts; derive canonical policy references.
Prospective documents, allocation handles and unsupported fixed rolls remain
empty. There is no caller-selected backend/path/reader or substitute operation.

An installed test may seed a small real immutable native source with an actual
`accept_command` result, explicitly declared native root-Resolution input and
Actor/Effect/Asset records. The GAME issuer reads them, not test-provided mappings.
This proves read/preparation over a conformance source, not creation/persistence/
atomic acceptance/recovery of that command or Resolution.

## Issuance and child boundaries

Remove authority registration from `NativePreparationContext.__post_init__`.
Only the source-bound issuer records the exact context object, read adapter,
operation/session/observation/source basis, catalog/compiler, native accepted
command/Resolution identities and immutable inputs, derived consumer/occurrence/
roles, adjudication/facts/policy and preparation-only scope. A weak lookup indexes
authentic unchanged issued contexts; it never grants issuance.

Enforce the same predicate at selector lookup/evaluation, cache identity and
membership acquisition/revalidation. Cache structural validation copies do not
register or inherit issuance. Direct construction, copied seals, copy/replace,
post-issuance mutation and cross-context rebinding reject.

Root DAG preparation is eligible. Nested instruction preparation within that root
is eligible only with retained scope/binding/input proof; it does not prove a
branch was reached or create a child Resolution. Distinct child/reaction/trigger
Resolution preparation holds without native causal acceptance evidence. A bare
child ID list, nonempty causal string or caller-event ExecutionStore record is
not sufficient. Production child creation joins SP04 and later native owners.

Replace counterfeit child-positive conformance with genuine root/nested-root
witnesses and explicit forged-child negatives. Preserve the structural binding
law at its proper test layer; do not delete invariant tests to bypass it.

## Exact allowed repair envelope

- `activity_contracts.py`: genuine preparation issuance/checks; shape separate.
- `mechanical_context.py`: issuance/cache/occurrence/evaluator checks.
- `mechanical_sources.py`: issuer enforcement, preserving source coverage rules.
- `runtime_host.py`: minimum private bound read/preparation adapter only.
- `test_sp03_selector_dag.py`, `test_sp03_native_membership.py`,
  `test_local_spell_context_cast.py`: authentic positives and adversarial cases.
- `test_local_spell_closed_contracts.py`: necessary structure/authority distinction.
- `test_runtime_host_composition.py`: source-operation/no-mutation proof.
- A small DEV-only helper may call the GAME issuer, but cannot become the issuer.

P0/compiler/acceptance/storage/policy APIs are reuse/inspect-only. No dispatcher,
NativePlanBuilder or new ExecutionService is introduced. Reopen for changed
source/admission/causal meaning, new persistent acceptance/lineage/epoch state,
generic caller-authority issuer, broad ordinary scans, wider host dispatch,
evaluator ABI changes or weakened invariants.

Required proof: actual installed compiler/source-root/issuer/selector path;
constructor/copy/replace/mutation and cross-session/campaign/catalog/consumer
rejections; invented occurrence/child/causal-key rejection; missing/foreign/stale
native command/Resolution hold and fresh reissue; no cache-side issuance;
membership rejects unissued contexts; reverified actor/target F2 projection;
zero writes, admission, RNG, allocation, events/receipts, spend or establishment.

## Version and continuation

VERSION_IMPACT: NONE for this development-only review record. Actual repair:
`activity_contracts` 1.0.7 -> 1.0.8 and `mechanical_context` 1.0.2 -> 1.0.3
cover the same unpublished DAG slice; `mechanical_sources` 1.0.1 -> 1.0.2;
`runtime_host` 1.0.17 -> 1.0.18. No identified catalog/profile/persistent/campaign/
storage/custom-digest bump; reassess actual scope.

Next: one coherent source-bound root issuer + all consumer/test synchronization,
frozen independent F1/F2 re-review, exact SP03 command, final integration/version/
full regression/audit/build/publication/read-back. Candidate remains unaccepted;
policy math, remaining DAG branches and cast preflight remain SP03 obligations.
