# Spell inventory and implementation coverage assessment

Status: RESEARCH CANDIDATE — not an accepted architecture amendment, executable plan, consumer admission or production-readiness claim.

Baseline: `21d0b624a88a4519a226ebedb853c92c2ba5c4a3`, branch `v1/engine-rearchitecture`.

## Scope and result

The inventory enumerates all 339 individually headed spell descriptions in the SRD 5.2.1 spell section, printed pages 107–175. It covers every listed class and spell level, not only the current character seed. It is exhaustive for this edition and corpus, not for all commercial D&D supplements, older editions, house rules or future publications. Those require separate ruleset and content admission.

[`spell-inventory.json`](spell-inventory.json) is the structured assessment; [`spell-inventory.csv`](spell-inventory.csv) is its spreadsheet projection. Every entry preserves name, level, school, class membership, source page, dominant capability group, cross-cutting tags, Actor impact, shared dependencies, marginal complexity, confidence and qualifications. Grouping is many-to-many through dependencies; the dominant group is only an index, not exclusive ownership. Tags are descriptive research facets, not an exhaustive casting-input schema or machine admission. Conditional costs and exceptional rules remain in each row's qualifications.

The current six-spell seed intersects this corpus in five spell descriptions. Thunderclap is an additional seed entry, not an individually headed spell in this SRD spell section. Occurrences of that word in item/monster abilities do not establish a spell description. This is a content-provenance boundary to reconcile with the admitted package owner, not a finding of unlawful content and not authority to remove or replace the accepted seed.

## Task boundary and source manifest

Question: determine the complete bounded spell corpus, identify shared mechanical capabilities and estimate relative per-spell work so player choice is not advertised before its mechanical consequences are supported. No gameplay bootstrap, release-package inspection or production implementation was performed.

Dependency subgraph: ruleset edition/content membership -> class/level selection and readiness -> admitted Activity and Rule Element -> targeting/cost/roll evaluation -> Actor, Effect, location, Asset, knowledge or other existing semantic owner -> execution receipts and durable recovery -> player-safe presentation. LLM interpretation and narration cannot replace missing mechanical or canonical owner transitions.

| Source | Authority and bounded use |
|---|---|
| SRD 5.2.1 spell descriptions and relevant neighboring stat blocks | Licensed rules content; inventory membership and spell semantics, not HDM architecture authority |
| `AGENTS.md`; `DEV/DESIGN_PROCESS.md`; `DEV/ARCHITECTURE/DESIGN_PROCESS.md`; `DEV/PROJECT_MAP.md` | Role, research discipline, source discovery and publication boundaries |
| `DEV/PRODUCT_OWNER_INPUT.md`, PO-003/007; accepted public provenance owner decision | Interactivity requirement; required attribution versus public research narrative |
| `DEV/CURRENT_PROGRESS.md` and current T06 cursor/Senior Sorcerer override review | Current authorization/dependencies and unresolved product gate; not evidence of broad spell execution |
| `DEV/ARCHITECTURE/CHARACTER_PROGRESSION_READY_PC_SEED.md`; admitted character seed package and S6D-07 compiler | Exact seed selection/readiness and consumer closure |
| `DEV/ARCHITECTURE/ACTIVITY_MODEL.md`; `ACTIVITY_PRIMITIVE_CONTRACTS.md`; primitive manifest/shards | Registered transition semantics and exact admitted consumers |
| `DEV/ARCHITECTURE/ACTOR_MODEL.md`; `HEALTH_EFFECTS_RECOVERY.md` | Actor identity, health, Effects, duration/support and recovery ownership |
| `GAME/TOOLS/mechanics.py`; `runtime_execution.py`; `catalog_runtime.py`; `runtime_host.py` | Inspected production execution/binding/host surfaces; limits of execution proof |
| `DEV/TOOLS/validate_character_mvp_seed.py`; `validate_health_effects_recovery_seed.py` | Conformance/reference evidence; explicitly not full production spell execution |

These sources were inspected at the baseline; derivative maps were used for routing. No recursive repository preload or new architecture activation is claimed.

## Actor grouping and shared implementation work

An Actor-only grouping would miss significant cost. HP/LifeState belong to Actor; applied modifiers and conditions use authoritative Effects and derived projections. A summoned creature can become an Actor, while a zone remains a spatial/Effect concern, an object an Asset/entity concern, and revealed information a knowledge/disclosure concern. Transformation must preserve accepted identity and temporary replacement/reversion semantics. A schema permitting these concepts does not implement them.

| Shared capability | Current evidence boundary | Work shared across spells | Relative shared scope |
|---|---|---|---|
| Recipe execution and casting transaction | Catalog binding and segment/receipt machinery exist; seed compiler is a DEV conformance tool | Evaluate admitted recipes, validate costs/targets, bind fixed RNG, commit to exact owners, prove replay/recovery and player selection closure | L |
| Damage, healing, temporary/max HP | Damage has six exact spell consumers; healing admits Second Wind only; temporary/max HP are not general spell admission | Attack/save evaluation, mitigation, health transitions, scaling and exact consumer extensions | M–L |
| Effects and conditions | Create Effect admits Innate Sorcery only; generic update/removal dormant | Application/aggregation, immunity, repeated saves, ending/reapplication, durable reconstruction | L |
| Concentration and supported durations | Generic concentration is conformance-only; periodic content not activated | Support lifecycle, interruption, expiry, replacing concentration, cross-owner termination | L |
| Reactions and counter-magic | Reaction window and choice primitives dormant | Offer eligibility, suspension/resume, fixed outcome reuse, counters and effect suppression | L |
| Areas and repeated triggers | Finite bound target selection is not geometric discovery; zones/follow-ups dormant | Area membership, affected-target bounds, entry/start/end triggers, idempotent scheduling | L |
| Movement and relocation | Movement/teleport/time primitives dormant | Existing location ownership, path/destination legality, forced motion, planes and recovery | L |
| Summoning and Actor transformation | Unified Actor design exists; create/retire/transform primitives dormant | Lifecycle, control/agency, archetypes/stat blocks, action economy, equipment/form projection and reversion | XL |
| Objects, environment and material costs | General entity/assets/currency operations dormant | Exact object/world owners, creation/destruction, terrain, consumed components and cast prerequisites | L |
| Information, illusion and control | Generic information-spell consumer not proven; active emit_fact is only Action Surge entitlement | Truth versus perception/knowledge/disclosure, interactions, communication and agency constraints | L |
| Resurrection and exceptional magic | Healing/rest conformance does not establish resurrection or arbitrary state change | Existing-owner restoration policies, prerequisites, continuity, exceptional modes and bounded failure | L–XL |

Sizes above express comparative cross-system scope, not measured effort. Existing accepted designs should be reused; dormant realization does not justify reopening them without a demonstrated insufficiency. Shared work is counted once. It cannot be obtained by summing the 339 marginal spell sizes.

The primitive registry has 31 names: eleven currently admitted under exact consumers and twenty quarantined. Arbitrary compositions are not authorized by those eleven names. The active `op.apply_damage` consumers include the six seed spells; `op.apply_healing` is limited to Second Wind, and `op.create_effect` to Innate Sorcery. Additional spells require lawful consumer/dependency closure, including failures and recovery.

## What the implementation evidence proves

`validate_character_mvp_seed.py` labels itself a conformance compiler and requires actual primitive consumers to equal each contract's exact seed consumer set. `validate_health_effects_recovery_seed.py` labels itself a reference/conformance aid, not production runtime. Their tests establish valuable bounded contracts, not automatic end-to-end support for new spells.

In the inspected GAME path, `resolve_mechanic` delegates to segment execution with caller-supplied event kind/payload and fixed-RNG evidence. Catalog executable binding proves identity/admission, not spell consequence evaluation. RuntimeHost supplies substantial transport/domain composition; this assessment does not declare that work absent. These inspected surfaces do not establish a complete cast -> recipe evaluation -> owner mutation -> durable recovery path for every offered spell. A focused consumer/call-chain and end-to-end proof is required before a readiness claim. Absence in these bounded surfaces is not an exhaustive claim that no other relevant repository mechanism exists.

## Per-spell estimates and qualifications

Marginal sizes assume all listed shared capabilities and lawful admission already exist:

| Size | Meaning |
|---|---|
| S | Bounded definition, few branches and focused spell-specific verification |
| M | Multiple parameters, riders, scaling, saves or interacting branches |
| L | Substantial modes, stat blocks, lifecycle, propagation or interaction verification |
| XL | Exceptional/open-ended cross-owner semantics requiring explicit design and bounded acceptance |

Confidence concerns the analytical classification, not production compatibility. No hours, developer-days, measured runtime latency or complete implementation budget is claimed. Calendar estimates require a representative pilot from each shared capability family, actual integration/recovery proof and throughput calibration. A low-level utility or reaction spell can cost more than a high-level direct-damage spell.

Examples: Fire Bolt requires straightforward damage content after the shared path exists; Shield additionally needs a reaction and temporary modifier; Mage Hand needs object interaction and a controlled temporary entity; Polymorph needs form/lifecycle projection; Wish requires exceptional cross-system boundaries. Similar names must not import older-edition mechanics: several current Conjure spells are zones/effects rather than summoned Actor stat blocks.

## Candidate product and delivery approach

1. Keep this complete inventory as the target coverage matrix. Do not silently equate catalog presence, accepted design or compiler success with playable support.
2. For the current Sorcerer choice gate, assess the entire SRD level-0/1 Sorcerer list rather than two fixed bundles or six seed entries. This inventory identifies 16 cantrips and 21 level-1 spells; this is a candidate choice corpus, not current admission or a statement that all are available at once to a character. Prerequisites, preparation limits and spell slots remain governing rules.
3. Implement reusable capabilities by dependency families, then admit/test each covered spell. Preserve per-spell exceptions; a generic LLM improvisation path cannot stand in for missing mechanics.
4. Before READY_PC, verify closure for the character's selectable/known spells and relevant supported encounter content. Encounter generation, NPC spell choices, loot/scrolls and advancement must not introduce unimplemented mechanics behind that boundary. Catalog/selection restrictions are an interim product limitation and must be explicit; broader advertised SRD support requires broader verified closure.
5. For each admitted spell prove legal/illegal targets, casting costs, attack/save outcomes, scaling, immunity/resistance where relevant, concentration/expiry/counter interactions, save/load, duplicate delivery and failure containment. Use shared-family tests plus meaningful spell-specific exceptional cases, not 339 copies of a shallow test.
6. Only after representative pilots, publish calibrated shared and marginal effort estimates. Full SRD coverage is a substantial content-plus-engine program; completing P1A alone cannot certify it.

This is a recommendation for a future bounded decision/amendment, not a new executable plan. The current P1A product question is not resolved by this research; current P2/P3 authorization and dependency gates, accepted S1/S2/P0 and dormant Story/T07/T08/W06 remain under their existing owners. New mechanics are not activated.

## Coverage and verification

| Level | Spell count |
|---|---:|
| 0 | 27 |
| 1 | 57 |
| 2 | 57 |
| 3 | 42 |
| 4 | 34 |
| 5 | 38 |
| 6 | 31 |
| 7 | 20 |
| 8 | 17 |
| 9 | 16 |

| Primary group | Spells | S | M | L | XL |
|---|---:|---:|---:|---:|---:|
| DAMAGE | 52 | 6 | 43 | 3 | 0 |
| HEALTH | 27 | 9 | 12 | 6 | 0 |
| EFFECT | 45 | 13 | 23 | 9 | 0 |
| ZONE | 45 | 0 | 18 | 26 | 1 |
| MOVEMENT | 25 | 3 | 12 | 10 | 0 |
| TRANSFORM | 11 | 0 | 1 | 9 | 1 |
| SUMMON | 11 | 0 | 1 | 9 | 1 |
| WORLD | 33 | 3 | 16 | 14 | 0 |
| INFORMATION | 30 | 3 | 25 | 2 | 0 |
| ILLUSION | 15 | 0 | 7 | 7 | 1 |
| CONTROL | 28 | 0 | 14 | 13 | 1 |
| COUNTER | 9 | 0 | 6 | 2 | 1 |
| SPECIAL | 8 | 0 | 0 | 1 | 7 |

Totals: S=37, M=178, L=111, XL=13. These are conditional marginal categories; the shared engineering scope above is additional.


Verification is inventory/assessment verification only. It does not run a campaign or claim all spells execute. All 339 source headings are uniquely represented; level/school/class/page metadata joins exactly; three disjoint analysis slices are merged without missing/extra names; all required classification fields and shared dependencies are present. Two-column extraction artifacts were checked against official neighboring rules/stat blocks. Telekinesis's fine-manipulation continuation remains truncated in the available text and is explicitly qualified; no full semantic-resolution claim is made for that tail. Source text was read through the authorized web channel; no local PDF-byte digest is claimed.

VERSION_IMPACT: NONE. New DEV research artifacts only; no GAME code, schema/catalog admission, campaign/storage generation, migration or release change.

Independent bounded review: PASS after repair of Planar Ally's casting-component/service-payment distinction. The review independently checked all inventory joins/projections, counts and selected high-risk classifications. It is not an exhaustive adjudication of every mechanical exception or proof of playable spell support.

## Research continuation checkpoint

Role: Architect / bounded spell-coverage research. Inventory and conditional assessment complete; production compatibility unverified. Current scheduling still belongs to `DEV/CURRENT_PROGRESS.md`. This checkpoint does not authorize a worker to expand the spell corpus or activate dormant capabilities.

NEXT_RESEARCH_PROBE: trace one exact admitted cast from selected character content through production recipe evaluation, mechanical owner mutation, persistence and duplicate/recovery acceptance. Distinguish contract/reference proof from the GAME consumer before calibrating shared engineering estimates. Then use representative reaction, timed Effect, zone, utility and Actor-lifecycle spells to estimate shared versus marginal work. This is a research recommendation; any implementation follows the current role/gates and approved impact envelope.

OPEN_PRODUCT_JUDGMENT: breadth and delivery priority of playable spell support, including the existing P1A override requirement. Do not replace that judgment with an arbitrary six-spell or fixed-bundle limit. The complete inventory informs the decision without itself resolving it.

## Required attribution

This work includes material from the System Reference Document 5.2.1 ("SRD 5.2.1") by Wizards of the Coast LLC, available at https://www.dndbeyond.com/srd. The SRD 5.2.1 is licensed under the Creative Commons Attribution 4.0 International License, available at https://creativecommons.org/licenses/by/4.0/legalcode.

Spell names and source metadata identify the licensed corpus. HDM groupings, dependency assessment and effort commentary are independently formulated; full spell rule descriptions are not republished here.
