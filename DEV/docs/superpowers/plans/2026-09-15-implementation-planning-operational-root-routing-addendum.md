# HDM Implementation Planning — Operational Root Routing Addendum

Status: **CURRENT MANDATORY AUTHOR REPAIR — PLANNING ONLY**
Date: 2026-09-15
Baseline before publication: 20a3cd0e09025c67fe1a3552214ca6229278d80a
Production implementation authorized: **NO**.

## 1. Defect and accepted boundary

**AUTHOR FINDING 58 — SIGNIFICANT.**

Step-5.2 Laws 2–5/9–11 and section 5 require complete bounded discovery of independently recoverable operational roots. WP-14 Laws 6–8 and R072 consume that requirement. RD-07 Task 2 says to enumerate admitted roots from current routing/lifecycle evidence, but the executable package supplies no non-temporal operational membership producer, physical route contract or producer/publication proof. WP-11 knows the direct path of a supplied runtime ID; it gives these families no discovery index. F6 covers armed temporal owners, a different root class.

A concrete missing path is an active Procedure after its originating Command has settled. A surviving native Procedure body and its known-ID route do not tell a fresh host which Procedure IDs remain independently active. With no checkpoint, HOT or remembered IDs, the planned consumer must invent enrollment, scan historical runtime records, omit work, or block an otherwise healthy promised recovery point.

This repairs realization of existing native-owner laws. R072 already records architecture-blocker PASS. Root eligibility, durability promises, source authority, Procedure lifecycle, identity, temporal ownership and failure semantics remain with their accepted owners. The physical representation below is an active-only, source-partitioned derivative admitted by Step-5.2 Law 4. It adds no semantic family, root snapshot, generic pending-work owner or mutable campaign-global root list.

## 2. Typed root contract and physical representation

### Eligibility and reachability

| Step-5.2 class | Allowed native family | Required membership lifetime |
|---|---|---|
| A | runtime.command | Non-settled command while mandatory unfinished descendant closure remains. A terminal-looking local segment does not settle the root while mandatory children remain. |
| B | runtime.procedure | Active native Procedure independently of Command lifetime. A completed originating Command cannot retire this root. |
| C | runtime.interaction, runtime.intent_plan | Materially unresolved accepted semantics included in an actually promised durability/handoff closure. Mere receipt of a message, unaccepted interpretation or ordinary ephemeral role context creates no promise. |

The initial realization enrolls each eligible member of these four families. Redundant references are permitted; native payload and writable authority are not duplicated. Resolution, Continuation, child/firing/receipt evidence and required accepted interpretation dependencies remain reachable by validated bounded native forward references. A missing required descendant blocks recovery; it is not repaired by replay or by rooting arbitrary history. The deterministic allocator singleton needs no membership entry. Temporal-source routing remains F6/F36 and is not folded into this route.

A class-C route is added as part of the closure that actually protects the accepted point, under Steps 5.4/5.5 and WP-13. No persistent promise flag or handoff ticket is introduced. The current durable route is retained while its native accepted semantics remain materially unresolved; omission from a later, unrelated SAVE scope is not a removal reason. Removal requires owner-proven settlement or an owner-proven sufficient durable replacement with bounded current reachability. Exact message/provenance content remains recoverable when still irreducible; a dangling message ID is insufficient. Routing presence alone proves neither semantic acceptance nor a successful promise.

### Campaign form

Under the existing selected state_root (`STATE` below is the template spelling of that MANIFEST-selected root, not a second hard-coded selector):

| Physical route | Content |
|---|---|
| STATE/RUNTIME/RECOVERY_ROOTS/FORMAT.yaml | Static format marker, local schema_version 1 and document_kind operational_root_route_format. No mutable root list, count, digest, revision frontier or completeness assertion. |
| STATE/RUNTIME/RECOVERY_ROOTS/COMMANDS/RECORDS/... | One derivative membership document for one runtime.command. |
| STATE/RUNTIME/RECOVERY_ROOTS/PROCEDURES/RECORDS/... | One derivative membership document for one runtime.procedure. |
| STATE/RUNTIME/RECOVERY_ROOTS/INTERACTIONS/RECORDS/... | One derivative membership document for one promised unresolved runtime.interaction. |
| STATE/RUNTIME/RECOVERY_ROOTS/INTENT_PLANS/RECORDS/... | One derivative membership document for one promised unresolved runtime.intent_plan. |

A valid blank campaign need not materialize empty Git directories for the four active prefixes. Absence of a prefix is accepted as zero entries only from complete exact-pinned tree/namespace evidence under the valid format contract and producer-coherence rules; a failed, unauthorized, truncated or unresolved read is not that evidence.

The suffix after each family root is exactly the WP-11 route-law suffix calculated with the **original native family_key and complete native identity components**. The physical root prefix changes; identity framing, SHA-256 shard selection, injective base32hex filename chunks and ID allocation do not. These are derivative route entries, not new native family records.

Each membership document has local schema_version 1, document_kind operational_root_route_entry and one typed owner_ref containing only native_family and identity_components. Family/prefix/body identity must agree. The closed family set is the four rows above; native identity policy is validated through the current shared identity contract. No lifecycle value, recovery payload, Procedure resources, RNG, chronology, currentness stamp, accepted-catalog payload or authority grant belongs in an entry.

A continuing eligible owner does not rewrite its byte-identical membership merely because an internal execution value changed. Membership creation/removal is owner-local; unrelated roots have no mandatory shared hot file update. The immutable campaign resulting tree still provides the existing campaign acceptance edge.

### Selected LIVE form

The final RD-09 LIVE envelope has required operational_root_routes: a typed list of the same logical owner_ref values, empty when no LIVE-owned operational root is eligible. Its owning source is implicit in the exact selected LIVE envelope. References resolve to native_state_entries under F31 and the current claim/birth policy. The list carries no campaign mirror of current LIVE payload and creates no new writable scope or source-native allocation policy.

RD-09 remains sole final live_scene.schema.yaml writer. F24–F31 identities, owner-equivalent/source-native/forbidden family dispositions and the existing local version-2 target remain controlling.

## 3. Producer, adapter and consumer ownership

RD-05 owns native accepted lifecycle and eligibility derivation. RD-06 owns promise construction and campaign publication. RD-09 owns selected LIVE acceptance/selection/absorption. RD-07 owns the mechanical routing representation and current-native recovery. No recovery module becomes a lifecycle or SAVE authority.

Future file actions:

| Owner | Action |
|---|---|
| RD-07 | NEW_CREATE GAME/TOOLS/recovery_roots.py; DEV/SCHEMAS/operational-root-routing.schema.json; GAME/SCHEMA/operational_root_routing.schema.yaml; GAME/CAMPAIGN/STATE/RUNTIME/RECOVERY_ROOTS/FORMAT.yaml. |
| RD-07 | Extend its planned GAME/TOOLS/recovery.py and DEV/TESTS/test_rd07_recovery.py. |
| RD-05 | Extend its planned GAME/TOOLS/runtime_execution.py and DEV/TESTS/test_rd05_runtime_execution.py. Native schema reconciliation remains the existing RD-05 lifecycle task; do not introduce a competing recovery lifecycle field. |
| RD-06 | Extend planned durability.py, publication.py and DEV/TESTS/test_rd06_durability_publication.py. |
| RD-09 | Extend planned GAME/TOOLS/live_state.py and DEV/TESTS/test_rd09_access_live.py; include the field in its one final live_scene.schema.yaml integration. Extend the existing final GAME/CORE/LIVE_SCENE.md and DEV/TESTS/LIVE_SCENE_CASES.md consumer cutover with operational-root handoff. |
| RD-14 | Extend planned DEV/TESTS/test_rd14_bootstrap.py generator/scaffold acceptance. |
| Shared projections | RD-07 supplies schema README, storage-template README and STORAGE CORE deltas; integrate through F41/F47/F46, as amended below. Required PROJECT_MAP and maintenance-audit discovery updates join their owning GREEN checkpoints. |

Canonical source paths: `../specs/2026-08-20-step-5-2-resumable-runtime-closure-canonical-spec-v2.md`, `../specs/2026-08-20-step-5-4-host-lifecycle-session-handoff-canonical-spec.md`, `../specs/2026-08-20-step-5-5-soft-hard-save-durability-canonical-spec.md`, `../specs/2026-09-02-r2-7-WP-13-durability-save-publication-canonical-spec.md`, and `../specs/2026-09-03-r2-7-WP-14-recovery-checkpoints-session-repair-canonical-spec.md` remain semantic authorities.

The schema pair defines the marker and entry document shapes plus the reusable logical owner_ref definition for LIVE. Marker validation does not certify complete membership.

Required mechanical interfaces, implemented with the named owner:

| Interface | Owner and role |
|---|---|
| operational_root_membership_path(owner_ref) | RD-07 pure deterministic derivative-path function, using RD-04/WP-11 routing and the current native identity contract. |
| derive_operational_root_delta(before_owner, after_owner, promised_native_closure, current_membership) | RD-05 derives required add/retain/remove refs from validated owner semantics and the effective owner-defined promise. Inputs are actual native closure evidence, not caller-supplied eligibility booleans. |
| validate_operational_root_delta(native_closure, root_delta, source_basis) | RD-07 mechanical identity/reference/coherence validation; consumes the native eligibility result, never invents it. |
| enumerate_operational_root_page(pinned_source, bounded_cursor, budget) | RD-07 read adapter returns typed refs, explicit continuation and complete/incomplete evidence for the selected active-only namespace or LIVE envelope. It grants no READY result. |
| hydrate_operational_roots(selected_sources, complete_root_routes) | RD-07 follows exact current native routes and required dependency edges, then performs native validation before final READY validation. |

Physical-routing helpers are pure or repository-adapter work outside the mechanic transaction. Derivation inside RD-05 performs no host/network IO. Local lifecycle establishment and any derived local membership bookkeeping use the existing RD-04/05 owner-transaction/dirty substrate; no durable second journal or generic transaction owner is added. RD-06 reconstructs/validates required deltas from the frozen native closure and current membership, so loss of a local derivative cannot suppress enrollment.

The RD-07 contract/path/schema checkpoint can be GREEN using native contract fixtures and RD-04 routing primitives before full RD-05 execution, RD-06 publication or RD-09 LIVE integration. Consumer closure later joins their actual producers. Do not turn this split into RD-07-full -> RD-05-full -> RD-07-full.

## 4. Campaign and LIVE publication closure

For every lifecycle/promise boundary changing required membership:

1. Freeze the affected accepted owner generations and native dependencies under the existing owner-defined scope.
2. Derive add/retain/remove memberships, including promised unresolved inputs and any active Procedure surviving its Command.
3. Validate native owner plus required routing in the same resulting campaign tree, or the same accepted exact-source LIVE packet.
4. Preserve the existing ACCEPTED/REJECTED/INDETERMINATE outcome rules. Uncertainty reconciles the frozen attempt/current source before another transition; accepted native work is never replayed to manufacture routing.
5. Claim durability/recovery-safe handoff only when the complete promised native composition and its required routing are actually durable/current.

Campaign publication cannot acknowledge durable active owner without enrollment, route without required native target, or removal stranding unfinished descendants. LIVE exact-source CAS establishes the owner and embedded route delta together; rejected CAS establishes neither. No-write success must prove the already-durable required native/root composition; it cannot skip a missing route. An independently failed domain does not undo real accepted work in another domain.

Campaign source and selected LIVE source use the same current-domain handoff discipline as F36:

| Transition | Required closure |
|---|---|
| Prepare candidate from exact H | Candidate native payload and operational routes are equivalent to the eligible claimed state at H; candidate remains non-authoritative. Do not move campaign membership at preparation. |
| Select prepared LIVE | One campaign closure selects the exact LIVE route and removes precisely the transferred campaign memberships. Unclaimed campaign roots remain. Prepared data must still meet exact opening/current-selection validation. |
| Ordinary selected LIVE transition | Native state plus matching operational_root_routes cross one CAS; no campaign-side mirror update. |
| Close LIVE | CLOSED_UNABSORBED remains the selected terminal truth, including its frozen routes; closing transport authority does not settle native unfinished owners or authorize fallback. |
| Absorb exact final Lf | One campaign closure materializes the F31 native successor and eligible campaign membership, then releases the selected LIVE route. Preserve accepted native IDs and dependency references. |
| Partial/unknown multi-LIVE transition | F7 forward-only exact-final-source rules apply. No old campaign root set, selected terminal source or accepted mutation is silently rolled back/reopened. |

Duplicate prepared references are harmless. Missing or duplicate **current-domain** enrollment during selection/absorption is an integrity conflict. No distributed transaction, all-LIVE scan, global lock, new recovery cut or additional normal campaign write inside selected LIVE is introduced.

## 5. Cold recovery and completeness

A recovery attempt selects current campaign/LIVE authority, pins exact native revisions and loads the campaign format marker plus the selected active-only namespaces/embedded LIVE routes. It completes required root enumeration, hydrates every root and bounded correctness-required native dependency, validates source/identity/lifecycle compatibility and only then performs final readiness validation.

The campaign adapter traverses only the four admitted active-membership prefixes at the exact campaign revision. It must bound each provider operation and expose finite progress/continuation. Partial/truncated listing never proves an empty or complete set. No ordinary family-history, campaign-wide tree, WORLD, all-ref or Git-history scan is allowed. Missing provider capability or exhausted operation budget yields the existing affected-scope RETRY/BLOCKED behavior with explicit bounded progress where valid; there is no hidden exhaustive fallback or indefinite in-call retry.

The current route is source-partitioned: campaign roots are separate from each selected LIVE source, entries are independent within the campaign source, and pinned traversal can be resumed without a mutable global routing generation. Where an operation is scoped, use accepted scope/claim/dependency evidence; a caller-supplied arbitrary subset cannot stand for the complete promised recovery scope.

Required outcomes:

| Case | Outcome |
|---|---|
| Valid blank marker plus fully read empty active namespaces and healthy producer/coherence evidence | Empty operational roots; ordinary bootstrap remains valid. |
| Missing/malformed marker, malformed membership, truncated enumeration or unproven completeness | No empty/READY inference; affected bounded retry, block or owner-authorized integrity repair. |
| Root points to absent/incompatible selected native owner | Integrity/prerequisite failure, no campaign/history/cache fallback. |
| Root points to terminal native owner | Native terminality wins; stale derivative is diagnosed/repaired, never reactivated or replayed. |
| Active required owner reached through another bounded path has no required entry | Completeness defect; reject affected READY/publication assertion. |
| Required root omitted so cold enumeration cannot see it | Producer and publication assertions must detect this omission at establishment; arbitrary syntactically valid edited routing is not certified complete by the reader. |
| Originating Command settled but Procedure active | Procedure remains independently discoverable and resumes from its same native identity/state. |
| Selected source moves or ownership changes | Invalidate affected selection, boundedly reselect; do not mix revisions. |
| Required accepted evidence/RNG/child/Continuation/catalog basis absent | Typed failure; no reroll, new offer/ID, ambient reinterpretation or recreation of lost HOT. |

Routing completeness does not grant authorization, disclosure eligibility, retention protection or permission to destroy history. Deleting a routing entry is not permission to delete its native owner/evidence or a transport ref. Existing cleanup/protection and absolute no-ref-deletion rules remain controlling.

## 6. Exact proof obligations and placement

These are future task-owned tests. Each class is created in its own RED-to-GREEN task, never pre-created as a failing later-task suite.

| Exact module and class | Primary channel | Required evidence |
|---|---|---|
| DEV/TESTS/test_rd07_recovery.py::OperationalRootRoutingContractTests | FOCUSED_BEHAVIOR | Closed family/identity/prefix contract; WP-11 suffix round-trip including chunked IDs; marker versus entry shape; no semantic payload; valid explicit blank format; malformed/foreign refs rejected. |
| DEV/TESTS/test_rd05_runtime_execution.py::OperationalRootEnrollmentTests | FOCUSED_BEHAVIOR | Every A/B/C eligibility edge; independent Procedure after Command settlement; class-C promise qualification and irreducible message evidence; retain during unrelated SAVE; terminal/sufficient-replacement removal; unfinished descendant protection; no IO or invented lifecycle authority. |
| DEV/TESTS/test_rd06_durability_publication.py::OperationalRootPublicationTests | INTEGRATION_SCENARIO | Actual RD-05 producer plus RD-07 routing contract; same resulting-tree owner/root closure; omitted owner/entry and premature removal injected; generation G/G+1; no-write, stale and unknown result cases; no broad derivation scan. |
| DEV/TESTS/test_rd09_access_live.py::LiveOperationalRootHandoffTests | INTEGRATION_SCENARIO | Actual seed/CAS/selection/close/absorption route deltas; preparation non-authority; transferred versus unclaimed campaign roots; duplicate/missing current domains; exact Lf and accepted-ID preservation; partial/unknown forward transition. |
| DEV/TESTS/test_rd07_recovery.py::OperationalRootRecoveryTests | INTEGRATION_SCENARIO | Real producer/publication output survives complete loss of HOT/checkpoint/chat; active Procedure counterexample; all promised root classes and required descendants; bounded active-only pagination, incomplete enumeration, missing/malformed/stale membership, selected-LIVE authority and final source movement. |
| DEV/TESTS/test_rd14_bootstrap.py::BlankScaffoldCompletenessTests | FOCUSED_BEHAVIOR | Actual generated FORMAT.yaml is valid with no gameplay root entries; missing input blocks generator validation; no post-generation repair or whole-RD09/RD16 prerequisite. |
| DEV/TESTS/test_implementation_proof_ledger.py::SharedSchemaStorageReadmeIntegrationProofTests | STATIC_AUDIT | Actual final integrated schema/storage README bytes include RD-07 operational routing and all other F41/F55 contributions. |
| DEV/TESTS/test_rd07_recovery.py::StorageProjectionTests | STATIC_AUDIT | Actual final F46 STORAGE bytes route cold recovery through current typed roots; no history/checkpoint/known-ID-only completeness fiction. |
| DEV/TESTS/test_rd09_access_live.py::ShippedLiveCoreCutoverTests | STATIC_AUDIT | Actual final LIVE_SCENE.md and LIVE_SCENE_CASES.md preserve current operational-root membership through selection/close/absorption and forbid campaign mirrors or close-as-native-settlement; preserve every earlier SIRR2/F24–F38 requirement. |

Commands, only during authorized implementation/proof execution:

~~~bash
python3 -m unittest DEV.TESTS.test_rd07_recovery.OperationalRootRoutingContractTests -v
python3 -m unittest DEV.TESTS.test_rd05_runtime_execution.OperationalRootEnrollmentTests -v
python3 -m unittest DEV.TESTS.test_rd06_durability_publication.OperationalRootPublicationTests -v
python3 -m unittest DEV.TESTS.test_rd09_access_live.LiveOperationalRootHandoffTests -v
python3 -m unittest DEV.TESTS.test_rd07_recovery.OperationalRootRecoveryTests -v
python3 -m unittest DEV.TESTS.test_rd14_bootstrap.BlankScaffoldCompletenessTests -v
python3 -m unittest DEV.TESTS.test_implementation_proof_ledger.SharedSchemaStorageReadmeIntegrationProofTests -v
python3 -m unittest DEV.TESTS.test_rd07_recovery.StorageProjectionTests -v
python3 -m unittest DEV.TESTS.test_rd09_access_live.ShippedLiveCoreCutoverTests -v
~~~

PG35 is the package integration row for this complete chain. It primarily uses INTEGRATION_SCENARIO, with the exact focused/static sub-obligations above. R072 owns current-route/root hydration; existing R038 accepted-execution recovery and R074 item-bound WP-14 obligations consume the applicable cases without being replaced by one aggregate PG pass. R011/R073 checkpoint shape is not misassigned as the root producer. No new readiness ID is created.

## 7. Checkpoint and shared-file joins

| Producer checkpoint | Target | Relation |
|---|---|---|
| RD04 routing primitives + current native identity contract | RD07_OPERATIONAL_ROOT_CONTRACT_READY | Local contract/path/schema/marker GREEN; no full recovery prerequisite. |
| RD07_OPERATIONAL_ROOT_CONTRACT_READY + RD05 native lifecycle contract | RD05_OPERATIONAL_ROOT_ENROLLMENT_READY | Producer derivation GREEN; no full RD07 prerequisite. |
| RD05_OPERATIONAL_ROOT_ENROLLMENT_READY + RD07_OPERATIONAL_ROOT_CONTRACT_READY + implicated RD06 publication substrate | RD06_OPERATIONAL_ROOT_PUBLICATION_READY | JOIN_BEFORE_INTEGRATION for the actual campaign acceptance edge. |
| RD05_OPERATIONAL_ROOT_ENROLLMENT_READY + RD07_OPERATIONAL_ROOT_CONTRACT_READY + RD06_OPERATIONAL_ROOT_PUBLICATION_READY + implicated RD09 identity/packing/CAS substrate | RD09_OPERATIONAL_ROOT_HANDOFF_READY | JOIN_BEFORE_INTEGRATION for actual LIVE/selection/absorption edges; RD06 campaign handoff acceptance participates. |
| Above actual producer/publication/handoff results + RD07 current-source selection | RD07_OPERATIONAL_ROOT_RECOVERY_READY | JOIN_BEFORE_INTEGRATION before claiming complete current-native READY. |
| RD07_OPERATIONAL_ROOT_CONTRACT_READY | RD14_BLANK_SCAFFOLD_INPUTS_READY | Fifth mandatory blank-product input under F40; precedes generator validation. |
| RD07 operational-root schema/projection delta + existing RD07 checkpoint schema delta | RD07_SCHEMA_DOC_DELTA_READY | Extend the existing F41 schema input; same identity. |
| RD07_OPERATIONAL_ROOT_CONTRACT_READY plus GREEN operational-route storage projection assertions | RD07_OPERATIONAL_ROOT_STORAGE_DOC_DELTA_READY | Bounded new F41 storage-template input, no full RD07 dependency. |
| RD07_OPERATIONAL_ROOT_STORAGE_DOC_DELTA_READY + existing RD02/RD03/RD04 storage inputs | GAME_STORAGE_README_FINAL_INTEGRATION_READY | Existing final shared writer now integrates four inputs. |
| RD07_OPERATIONAL_ROOT_RECOVERY_READY plus existing RD07 STORAGE recovery delta | RD07_STORAGE_RECOVERY_CORE_DELTA_READY | Extend F46's existing input; retain one final CORE integration. |
| All PG35 behavioral/integration targets plus actual generated and final projection proofs | OPERATIONAL_ROOT_ROUTING_PROOF_READY | PROOF_AFTER_TARGET; terminal proof sink, not a semantic prerequisite. |

Contract/scaffold readiness must not wait for full RD05 mechanics, RD06 SAVE, RD09 source-native identity, RD14 generator, RD16 shared machine integration or final RD07 recovery. Native identity **contract** validation can use fixtures; final generated/runtime instances still require the existing final shared identity integration. This preserves the early RD14 campaign-identity and late RD16 topology joins.

F41's schema README still has five owner inputs (RD02/03/04/07/08), with the complete RD07 delta extended. Its storage-template README now has four (RD02/03/04 plus the bounded RD07 operational-root storage delta). F47's unchanged exact final-byte witness must run after both final integrations. No owner-local snapshot may overwrite another admitted contribution.

This addendum also extends existing final LIVE_SCENE and STORAGE CORE consumer projections where they describe the changed route/handoff behavior. ShippedLiveCoreCutoverTests and StorageProjectionTests above inspect those actual final bytes after their existing F46/SIRR2 integration targets. Fold the delta into those final edits; do not publish an independently final earlier version.

## 8. Version, cost and completion limits

The new derivative contract/marker/entry local version is 1. Final live_scene remains local version 2 under F43, now including operational_root_routes before its one final unpublished cutover. Existing native owner schema changes remain under their RD05/current version owners. No extra native family, catalog generation, campaign contract generation, engine version, allocator namespace or MANIFEST selector is created by the derivative routing.

Final STORAGE framework_module_version remains 1.0.2; final LIVE_SCENE remains 1.0.4. Integrate the new required projection into the existing unpublished final edit. Schema/storage READMEs have no independent version bump. Clean-slate generation includes the format marker; no legacy migration, dual-read or compatibility shim is introduced.

Cost obligations: root enumeration is proportional to admitted active memberships and required dependencies, not retained terminal runtime history. Record N active roots, traversed active-only tree nodes/pages, payload bytes, source count, provider calls and serial dependency depth separately. Provider batching is not assumed. Membership create/remove has real publication cost; unchanged membership adds no mandatory rewrite. Selected LIVE keeps its existing packet CAS edge, with payload growth to measure. No new LLM pass or global campaign hot singleton is required. Exact latency, practical batch size and optimal future partitioning remain measurement obligations, not claimed results. Normal operation may not replace the bounded contract with an unmeasured whole-history scan.

Planning closure requires the concrete producer, physical contract, same-closure publication, current recovery, generated scaffold, final projections and item-bound proof chain above. Passing current hosted documentation/tooling tests does not execute these future runtime tests or independently approve the package. Production execution and zero-open author/Senior closure remain gated by current package authorities.
