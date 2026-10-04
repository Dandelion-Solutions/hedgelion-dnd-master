# Spell execution Step 2 — Local content, physical cost and recovery evidence

Status: **DESIGN WORKING EVIDENCE / CANDIDATE RECOMMENDATIONS**. No production implementation, capability admission, measured latency, canonical amendment or complete 339-spell semantic closure is claimed.

Source basis: fresh Connector read of `refs/heads/v1/engine-rearchitecture` returned `05576261665280c3f424d791c19d8c4080343c6a` on 2026-10-04. Repository file reads below use that exact commit. Delegated role: bounded read-only architecture investigation after Review Stop 1 GO. Local task brief/product input and spell research are requirements/routing aids, not replacements for current repository owners.

## 1. Bounded dependency subgraph and Source Manifest

Complete local spell content -> manifest/exact snapshot/resolved lock + engine capability inventory -> selected catalog context -> discovery cards and immutable compiled recipe -> interpreter/binder -> pinned actor/source/target/Effect/Resource/Procedure inputs -> existing ExecutionSegment/native semantic owners -> receipt/mandatory children/Continuation -> HOT or selected LIVE native establishment -> durability/publication/recovery -> eligible role packet -> Narrator emission.

Side dependencies: local supporting stat blocks/archetypes/assets/rules; exact policy basis; temporal provider/boundary/relation enrollment; actor control/agency; world truth versus knowledge versus player disclosure; instruction-cache restoration; currentness/adoption/retention. Each side route must be closed for the particular spell and mode rather than loaded universally.

| Source | Role and inspected claim scope |
|---|---|
| `AGENTS.md`, `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md`, `SKILL_SCOPE.md`, both design-process owners | Process/transport, inherited pinned delegation, design-only boundary, source completeness, no repeat gates; Superpowers brainstorming and project-local Clean Architecture read; Prompt Optimizer read for the context-boundary lens, no actual prompt rewrite or model optimization performed |
| `DEV/PROJECT_MAP.md`, `DEV/CURRENT_PROGRESS.md` | Derivative discovery and sole global authorization cursor respectively; preserve P0/S1/S2, P1A hold and separately eligible P2/P3; this slice grants no production authority |
| `DEV/PRODUCT_OWNER_INPUT.md` PO-003/007/008/010; delegated latest product input | Sparse decision basis/zero-extra-serial law; legal provenance boundary; proactive durability-risk intent; current mutable sizing bands; accurate local 339-spell direction |
| `DEV/ARCHITECTURE/ACTIVITY_MODEL.md` §§3–9 | Canonical finite composition, bounded binding/hydration, cached recipes, no deterministic-step LLM calls, continuation and one normal host operation |
| `CATALOG_RESOLUTION.md`, `CATALOG_ADMISSION.md`, `RULESET_PACKAGE_IDENTITY.md`, `RULESET_PACKAGE_MACHINE_CLOSURE.md` | Exact context/source identity, discovery versus execution, admission versus realization, manifest member closure, load/adoption/recovery and immutable accepted-work basis |
| `2026-08-19-step-3-execution-boundary-canonical-spec.md` §§5–6,12–22 | Idempotency first; fixed RNG/facts; safe recomputation; complete mandatory due closure; context barrier; native commits/receipts and partial/blocked outcomes |
| `2026-08-20-step-4-truth-knowledge-role-context-story-canonical-spec.md` §§5–6,9–10 | Subject knowledge, player disclosure, coherent phase context, restricted Interpreter/Actor/Narrator evidence |
| `2026-08-24-r2-3-context-runtime-canonical-spec.md`, `2026-08-24-r2-4-single-context-llm-execution-canonical-spec.md`; WP-08 and WP-09 realization specs | Bounded discovery/typed closure; required representation floors; central estimator; logical roles do not mean physical calls; rebind; terminal one-alternative fallback; no universal percentages |
| `2026-08-21-step-5-3-5-9-temporal-agenda-chronology-integration-canonical-amendment.md`; WP-15 canonical spec §§5–6,10–12 | Complete enrolled dependencies, local invalidation, due is not accepted firing, no wall-clock catch-up, current-native-root recovery; WP15-29 qualifies earlier generic future-RNG-frontier wording |
| WP-16 canonical spec §§4–5,7,10–14 | Separate campaign/LIVE/HOT currentness; bounded owner lookup; cross-source accepted edges; one action is not one LIVE write |
| WP-24 canonical spec, all law groups; `2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md` | Structural/Class A/Class B/Class C evidence separation; bounded operation and growth; no invented numeric SLA; full CORE special-path preload preserved; lossless owner-valid partition; read-only package material is outside mutable sizing bands |
| `GAME/CORE/AI_REASONING.md` §§13–14, `PLAY_POLICY.md` cache/lazy/research/intent/latency sections; `GAME/RULES/INDEX.md`, `README.md` | Actual instruction owners, natural player language, local current-decision path, external lookup explicit opt-in; existing general guidance is not precise complete local spell-content provisioning |
| `GAME/TOOLS/runtime_host.py`, `catalog_runtime.py`, `context_budget.py`, `context_runtime.py`, `hot_store.py`, `temporal.py`, `ruleset_package.py`, `runtime_execution.py`, `mechanics.py`, `turn_runtime.py` | Actual function/call-chain evidence discussed in §2; bounded infrastructure does not establish every cast consumer |
| Built-in package manifest and `character-mvp-seed.json`; remote package subtree metadata | Current explicit five semantic members and exact seed material; no release archive inspected |
| `test_rd15_catalog_runtime.py`, `test_rd11_context_runtime.py`, `test_rd08_temporal.py`, `test_runtime_host_composition.py`, `test_rd04_native_routing_index_hot.py` | Inspected pertinent positive/negative assertions, not executed test evidence; tests protect current identity/closure/currentness boundaries rather than measuring supported-host latency |
| Local 339-entry inventory/assessment | Research-only breadth, dependency and exceptional-mode nominations; source parsing qualifications retained; grouping is not an executable closure proof |

Owning specs are under `DEV/docs/superpowers/specs/`; architecture filenames in this table are under `DEV/ARCHITECTURE/`. Full source references and function identifiers make the bounded reads reproducible. No whole-repository contents preload was used.

## 2. Current-source evidence and qualified gaps

| Evidence | Established behavior and qualifier | Consequence for the candidate |
|---|---|---|
| Activity §8 | Compile when loaded; cache full compiled object; hydrate acting actor, explicit targets/source, relevant Effects/Resources/Procedure; one normal host call runs until closure/failure/genuine suspension | Reuse this accepted direction; no new spell service or per-spell LLM |
| `catalog_runtime.bind_catalog_context -> _normalize_dependencies -> _rebuild_definition_sources -> ruleset_package.build_resolved_lock -> build_snapshot` | Every fresh bind through this path rebuilds the explicit package lock from disk, hashes declared members and parses JSON; definitions are collected across rebuilt snapshots. `_find_dependency` is linear over the bound dependency tuple | Correctness protection exists. If called each cast, package-member work would repeat. This is a conditional cost risk, not measured latency or proof current orchestration does invoke it each cast |
| Catalog tests around `test_changed_package_bytes_cannot_reuse_a_snapshot_self_reported_digest` and forged semantic entry | A caller-mutated snapshot or self-reported digest cannot replace immutable source validation | Memoizing the existing mutable `PackageSnapshot` or trusting path/mtime is insufficient. Cache needs loader-issued admitted immutable inputs; exact current tests must remain valid |
| `runtime_execution.accept_command` / `validate_execution_proposal`; `mechanics.resolve_mechanic -> execute_segment` | Exact command/catalog/input identity and segment/RNG evidence are guarded. The segment function accepts event payload/roll request/Procedure/Continuation inputs; it is not itself a demonstrated full spell evaluator | Production binder/evaluator/native owner-write closure remains to prove through a real cast call-chain; no claim that all other repository functionality is absent |
| `RuntimeHost`, `ContextService.assemble`, `_begin_operation` | Host binds real sibling services. Each ContextService assembly explicitly begins an operation, pins campaign and reads selected LIVE; some other internal service routes accept only their own host-issued operation basis. Test `test_each_operation_repins_campaign_and_rereads_selected_live` asserts four independent operations mean four pins/LIVE reads | No source evidence of zero remote reads for each actual current host operation. “Already-local ordinary path” is accepted architecture/target, not a measured implementation result. Do not bypass currentness checks to meet a read budget |
| `turn_runtime.bind_phase_from_context` | Each material phase assembles through actual ContextService and seals scope/frontier/bundle identity before binding | Logical rebind is required; it does not imply a model call. Repeated host assemblies may amplify pins/owner reads; operation-scoped current observation reuse requires owning-safe lifetime/revalidation proof |
| `context_runtime.discover_candidates`, `_required_closure`, `_assemble_bound_context_unverified` | Candidate hints are channel-filtered, sorted and bounded. Required closure is cycle-safe and typed; missing dependency is terminal. After complete required closure, every remaining discovered optional candidate is resolved before byte allocation | Finite is useful; optional hydration can still dominate a narrow spell turn. A narrow discovery set and minimum eligibility/compact representation before full optional body load are the candidate optimization. Top-k hints cannot prove exhaustive target or choice scope |
| `context_budget.estimate_size / allocate` | Actual canonical JSON UTF-8 bytes, not caller-supplied size; required-first allocation; terminal `UNSATISFIABLE` | This proves byte accounting only. It is not measured model tokens, remaining host capacity, total prompt size or protected Narrator/output calibration |
| `NativeHotStore.read_admitted_snapshot` | Exact native owner keys in a closed SQLite snapshot; raw persisted dirty rows are not current merely after restart; instance-local admission markers must match | Reuse key-based HOT reads. Recovery must re-establish current source/admission, not trust a surviving SQLite row |
| `temporal.resolve_temporal_dependency_dependents` | Selects matching dependency key by filtering all entries in the supplied exact route. Rebuild walks explicit roots; completeness validates producer-issued native enumeration | Correctness/route completeness exists. Dependency-local physical complexity is not demonstrated by the filter alone. Reverse index or an explicitly bounded partition is needed when measured route fanout triggers it; do not infer a campaign-wide scan |
| Manifest `hdm.rules.dnd2024-srd52-core` | Declares five semantic members: manifest, character capabilities, character seed, health/Effects recovery seed and gameplay spine seed; package revision1/catalog generation2 | Manifest breadth does not establish 339 recipes/supporting blocks. Extend explicit semantic member/admission closure; do not use a wildcard, online registry or runtime DEV validator |
| WP-16 laws42–48 | No distributed multi-LIVE transaction; native durability edge defines atomic establishment; accepted edges survive later failures | Normal one local orchestration target is compatible with multiple necessary owner/LIVE/publication edges. Never promise one cast = one physical write |

These are source-supported behavior/proof limits at this pin. No timing benchmark was run, no GAME startup performed and no production tests/builds executed in this design slice.

## 3. Minimal local content design

**Recommendation: extend the existing package, catalog, Activity and native-owner path with immutable loader-bound indexes and recipes.** Three alternatives are materially different:

| Alternative | Assessment |
|---|---|
| Runtime raw-rule interpretation, full-catalog prompt or per-cast external lookup | Fails offline/correctness/performance direction; no recommendation |
| Existing finite Activity composition, admitted exact shared capabilities, local source-derived cards and cached compiled recipes | Recommended; preserves owners and makes ordinary cost proportional to the bound cast/current decision |
| New general spell DSL/service/interpreter and state/commit plane | Unjustified before concrete accepted capability insufficiency; creates avoidable ownership and recovery risk |

### 3.1 Package and compile boundary

1. Author independently formulated semantic spell/mode definitions and supporting local content under existing package owners. The exact manifest names every semantic member. Required legal attribution remains; public source-specific development narrative does not become architecture.
2. At authorized build/load/adoption/recovery boundaries, validate the explicit dependency-closed package set, namespace uniqueness, schema/exact consumer admission, engine contract inventory and all spell/support dependencies. Produce an internal immutable admitted-source handle from validated exact bytes and typed identity, not an externally asserted hash.
3. Compile every admitted recipe once per applicable content/engine-contract identity, either at this boundary or once on first local demand after those same admission prerequisites. Compilation resolves legal operations, argument/result validators, selectors/accessors, costs, dependent definitions, typed fact permissions, continuations and owner write surfaces. A missing capability is a typed admission/compile failure.
4. Derive a local ID -> complete compiled recipe table and compact search/card indexes. Choose simple in-process maps/inverted sets first; no vector database, new network registry or persistence authority. A serialized cache, if later worthwhile, is optional derivative support and must be reconstructible from the exact pinned content.
5. Ordinary invocation dereferences the selected validated recipe and only its bound live inputs. It neither hashes/parses the full package nor recompiles all recipes each turn.

**Cache validity:** compile cache key covers typed ruleset-set identity, exact engine capability/contract identity, catalog generation and relevant compile-contract generation. Owner-local campaign/session definition inputs retain their exact frontiers/evidence. Card localization and recipe semantics have explicit dependencies; a localized alias change cannot silently change executable meaning.

Do not invent a digest that replaces the existing snapshot/lock/catalog fingerprint chain. A changed compile implementation invalidates its derivative product even when semantic source is unchanged. A package or engine switch invalidates future selections; accepted in-flight work continues on its retained exact compatible basis or reaches the existing explicit migration/adoption block.

The current binder's mutable filesystem-source protection cannot be weakened. A future optimization must either consume a sealed immutable loader-owned source or revalidate the affected source at the appropriate load/adoption boundary. Until that issuer/consumer contract is proved, retain current rebuild behavior rather than claim cache closure.

### 3.2 Discovery and player-facing cards

Cards contain only compact relevant names/aliases, intent/effect facets, source/mode reference, coarse targeting/cost choices and a local exact recipe ref. They nominate; they do not confer ownership, preparation, spell slots, targeting legality or control.

Search scope begins with the acting character's actually available casting sources/capabilities, current pending continuation and declared intent. Direct exact-ID or alias lookup precedes broader bounded facet lookup. Natural or translated wording maps to an existing capability only after deterministic availability and equivalent consequence/cost checks. Material alternatives prompt one genuine choice; ambiguous wording never silently grants/casts a guessed unavailable spell.

A player who may select from a large legal list gets local filtered/paged choices with explicit completeness/continuation semantics; search top-k is not proof no other legal choice exists. The normal prompt contains a small candidate set or the selected card, never 339 complete descriptions. Package-wide indexing may inspect all finite339 at load; ordinary retrieval does not.

Character acquisition/progression, NPC casting, scroll/item use and encounter generation remain distinct lawful consumers. Complete packaged spell support cannot prove every class progression/loadout or authorize an unimplemented scroll/NPC/source route.

### 3.3 Engine packet versus role packet

The engine needs complete exact mechanics for the invoked mode plus all transitive required stat/rule/owner inputs. It consumes compiled typed content locally. The LLM normally needs selected semantics, registered genuine adjudication inputs/choices and the recipient-safe resulting receipt; full raw mechanics and per-target arithmetic are not transported by default.

RoleContextBundle remains ephemeral and profile-owned. Extend existing registered profiles/typed relations only for proved spell consumers and legal representation floors. Required meaning must fit before optional lore/texture. Narrow descriptor/eligibility reads first; hydrate full optional content only when its selected legal representation actually needs it. No third allocator or spell-private universal context graph.

Fresh Interpreter/Actor/Narrator binding remains mandatory. Hidden monster statistics, illusions, private source facts and another Actor's knowledge do not become Narrator/player information from cache presence. Information spells establish only the owner-approved knowledge/disclosure changes; emitting a result follows the actual Narrator/EMISSION_COMMIT boundary. No erase of human disclosure to simulate memory loss.

Keep complete exact deterministic evidence in its native execution/retention route; a compact narrative receipt may aggregate only where the typed consumer permits it. Receipt compression never deletes affected targets, required causal evidence, pending work or mechanical outcome distinctions.

### 3.4 Complete offline supporting content

A 339-name inventory is insufficient. For every spell and mode, a machine-checkable closure row must identify:

- exact authored rule semantics and casting-source/prerequisite/slot/component/consumption routes;
- every required Activity/Rule Element/primitive/selector/accessor/value/policy;
- supporting stat blocks/archetypes, form eligibility/retained fields, innate or referenced actions/spells, senses/movement/resistance/immunity/condition rules, assets/equipment and transformation teardown;
- spatial/environment/location/plane and temporal dependencies;
- facts requiring genuine subjective adjudication, with allowed provenance and failure/continuation route;
- persistence/currentness/recovery and recipient-safe presentation requirements.

Classify a dependency as local admitted content, current bound campaign owner, newly authored bounded supporting content, genuine invocation adjudication, or unresolved source/admission blocker. Follow transitive references only through explicit content/consumer relations. Detect missing/circular executable support before availability is advertised.

Examples nominated by research: Skeleton/Zombie for Animate Dead; Animated Object body for Animate Objects; legal Beast/form content for Polymorph/Animal Shapes; copied-stat/resource divergence for Simulacrum; spell duplication for Wish; plane/portal/destination capability for Gate. These examples do not assert a complete support census. Several current Conjure spells require zones/Effects rather than old-edition creature-summon blocks.

A required local block missing at invocation returns the typed unavailable prerequisite; no browsing, model-memory stat block or invented arithmetic repairs it. The final full-corpus promise may be accepted only after all such blockers close. Local rules availability is compatible with GitHub writes required for campaign persistence: offline rules does not promise disconnected LIVE authority.

Primary-source extraction uncertainty is a separate blocker. Telekinesis's fine-control tail in the research is explicitly unresolved; nearby two-column contamination and recovered embedded blocks require primary visual/text comparison. Resolve licensed source versions and all exceptional clauses, then independently author the semantic contract and golden cases. Research tags such as “scheduler” or “rollback” do not activate a scheduler or rewrite accepted-history law.

## 4. Large sets, temporal duration and lossless resumption

### 4.1 Complete set before consequential execution

Where spell semantics require all creatures/objects in a scope, the relevant owner must establish complete current scope membership and required spatial predicates. Scene hints/index omission or bounded candidate search cannot prove all targets were found. If completeness is not establishable, suspend for the exact missing scope evidence/adjudication; do not cast against only loaded actors.

Pin/freeze the lawful target/effect dependency footprint at the native contract boundary. Distinguish a finite complete semantic set from working-batch width. Never replace “all eligible targets” with a host chunk limit.

- If native semantics permit order-independent distinct owner segments, process lossless bounded chunks with stable target/step identity, completed receipt refs and explicit remaining work under the existing root/Continuation law.
- If rules define coupled simultaneous or atomic consequences, bounded chunks may stage/read/compute, but the complete native atomic closure must be established together. Do not commit the first chunk and pretend that is the same cast.
- If order matters, use the registered timing/controller choice/order-adjudication route. ID order, SQLite order and chunk boundary cannot choose mechanical precedence.
- If the supported host cannot safely hold/establish an indivisible native edge, return a typed capacity/prerequisite hold before that edge and preserve any lawfully accepted ancestors. Do not split canon for speed or report final success.

Atomicity may be owner-local or cross-source edge-relative; WP-16 forbids fabricating an all-LIVE atomic transaction. Recovery reconstructs each accepted edge and unresolved dependency exactly. Full legal cardinality cannot be promised constant latency.

### 4.2 Summons and transformations

Resolve local admitted stat content without an LLM pass per entity. Create/retire/control/project form through actual Actor/Asset/Effect owners, preserving identity/reversion and any source-native LIVE identity. Commands, agency, initiative, duration, concentration/support and follow-up actions remain exact per spell.

Material Actor decisions are separately rebound logical phases; deterministic creation/stat derivation is not an Actor model call. Compact identical-stat derivation may share read-only recipe/block data, while actor identity, HP/resources, control and history remain independent.

### 4.3 Long duration, off-scene and recovery

Enroll only the actual dependency keys of armed owner occurrences: applicable Procedure boundary, metric provider, source/target life/support/concentration, area membership, relation evidence and declared local temporal state. Use derived key -> affected owner/occurrence support, or an explicitly bounded owner partition where that is cheaper. Changes reach every declared affected consumer; narrative relevance does not suppress correctness.

Long duration causes no per-turn catalog/world/Effect scan and no per-wall-clock polling. Offline/host absence, SAVE, load, LIVE close/absorption and Git commit do not advance fiction. Accepted fictional advancement stops at due coordinates, closes or durably suspends the complete immediately-due set, and retains exact unconsumed advancement.

Repeated numbered spell phases retain their own semantic stages; do not reduce Storm of Vengeance to one generic tick. Periodic catch-up may be reduced algebraically only when exact outcome equivalence, ordering, triggers, costs, choices and RNG semantics are proved; otherwise process every mandatory occurrence through bounded continuation work. No missed-tick truncation.

Cold recovery follows current routed native operational roots and exact accepted rules/inputs, resumes accepted execution first, then rebuilds derived temporal/index/cache support. `DUE` hydration alone is not a new firing. INDETERMINATE remains enrolled. Old ambient MechanicalContext never resumes as trusted state; re-pin/rebuild only from the declared safe phase while retaining fixed RNG, facts, choices and accepted receipts.

Earlier Step-3 future-RNG wording is qualified by WP15-29: do not add a generic persisted future RNG schedule. Preserve actual accepted fixed values/provider state required by the admitted mechanic; reserve-before-generation semantics need their own proved consumer.

## 5. Physical budgets and minimum acceptance plan

### 5.1 Separate counters

Measure per path: physical LLM invocations; sequential model depth; assistant/model continuations after tools; total local tool operations and deterministic compute; remote reads/writes/objects/bytes; selected LIVE CAS/refresh/retry; prompt and output bytes and actual tokens where host exposes them; cold compile/parse/hydration; cache hit/invalidation; owner/target/due cardinality; recovery reads; end-to-end and component wall time.

One GAME assistant turn / one chat / several logical roles is not evidence of one physical model inference. Adopt **zero additional dedicated spell, arithmetic, per-target or per-summon LLM invocations and zero added serial model depth solely for deterministic spell work** relative to the already sufficient ordinary host path. Measure the actual baseline and any tool-response continuation. Genuine human choice/adjudication/reaction/currentness suspension is classified separately; optional Story/Commentator does not acquire critical-path capacity.

Normal sufficient-local cast target: one local IntentPlan orchestration invocation runs deterministic work to closure or genuine typed stop. This does not impose one native commit, one remote API request or one LIVE write. Required owner publication/CAS/currentness reads remain visible counters. If they add serial cost, optimize only within their proven boundaries.

### 5.2 Fixture matrix

| Fixture/path | Required observation and acceptance |
|---|---|
| Cold load/admission, full339 + required support closure | Exact finite manifest/set validation and bounded dependency closure; all required content resolves locally; one compile per admitted content/engine identity; missing/malformed/source-contaminated member rejects availability; record bytes/parse/compile/memory/time separately |
| Warm ordinary direct cast and multi-clause message | No rule network lookup, catalog-wide hash/parse/compile or per-step model call; only bound actor/source/targets/relevant dependencies; each clause settled/skipped/failed/suspended accurately; count actual host pins/read amplification |
| Small versus enlarged unused catalog/world/history | Same selected recipe/targets/current dependencies produce the same semantics; warm prompt/runtime reads/deterministic work do not grow with unused corpus/history merely because it exists |
| Freeform and localized intent; many legal choices | Exact candidate/current capability validation; no guessed new spell; material alternatives preserved; paging complete; no full-catalog prompt or top-k-as-absence claim |
| Reaction/choice/concentration interaction | Freeze accepted historical inputs; expected child changes lead to lawful safe recomputation; no reroll/reapply; changed relevant external dependency conflicts; bounded closure remains non-settled when blocked |
| Large target set around chunk boundary | All legal targets processed exactly once; result invariant across working batch widths where lawful; order-sensitive case rejects arbitrary sorting; atomic case never partially establishes due solely to chunking |
| Summon/form/duplicate body | Required local exact stat/action/equipment closure; distinct identity/resource histories; no per-entity deterministic model call; proper teardown/reversion/control; omission/missing block fails before false completion |
| Long duration, many unrelated off-scene owners | Changing K keys selects exactly all affected consumers and no unrelated partition scan; INDETERMINATE stays reachable; due stage/repeat/save/concentration/expiry rules and same-coordinate closure preserved |
| SAVE/LOAD, cold recovery and lost cache | Resume accepted receipts/RNG/choices exactly; no fiction advanced from host elapsed time; declared current-root reads only; restart rejects unadmitted dirty HOT rows; exact old rules recover or finite compatibility failure |
| Selected LIVE, cross-LIVE and stale/indeterminate CAS | Required exact authority fences preserved; multiple native edges counted; accepted first edge survives later rejection; no blind duplicate write/mechanics retry; unchanged technical transfer does not advance duration |
| Cache/adoption attack cases | Mutated source bytes/self-reported digest, wrong engine contract, localization mismatch, owner frontier change and incompatible ambient rules reject stale selection; compatible refresh retains accepted prior basis and safe barriers |
| Required context overflow/secret and optional bloat | Required floors retained or terminal UNSATISFIABLE with exactly one registered alternative; no silent required removal; eligible later use works; Narrator gets recipient-safe receipt; optional hydration/read growth documented |
| Real supported-target ordinary/cold/load/save/LIVE/recovery turn | Production host instrumentation, model/version/context state, runtime/set identities and workload recorded; time-to-response and total latency distributions plus component counters; protected output and natural player UX evaluated |

Use meaningful shared capability fixtures plus each spell's exceptional golden cases and a machine equality check that every339 row/mode/support obligation is closed. Do not create339 tests that only validate a label or mock an evaluator. Dedicated currentness/cache tests must preserve the existing forged/mutated-source negatives. Growth fixtures include adversarial irrelevant candidates, optional large payloads and unrelated due owners.

Class A: current exact content counts/bytes/topology only. Class B: benchmarks the implemented local/storage/transport path. Class C: real production-like supported host, including physical model calls/context behavior/Connector latency. These cannot be substituted for one another; no preimplementation parallel MVP or reported millisecond SLA.

Before performance acceptance, record repeated trials for cold and warm paths, distribution/spread/failures, exact environment and cache state, raw counters and identical semantic outputs. Only after those measurements may owner-approved workload-specific ceilings or regression tolerances be calibrated. Structurally reject prohibited work even if a small fixture happens to run quickly. Any real new serial correctness work is exposed as a material escalation rather than hidden behind “one tool call.”

## 6. Coverage and next integration obligations

The current accepted laws are sufficient as a base for this local/performance direction. Proved extensions are **new consumers/content and production realization**, rather than grounds for replacing semantic/context/durability owners. Exact new operation/value/profile contracts remain to derive from the per-spell evidence; no generic new state family is selected here.

Outstanding integration requirements:

1. Complete every339 spell/mode/source/support row and resolve primary extraction uncertainty before exact-content closure; cross-check discovery/acquisition/item/NPC consumers separately.
2. Trace actual production cast bind -> compiled evaluation -> native owner mutation -> mandatory child closure -> durable recovery and Narrator emission. Current inspected infrastructure is valuable but does not prove that full chain.
3. Make the immutable admitted-source/cache issuer contract concrete enough to preserve mutated-source rejection; remove repeated package rebuilding only after that proof.
4. Compare actual repeated phase currentness/read cost with operation-scoped owner observation lifetime; optimization must preserve revalidation. Existing host tests intentionally repin independent operations.
5. Realize/admit dependency-local temporal reverse support or contract-bounded partitions only on justified consumer/scale evidence, preserving complete future invalidatability.
6. Run the structural/Class-B/Class-C fixture plan on the separately authorized implementation and supported target. No numerical claim exists until then.
7. Preserve Story/T07/T08/W06 dormancy/current production cursor; update owning laws/status/traceability only through the coordinator's later design/gate/publication route.

Completeness gate for this slice: owning law and inspected function evidence reconciled; material qualifiers and superseding sizing/WP15-29 rules retained; negative cache/currentness/closure tests checked; read-only versus mutable content distinguished; no full339 semantic, all-class progression, benchmark, production-ready or canonical completion claim made.

VERSION_IMPACT: NONE for this design working artifact. A future semantic member, runtime cache contract, persistent continuation representation or compatibility-bearing schema change requires its own normal Version Impact/admission/migration gate.
