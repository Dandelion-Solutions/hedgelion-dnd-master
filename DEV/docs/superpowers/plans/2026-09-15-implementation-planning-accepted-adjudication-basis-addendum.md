# HDM Implementation Planning — Accepted Adjudication Basis / Retry / Recovery

Status: **CURRENT MANDATORY PLANNING AMENDMENT — EXECUTION NOT AUTHORIZED**
Date: 2026-09-15
Finding origin: **AUTHOR FINDING 62 — SIGNIFICANT**.

## 1. Exact defect and owner boundary

HOUSE_RULES_MECHANICAL_BOUNDARY sections3/6/8 and CAMPAIGN_HOUSE_RULES HR-17/section15/section19 already require exact policy-source resolution before acceptance, full accepted binding/fact identity and frozen historical retry/recovery. Implementation Planning explicitly owns production RuntimeCommand/idempotency realization. RD-05's generic accepted-ID/RNG cases, RD-06's generic required closure and RD-07's generic recovery cases do not name this source-resolution/accepted-input join. PG23 reconstructs catalog definitions, not policy adoption/meaning. The static S6D-10 fixture round-trips JSON and validates supplied resolver evidence; it is not the production resolver, RuntimeCommand fingerprint, publication or cold-recovery mechanism.

This amendment adds the exact task-owned producer/consumer and witness joins. It preserves Step-3 identity/retry order; Step-5.6 publication; Step-5.7 recovery; House-Rules policy/adoption; ACCESS_CONTROL authority; S6D typed parameter/fact validation; and RD-15 exact SUPPORTED catalog binding. Policy interpretation/applicability remains with existing semantic owners. No prose compiler, deterministic policy-meaning engine, policy registry/frontier, new permission or generic workflow is introduced.

## 2. Bounded exact-source resolver

Extend the existing RD-07 recovery/publication-history adapter in GAME/TOOLS/recovery.py with the bounded policy-basis resolution needed by RD-05. This is an early owner-local part of RD-07 Task2, separate from full current-root hydration and accepted-execution recovery. It consumes the fixed gameplay Connector read boundary and exact pinned source evidence; it neither implements a transport nor requires a running executor/HOT store.

For every materially used durable policy ref, preserve the existing policy_id@exact_campaign_revision grammar (40 or64 lowercase hex commit). Resolve the paired RULES/HOUSE_RULES.yaml and its declared normative Markdown/anchor at that same exact campaign revision; verify the policy ID and owner-valid adoption/authority/applicability evidence through the existing owners. Locator syntax, path existence or caller-supplied authority_validated/applicable booleans alone do not establish this evidence. The resolver returns a typed resolved result or existing finite failure, not unvalidated evidence passed through to acceptance.

The source reader may reuse already verified exact revision bytes. Load only the distinct exact revision/policy dependencies actually required by the bounded request; do not discover all policies/history/refs, refresh every turn or introduce a current global policy frontier. A valid one-off adjudication has the required empty policy_basis_refs array and requires no durable-policy read. Conflicting, missing, unavailable, stale, inapplicable or unauthorized evidence follows existing owner failure vocabulary and blocks the affected acceptance/recovery path; never replace a missing historical source with current HEAD or a fabricated empty array.

New prepared work uses current owner-valid policy/authorization evidence. Existing accepted execution resolves its frozen historical policy/input basis. A later adopter deactivation/grant revocation does not invalidate previously lawful adoption; current operation authority remains separately enforced by its native owner. Unresolved creator authority is denied under the existing gate; this amendment selects no creator identity or placement.

## 3. RD-05 accepted-input and idempotency join

Extend RD-05 Tasks1/3/5 and GAME/TOOLS/runtime_execution.py. Before accepting a new applicable command/constructing its Resolution, consume actual resolved policy evidence plus the exact current declared parameter/fact consumer validation and the existing RD-15 SUPPORTED binding where required. Policy prose/sidecar/linkage cannot execute an Activity, create an undeclared parameter/fact, select RNG or mutate state. All external source reads and semantic preparation remain outside the HOT mechanic transaction.

The complete accepted richer binding and invocation fact include value, provenance/eligibility/binding/rules fingerprints as applicable and unique Unicode-code-point-sorted policy_basis_refs. Keep the required array even when empty; missing is not empty, and a missing fact is not false. The existing Step-3 canonical RuntimeCommand input_fingerprint includes this complete mechanically relevant accepted value. Changing only a policy ref for the same command/resume identity must return the existing idempotency-conflict outcome before RNG or mutation. The S6D-10 conformance hash helper is not a new runtime fingerprint owner.

Perform existing-identity lookup before ambient rebinding. Exact retry returns stored result/current suspension and accepted inputs; no current-policy reinterpretation or policy-HEAD reread for that purpose. New hydration may acquire a frozen historical dependency, but cannot change the accepted fingerprint. Copy the same accepted input/ref values through Resolution, child Resolution where applicable, Continuation, downstream evidence adapters and retained retry/recovery. A divergence is a typed integrity/idempotency failure, not permission to rebind, reroll, re-ID or replay an accepted segment.

## 4. RD-06 publication and RD-07 cold recovery

Extend RD-06 Tasks2–4 and existing GAME/TOOLS/durability.py / publication.py only where their adapter needs the exact accepted dependencies. The frozen correctness-required closure includes accepted parameter/fact values and their reconstructive historical policy dependencies; existing retained source refs are dependencies, not a request to rewrite old policy bytes or copy policy meaning into runtime records. Publication retry/currentness reconciliation preserves the accepted identity/result/basis. An omitted required carrier/dependency or unresolvable basis cannot be reported durably recoverable. Successful remote acceptance remains accepted even when later local adoption fails; no blind repeat.

Extend RD-07 Task4 in GAME/TOOLS/recovery.py. Select current native operational roots/sources using existing F58/F30 routing, hydrate the accepted native Resolution/Continuation and resolve only their exact frozen policy dependencies through the same bounded resolver. Validate complete accepted inputs, fingerprint/catalog basis and required evidence before resume. The actual RD-05 resume path consumes retained RNG/result/segment evidence; a later policy revision, grant change or narration failure cannot replace the prior basis. Missing exact historical evidence yields the existing finite blocked/unavailable result, without current-HEAD substitution, model-memory reconstruction, reroll or gameplay mutation.

The initial current-native source pin required by normal recovery remains valid. The prohibition concerns rereading current policy HEAD to reinterpret accepted work; it does not forbid owner-required current-source/authorization checks or exact historical hydration. No permanent all-policy snapshot, new durable policy record, generic retention graph or new publication protocol is added.

## 5. Exact task-owned witnesses

Create each class only in its owning RED-to-GREEN task after its declared prerequisites. Use the actual shipped resolver/executor/publication/recovery adapters with exact revision fixtures and a controlled fixed-Connector boundary; do not mock the mechanism under proof into success booleans. Present source-only fixtures cannot substitute for these later integrated targets.

| Exact module/class | Primary channel | Required cases |
|---|---|---|
| DEV/TESTS/test_rd07_recovery.py::ExactPolicyBasisResolutionTests | FOCUSED_BEHAVIOR + INTEGRATION_SCENARIO | Exact paired source/sidecar/revision/anchor and policy ID; owner-validated adoption/authority/applicability; mixed revision, missing/unavailable source, absent anchor, unauthorized/inapplicable/conflicting basis; legal empty one-off basis; no ambient HEAD/all-history fallback; bounded reads/cache reuse per exact dependency. |
| DEV/TESTS/test_rd05_runtime_execution.py::AcceptedAdjudicationBasisTests | INTEGRATION_SCENARIO | Actual resolver and typed consumer gate before acceptance/RNG/mutation; full binding/fact fingerprint including only-policy-ref change; sorted unique/missing/empty array; duplicate exact invocation returns accepted work; current-policy change does not rebind accepted work; complete Resolution/Continuation/child/adaptor preservation; missing fact versus false; no undeclared/dormant/realization-link execution. |
| DEV/TESTS/test_rd06_durability_publication.py::AcceptedAdjudicationPublicationTests | INTEGRATION_SCENARIO | Actual accepted command/Resolution/Continuation -> frozen required closure -> publication/indeterminate reconciliation; omitted carrier/dependency blocks false success; accepted basis and RNG/result unchanged on retry and after remote success/local failure. |
| DEV/TESTS/test_rd07_recovery.py::AcceptedAdjudicationRecoveryTests | INTEGRATION_SCENARIO | Actual native root/source selection -> exact accepted carriers -> historical policy resolution -> RD-05 resume; fresh-process/no cache path after newer policy publication; same accepted fingerprint/RNG/result; changed ref conflict; unresolvable historical basis blocked; no latest-policy fallback or mutation before validation. |

The parameter and fact route cases must enumerate the identity-verified source-derived edge keys individually, not accept a total count: parameter:activity.check.generic:dc and parameter:activity.save.generic:dc; fiction.target_reachable for activity.attack.ranged_weapon, activity.spell.fire_bolt, activity.spell.poison_spray, activity.spell.thunderclap, activity.spell.acid_splash, activity.spell.magic_missile and activity.spell.burning_hands. Each edge must reach its actual declared consumer/accepted carrier and the relevant negative. The two exact-consumer fixtures from S6D-10 remain minimum retry/recovery regression cases; their obsolete future_rng_frontier fixture field follows RD-05's already accepted contract cutover and is not restored. Extend item enumeration only on an accepted source-owner consumer change.

The third S6D route, policy realization-link conformance, remains nonselectable with zero actual built-in realizations. Keep its three exact link-shape fixtures under static conformance; they neither invoke targets nor substitute for production acceptance/recovery. The first real admitted realization retains its existing separate trigger.

Commands only during authorized implementation/proof execution:

~~~bash
python3 -m unittest DEV.TESTS.test_rd07_recovery.ExactPolicyBasisResolutionTests -v
python3 -m unittest DEV.TESTS.test_rd05_runtime_execution.AcceptedAdjudicationBasisTests -v
python3 -m unittest DEV.TESTS.test_rd06_durability_publication.AcceptedAdjudicationPublicationTests -v
python3 -m unittest DEV.TESTS.test_rd07_recovery.AcceptedAdjudicationRecoveryTests -v
~~~

PG37 names this exact integrated chain. R041 ExecutionRetryProofTests consumes the applicable actual acceptance/publication/cold-recovery witnesses while retaining its original stale-Continuation/child-crash duties. No new readiness ID, count-only closure or premature runtime PASS is introduced.

## 6. Checkpoint and version integration

| Prerequisites | Checkpoint | Relation |
|---|---|---|
| Existing exact-source reader contract and current policy/adoption/typed-evidence owners | RD07_POLICY_BASIS_RESOLVER_READY | Bounded early RD-07 Task2 resolver and exact-source fixtures. Does not wait for full recovery, RD-05 execution or generated runtime output. |
| RD07_POLICY_BASIS_RESOLVER_READY + existing RD05 lifecycle/identity and RD15 supported-binding local contracts | RD05_ACCEPTED_ADJUDICATION_BASIS_READY | Actual accepted-input/fingerprint integration. New source resolution precedes acceptance; existing identity lookup precedes ambient rebinding. |
| RD05_ACCEPTED_ADJUDICATION_BASIS_READY + existing RD06 frozen publication/execution-SAVE join | RD06_ACCEPTED_ADJUDICATION_PUBLICATION_READY | Actual required-closure/publication integration proof; no whole-RD barrier. |
| RD07_POLICY_BASIS_RESOLVER_READY + RD05_ACCEPTED_ADJUDICATION_BASIS_READY + existing RD07 accepted/native-root recovery and RD06 publication targets | RD07_ACCEPTED_ADJUDICATION_RECOVERY_READY | Actual cold hydration/resume after accepted publication fixtures. No reverse prerequisite from full recovery to the early resolver. |
| Four exact task-owned target/proof results above | ACCEPTED_ADJUDICATION_BASIS_PROOF_READY | Terminal PROOF_AFTER_TARGET / PG37 sink; never an execution prerequisite. |

Runtime evidence-before-acceptance is a per-attempt law, not a new scheduler. The bounded early resolver depends only on exact native source/owner contracts, which makes the split substantive; full restoration consumes accepted execution later.

Future edits extend only existing planned GAME/TOOLS/runtime_execution.py, recovery.py, durability.py and publication.py plus their named RD-05/RD-06/RD-07 test modules. RD-15 and access/policy owners remain consumed contracts; no new engine, module, schema, durable field, record family, allocator, route, CORE final writer or blank scaffold is introduced. Existing parameter/fact schemas already retain policy_basis_refs and applicable full binding fields; planned final retained-schema/CORE/catalog integration targets remain unchanged. Version Impact: NONE for this planning repair. A concrete later incompatible owner/schema delta must return to its native owner; no invented version, digest, migration or release action here.
