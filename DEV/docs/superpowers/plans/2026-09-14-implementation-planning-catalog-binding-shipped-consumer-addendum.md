# HDM Implementation Planning — Catalog Binding Shipped-Consumer Cutover Addendum

Status: **AUTHOR GRAPH REPAIR — MANDATORY OVERLAY / PLANNING ONLY / NO PRODUCTION IMPLEMENTATION**
Date: 2026-09-14
Finding: **AUTHOR GRAPH FINDING 14 — SIGNIFICANT**

This addendum repairs a shipped-instruction half-cutover discovered after RD-15 was introduced. It does not create new catalog semantics, rules authority, readiness IDs, product policy or architecture. It makes existing shipped gameplay instructions conform to the already-canonical Step-3 deterministic binder and catalog-resolution laws realized by RD-15.

Production implementation remains **NOT AUTHORIZED**.

## 1. Root cause

The canonical execution boundary requires:

```text
LLM semantic interpretation / bounded semantic choice
-> deterministic validation against the SAME accepted ResolvedCatalogContext
-> only then RuntimeCommand acceptance / deterministic execution
```

The LLM may not establish an unchecked executable/entity ID or an executable primitive absent from the loaded catalog. Catalog discovery/search/model memory is not authority.

Current shipped gameplay prose contains a competing route in three current consumers:

- `GAME/CORE/PLAY_POLICY.md` — rules decision order permits model rules knowledge followed by a quick fair local ruling when exact RAW is unavailable;
- `GAME/CORE/CORE_INDEX.md` — repeats that route and states that the chosen quick ruling is then executed;
- `GAME/CORE/ADJUDICATION.md` — permits model D&D knowledge plus a smallest fair ruling and then carries the accepted gameplay consequence forward.

That prose is valid only for bounded semantic/adjudicative judgment that does **not** invent a new executable primitive or bypass deterministic catalog legality. Without an explicit fence, it permits a direct prose/model-memory path around RD-15 into mechanics/execution.

## 2. Exact semantic correction

The v1 shipped rule is:

```text
fictional intent / semantic adjudication may be local-first
BUT
any material executable mechanic/capability/definition used by deterministic execution
must bind to an exact supported primitive/definition under the same accepted BoundCatalogContext
before RuntimeCommand acceptance.
```

Therefore:

1. model rules knowledge may help interpret intent, choose among bounded candidates, establish owner-admitted invocation facts, or make a one-off fiction/semantic ruling within already-supported capability;
2. a quick/local ruling may decide fiction-facing semantics such as approach, DC/classification or consequence framing only where the applicable owner admits that judgment;
3. neither model memory nor a local ruling may create an executable Activity/primitive/definition absent from the loaded exact catalog;
4. approximate/noncanonical player wording remains legal input and may be semantically normalized, but the normalized execution target must pass RD-15 deterministic ID/kind/capability validation;
5. a search miss, unknown phrase or remembered rule is not by itself `unsupported`;
6. when deterministic same-context validation establishes that the requested mechanic is not expressible, route to RD-15 `UNSUPPORTED` / `runtime.catalog_gap_report`; do not create a RuntimeCommand and do not improvise a mechanically equivalent hidden primitive;
7. when a request is fictional/nonmechanical and requires no executable primitive, RD-15 does not manufacture a catalog dependency merely because prose adjudication occurred;
8. external RAW research policy remains unchanged: lack of automatic web research does not grant model memory execution authority.

This preserves local-first play while restoring the accepted LLM/deterministic authority boundary.

## 3. Mandatory RD-15 shipped-consumer checkpoint

RD-15 gains one mandatory shipped-instruction cutover checkpoint after the deterministic candidate-validation contract is defined and before its full integration proof may close.

### Files

Modify together:

```text
GAME/CORE/PLAY_POLICY.md
GAME/CORE/CORE_INDEX.md
GAME/CORE/ADJUDICATION.md
DEV/TESTS/test_rd15_catalog_runtime.py
```

Inspect only for contradiction, and modify only if the exact current wording still creates an alternate bypass:

```text
GAME/CORE/RUNTIME.md
GAME/CORE/MECHANICS_INTEGRITY.md
GAME/CORE/AI_REASONING.md
```

Current author audit found no competing executable-primitive authority in the latter three; implementation currentness must re-check rather than blindly edit them.

### Required prose effect

The three changed files must state consistently that:

```text
player prose / approximate terminology
-> semantic intent/adjudication
-> exact catalog bind when material deterministic mechanics are required
-> SUPPORTED -> deterministic execution
   OR
   UNSUPPORTED / INVALID -> typed non-execution path
```

No active instruction may retain a shorter path equivalent to:

```text
model remembers plausible mechanic
-> quick ruling
-> execute as mechanic
```

A quick fiction ruling that does not instantiate a catalog mechanic remains lawful.

## 4. Focused proof

Add `CatalogBindingInstructionCutoverTests` to `DEV/TESTS/test_rd15_catalog_runtime.py`.

Required assertions:

```text
test_play_policy_local_first_does_not_bypass_catalog_binding
test_core_index_rules_route_requires_exact_bind_before_mechanical_execution
test_adjudication_local_ruling_cannot_invent_executable_primitive
test_noncanonical_player_wording_can_map_to_supported_exact_primitive
test_fiction_only_ruling_does_not_require_fake_catalog_primitive
test_search_miss_or_model_memory_is_not_unsupported_proof
test_deterministically_unsupported_mechanic_creates_no_runtime_command
test_no_active_core_consumer_admits_model_memory_as_executable_catalog_authority
```

The final negative scan must be semantic/exact, not a broad ban on words such as `model`, `local ruling`, `knowledge` or `RAW`; those concepts remain valid in their admitted roles.

Focused verification:

```bash
python3 -m unittest DEV.TESTS.test_rd15_catalog_runtime.CatalogBindingInstructionCutoverTests -v
python3 -m unittest DEV.TESTS.test_rd15_catalog_runtime.CatalogCandidateValidationTests -v
```

RD-15 full integration proof cannot close unless this shipped-consumer checkpoint is green.

## 5. Shared-writer / ordering rule

RD-01 Task 3 may inspect `GAME/CORE/**` for R033/R050 stale projections, but Finding 14 does not transfer catalog-binding semantics to RD-01.

If RD-01 currentness work also needs to edit any of the three Finding-14 files, do not create two independent final writers. The execution schedule must consolidate the exact file into one ordered/coherent checkpoint or rebase the later writer on the already-green earlier checkpoint and preserve both requirement sets.

The catalog-binding semantic acceptance for these exact lines remains RD-15 + this addendum.

## 6. Version / migration

This is an unreleased v1 shipped-instruction cutover. Legacy v0.8 wording is not a preservation constraint and requires no compatibility shim or migration.

At implementation, apply the normal module Version Impact Gate once per materially changed shipped file after all same-checkpoint edits are known. Do not double-bump a file solely because multiple repair findings are consolidated into one final v1 edit.

## 7. Coverage / disposition

```text
AUTHOR_GRAPH_FINDING_14:
  classification: SIGNIFICANT
  root_cause: shipped instruction route bypasses deterministic catalog binding
  canonical owners:
    Step-3 deterministic execution boundary §§6.1-6.2
    CATALOG_RESOLUTION.md §9
    RD-15 catalog binding realization
  shipped consumers:
    PLAY_POLICY.md
    CORE_INDEX.md
    ADJUDICATION.md
  proof:
    RD-15 CatalogBindingInstructionCutoverTests
  readiness treatment:
    post-WP27 author graph repair; do not invent a fake R27-R###
```

```text
AUTHOR_GRAPH_FINDING_14: REPAIRED_IN_PLANNING
ARCHITECTURE_REOPEN_REQUIRED: NO
HUMAN_DECISION_REQUIRED: NO
PRODUCTION_IMPLEMENTATION_AUTHORIZED: NO
INDEPENDENT_CONFIRMATION: PENDING
```
