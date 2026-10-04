# Local spell content and acquisition contracts

Status: CANONICAL ANNEX — PO-013 ACCEPTED; independent Senior Stop2 and stable worker-plan approval remain required before production.
Canonical destination: `DEV/docs/superpowers/specs/2026-10-04-local-spell-content-acquisition-contracts.md`.
Evidence pin: `Dandelion-Solutions/hedgelion-dnd-master@fbaef81af38a64f3defd0ee928c9313a0c488fd2`, branch `v1/engine-rearchitecture`. No implementation, catalog activation, content import, tests or release validation was performed in preparing this annex.

## 1. Bounded source and dependency manifest

The bounded graph is: qualified primary spell/class/common-rule sources -> exact spell/mode records -> supporting definition/action/prerequisite domains -> registered contracts and native consumers -> package compilation/admission -> source-specific acquisition -> Actor/READY_PC -> real execution/recovery -> packaged offline/performance proof. Definition and state owners remain distinct.

| Source, read at the evidence pin unless marked external | Owning use and qualification |
|---|---|
| `DEV/ARCHITECTURE/CHARACTER_PROGRESSION_READY_PC_SEED.md`; accepted S6D-07 candidate; `DEV/ARCHITECTURE/ACTOR_MODEL.md` | Definition-owned choices/grants, Actor-owned bindings, fixed initial commitments, exact readiness and narrow supported classes |
| `DEV/SCHEMAS/build-choice-slot.schema.json`; `advancement-definition-data.schema.json`; `world-actor-state.schema.json`; current character seed, fixtures, validator and S6D-07 tests | Actual finite option/cardinality shape; existing known-all-six binding; actual hardcoded first-option mismatch check, not permission to weaken it |
| `DEV/ARCHITECTURE/PORTABLE_ACTIVITY_VALUES.md` | Definitions constrain bindings; source/cardinality cannot widen; generation-bound offers are embedded nonowners |
| `DEV/ARCHITECTURE/RULESET_PACKAGE_IDENTITY.md`; `RULESET_PACKAGE_MACHINE_CLOSURE.md`; current package manifest/capability declaration | Explicit semantic members, exact immutable identity, registered validators, comparator/adoption/retention; no shadowing or second digest authority |
| `DEV/ARCHITECTURE/DOMAIN_RULES_COVERAGE.md` | Exact promise/package/active-consumer equality; subsequent machine-closure owner establishes that its older migration blocker is historical |
| `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/candidate-spec.md`, SP-01/02/03/04/05/18/19/20; `source-obligation-resolution.md`; `performance-offline.md` | Current design proposal and resolved source obligations; not production admission |
| Three `source-pass-0-2.json`, `source-pass-3-5.json`, `source-pass-6-9.json` files in that design directory | All 141 + 114 + 84 available raw bodies, modes, exceptions, qualifications, negative evidence and confidence; historical source baseline and raw hashes are retained |
| `DEV/docs/superpowers/research/2026-10-04-spell-coverage/spell-inventory.json` | 339 exact headed entries; research group labels and class-header candidate tags are discovery evidence, not executable eligibility |
| Official [SRD 5.2.1 PDF](https://media.dndbeyond.com/compendium-images/srd/5.2/SRD_CC_v5.2.1.pdf), printed pages 64–65 and 67–68, freshly inspected 2026-10-04 | Independently confirms initial Sorcerer selection semantics and the 16-cantrip/21-level-1 SRD lists; not an online runtime dependency |
| `GAME/CORE/CHARACTER_READINESS.md`; `GAME/RULES/OFFICIAL_SOURCES.md` | Progressive local sufficiency and preparation lookup policy; qualify these for the promised installed spell surface |

The primary source says Sorcerer 1 chooses four known cantrips and two prepared level-1 spells. Spellcasting uses Charisma and may use an Arcane Focus. Replacement is a Sorcerer-level acquisition boundary, not a freely reopened Long Rest choice. This annex implements only the initial boundary; future class progression stays separately gated.

Attribution retained from the pinned research notice: This work includes material from the System Reference Document 5.2.1 ("SRD 5.2.1") by Wizards of the Coast LLC, available at https://www.dndbeyond.com/srd. The SRD 5.2.1 is licensed under the Creative Commons Attribution 4.0 International License, available at https://creativecommons.org/licenses/by/4.0/legalcode.

Raw body hashes identify the supplied extraction, including page furniture, displaced blocks or foreign headings. They are never canonical rule-content hashes. The published source-pass qualifications remain item-level import obligations, not silently corrected history.

## 2. Chosen initial acquisition contract

Preserve Human + Criminal + Fighter 1–2 + Sorcerer 1. Broaden the Sorcerer 1 spell option surface, not its initial cardinality or class progression. The full installed spell corpus does not grant every spell to that character.

Use the existing definition-owned finite `build-choice-slot` shape. At Sorcerer level 1, two opened slots under `advancement.sorcerer.mvp_1` replace the single selectable six-spell bundle in the new definition revision:

| choice_id | minimum = maximum | Each option's exact payload |
|---|---:|---|
| `advancement.sorcerer.level_1.cantrips` | 4 | One level-0 Sorcerer spell ID in `grant_definition_ids`; the same singleton in `spell_bindings.known_spell_ids` |
| `advancement.sorcerer.level_1.prepared_spells` | 2 | One level-1 Sorcerer spell ID in `grant_definition_ids`; the same singleton in both `spell_bindings.known_spell_ids` and `spell_bindings.prepared_spell_ids` |

Each option has one stable owner-relative `option.spell.<existing_spell_id_suffix>` ID. No arbitrary ID list, predicate query, model-produced option, bundle Cartesian product or new choice service is introduced. The current option schema already supports these payloads; compiler/readiness consumers need the coherent selected-option union change.

For this narrow HDM profile, preserve the accepted `known_spell_ids` bookkeeping meaning: the union of all six acquired spell grants. It is not a claim that the source labels its level-1 spells “known” under an older edition. Require `prepared_spell_ids` to equal exactly the selected two level-1 grants. `spellbook_spell_ids` is absent. Casting availability is source-specific: a selected known cantrip, or a selected prepared level-1 spell with its actual casting/resource profile. A generic “any known ID is castable” shortcut fails. No generic cross-class law `prepared subset known` is invented by this profile.

The exact reconstructive equations are:

```text
C = spell grants from the accepted four cantrip option bindings
P = spell grants from the accepted two level-1 option bindings
C intersect P = empty; size(C) = 4; size(P) = 2
Actor.build.spellcasting.known_spell_ids = C union P
Actor.build.spellcasting.prepared_spell_ids = P
required selected Activities/support = full admitted dependency closure(C union P)
```

Validate option identity in the owning slot and exact adopted catalog context; duplicate bindings/options/grants, cross-slot IDs, invalid class/level, bad defaults, missing support, stale context and extra/omitted membership fail closed. Compare required Activities to the whole selected dependency closure, including every required mode; do not use `activity_ids[0]` as completeness proof. Missing extra spell Activities is not excused because the original six Activities are present.

The current validator's `options[0]` comparison is superseded by validated selected-option derivation. The rejection `spell_selection_binding_mismatch` remains required for all mismatching states, including too few/many spells, omitted prepared membership, extra legal-but-unselected spells and unsupported IDs. This is a consumer correction, not removal of the negative case.

Starting equipment remains independent of spell identity. The existing one Arcane Focus must be granted once; do not attach one copy to each of four selected cantrip options. Where the existing definition envelope requires an option carrier, a singleton `choice.deterministic_default` starting-focus slot using the already accepted `starting_assets` shape preserves that one grant without adding a player question or opening equipment breadth.

### Complete SRD option pool

For the promised fully realized SRD package, the initial option lists must equal the independently reconciled source-eligible sets below. During authorized development, unsupported members remain absent/nonselectable and a partial profile must say so. Full-corpus release cannot hide a missing member by shrinking this list.

| Pool | Exact source names |
|---|---|
| Level 0, 16 | Acid Splash; Chill Touch; Dancing Lights; Elementalism; Fire Bolt; Light; Mage Hand; Mending; Message; Minor Illusion; Poison Spray; Prestidigitation; Ray of Frost; Shocking Grasp; Sorcerous Burst; True Strike |
| Level 1, 21 | Burning Hands; Charm Person; Chromatic Orb; Color Spray; Comprehend Languages; Detect Magic; Disguise Self; Expeditious Retreat; False Life; Feather Fall; Fog Cloud; Grease; Ice Knife; Jump; Mage Armor; Magic Missile; Ray of Sickness; Shield; Silent Image; Sleep; Thunderwave |

Exact class-list membership is proved against the lawful adopted source, then embodied in explicit definition options. Header candidate booleans alone do not author eligibility. Options offer full support units, not only convenient modes.

Acquisition legality is distinct from whether a spell can be cast in the current scene. Required component/Asset profiles must be installed and mechanically admitted, but selecting a spell does not grant or consume its priced material. READY_PC does not require every prepared spell to have an eligible target or every consumable currently in hand; actual cast preflight owns current components, resources and target applicability. Initial known/prepared equations apply to this acquisition source, not to a universal six-spell ceiling on later separately admitted grants.

### Defaults, commitments and migration

Both slots retain `choice.player_or_delegated`; their reviewed defaults constitute one explicit legal supported 4+2 recommendation. Preserve the existing recommended IDs—Fire Bolt, Poison Spray, Thunderclap, Acid Splash, Magic Missile, Burning Hands—when exact provenance, Sorcerer eligibility and complete support prove them lawful. They are recommendations, not the only legal choices. Explicit or delegated alternatives commit before relevant situational exposure.

Thunderclap is an existing admitted seed extra outside the 339-entry SRD inventory. Keep its definition and legacy commitments in a separate provenance/support lane; never count it as one of 339, infer SRD licensing from package ancestry, or silently delete/replace it. If that lane cannot lawfully close, the content owner must repair the new installed default atomically from the legal supported pool, preserving legacy snapshots/accepted work and recording source and compatibility/migration evidence before release. This is an exact materialization obligation, not another product-scope decision or runtime fallback.

The old `advancement.sorcerer.level_1.spells -> option.spells.mvp_default` meaning remains interpretable in its original exact snapshot. A new-context adoption maps the old accepted six values to the two new bindings and exact prepared subset without retuning the player's choices; any lawful content repair is explicitly reconciled. Changed advancement/options/membership may change canonical semantic hashes and block additive comparison. Do not assert silent compatibility from additive spell count. Use the existing comparator and adoption/migration owner, retain accepted contexts and fail when exact old dependencies are unavailable.

READY_PC continues to require one legal initial build, closed material initial choices and exact admitted selected dependencies, bound to Actor revision and generation-qualified ruleset/catalog identity. Defaults, source metadata, unbound proof lists and catalog presence do not establish readiness. Provisional play still uses local committed sufficiency; fixed initial choices do not await a favorable encounter.

## 3. Source, mode and dependency equality

A support unit is an entry plus its complete modes/branches and transitive content/mechanical requirements. Seal the entry/mode roster before claiming support. Finite parameter constraints describe legal values; a working chunk limit is not a smaller semantic domain.

For every claimed entry, the producer must independently derive and reconcile:

1. Promised exact entry names/IDs == reconstructed lawful source entry names/IDs == package spell definition IDs. Existing extras are a separately named set.
2. Required source requirement keys == keys with exact definition/mode/consumer/proof mappings. Every requirement keeps its exception, qualification, non-goal and confidence; no orphan or fabricated requirement.
3. Source-required mode/branch keys == declared mode/branch keys == verified production mode/branch keys for a released support claim.
4. Computed transitive dependency edges == declared/admitted dependency edges, with exact eligible-set census for domain-valued choices and exact active primitive-to-consumer equality.
5. Required registered schema/value/selector/accessor/fact/primitive/policy contracts == available compatible contracts for those consumers; structural validation cannot stand in for consumer admission.
6. Required conformance/native execution/retry/recovery/disclosure proof keys == actual fresh proof keys on the packaged path.

These are typed set/equality checks and explicit mapping relations, not literal equality between differently typed source IDs and Activity IDs. Unknowns, unresolved tails, duplicate ownership, omitted branches, unsupported advertised modes and `SUPPORTED_GAP` fail the corresponding admission/release boundary.

Report stages separately: architecture-routed; definition-complete; machine-admitted; production-realized; scenario-verified; target-performance-observed. A 339-row design matrix establishes the first stage only. READY_PC offers require actual current realization, not just a design row. Performance observation additionally requires real target instrumentation.

Supporting content is substantive mechanics. Find Familiar needs all eligible SRD CR-0 Beast forms and their permitted senses/actions, not only examples. Polymorph/Animal Shapes need complete eligible Beast/action domains. Shapechange/True Polymorph need their full source-specific lawful creature/action census and retained/granted fields. Animate Dead/Create Undead require complete Skeleton/Zombie/Ghoul/Ghast/Wight/Mummy mechanics; spell-created Animated Object, Otherworldly Steed and Draconic Spirit blocks travel with their owning spell support. Reincarnate needs eligible species traits/choices. Wish feat replacement needs the complete eligible SRD feat/prerequisite/benefit graph, not arbitrary feat names or universal class progression.

Monster Spellcasting and other actions retain actual acquisition, action/reaction, recharge/resource and nested spell dependencies. A decorative stat block is insufficient. Conversely current Conjure Animals/Elemental/Minor Elementals/Woodland Beings are not licensed to import older creature rosters when the current source defines zones/effects.

The source reconstruction lane must close displaced Animated Object/Otherworldly Steed blocks; Antipathy/Sympathy and Find the Path tails; Telekinesis's qualified licensed continuation; every foreign heading/footer/control character; and source-specific edition conflicts in existing seed consumers. Preserve valid U+2212 and U+00D7; withdrawn false corruption findings are not repair instructions. Exact numeric/branch recipes are independently formulated in HDM terms with attribution, not copied private/proprietary structures.

## 4. Package layout and adoption

Extend the existing `hdm.rules.dnd2024-srd52-core` package and its explicit manifest. No overlapping spell namespace package, last-wins overlay, online registry or new runtime state owner is needed.

Chosen content partition: ten explicitly named level shards `spell-content/level-0.json` through `spell-content/level-9.json`. Every entry/mode has one authoritative source record in its level shard; referenced supporting records live once in their natural content-owner shard. The six existing spell/Activity records move or are coherently refactored into that ownership at authorized materialization; the character seed keeps its grants/options/references and cannot retain duplicate competing spell bodies. The six-only compiler-source promise is superseded exactly at that transition.

An explicit semantic capability member names the promised spell profile and exact membership independently of the still-bounded character capability declaration. `full_srd_character_corpus=false` remains true and `ABSENT_NONSELECTABLE` remains required. A derived support inventory/compiled table is verification/retrieval evidence; it cannot choose mechanics, widen a promise or become a digest owner. The exact file names/schema and supporting shards must be reconciled into the stable worker plan before execution; this physical partition does not activate content.

The identity chain remains manifest -> exact semantic bytes -> builder-derived snapshot -> exact dependency-closed resolved lock -> generation-qualified ruleset-set identity. Include all runtime-required semantics and attribution, plus compiled runtime-owned conformance evidence. Runtime reads no DEV paths. Preserve exact Actor/Resolution/Continuation contexts, owner-local frontiers, retained snapshots and source qualification. No package revision/catalog/compatibility/engine generation is guessed here.

At build/load/adoption/recovery, validate the declared closure and issue immutable admitted inputs. Cache only against their exact content/engine/compiler/context dependencies. Ordinary warm casting dereferences the selected local compiled recipe; it does not rehash every member, recompile the corpus or traverse all source dependencies. Current mutable-source/tamper negatives remain intact; path/mtime or caller-reported digest is insufficient cache admission. Missing local authoritative support blocks before an offered unsupported cast spends resources.

## 5. Proof and performance release gates

Required proof is real command -> native owner admission -> composed host/execution/durability/publication -> receipt/state -> exact replay/cold recovery. Per-entry golden arithmetic, all modes, interruption/decline/counter cost, invalid-target paid no-effect/disclosure, stale offers, schema substitution and branch tests accompany each content shard. All legal supporting actions/feats/forms must execute through their actual owners.

Full release includes blocked rules-network execution, absent/corrupt local dependencies, cache invalidation, exact source/mode/support/proof equality and real packaged-path witnesses. It must not postpone discovering a missing implementation until after a claimed supported cast pays costs. Missing campaign facts, genuine adjudication, capacity suspension and missing installed rules are distinct routes.

Route measurements to WP-24: physical LLM count/serial depth; selected candidate/card/receipt prompt bytes and tokens; compile/lock validation/read cache behavior; local primitive/CPU/native owner work; dependency-local temporal work; remote currentness/publication/retry costs; and cold/warm/load/save/LIVE/recovery user-to-base-response distributions. No additional dedicated spell model, deterministic-step model or per-entity model fan-out; optional Story/Commentator work does not block the base answer. Hold relevant work fixed while growing unrelated corpus/campaign history; separately measure legitimate large affected sets without capping their semantics. Offline rules do not waive actual persistence/LIVE network barriers. No measured latency or invented SLA is asserted.

## 6. Bounded worker partition suggestions

These are decomposition inputs, not a final approved executable plan or task activation. Senior Stop 2 must reconcile the current stable plan/cursor, owner amendments and dependency gates first.

| Content unit | Entries | Owned finite shard |
|---|---:|---|
| C00 | 27 | level-0 |
| C01 | 57 | level-1 |
| C02 | 57 | level-2 |
| C03 | 42 | level-3 |
| C04 | 34 | level-4 |
| C05 | 38 | level-5 |
| C06 | 31 | level-6 |
| C07 | 20 | level-7 |
| C08 | 17 | level-8 |
| C09 | 16 | level-9 |

Each unit materializes every source-pass row requirement and proof key for its entries after shared native contracts exist; the 13 research groups are cross-family review facets, not services or mechanically separate executors. Data edits have disjoint shard ownership; shared schema/registry/package changes have one designated integrator.

Separate prerequisite/integration units should own: (A) primary reconstruction, attribution and the Thunderclap extra; (B) complete eligible statblock/action/species/feat supporting domains and their transitive closure; (C) the two-slot selected-union acquisition/readiness/default/focus/adoption contract; (D) manifest/compiler/support-equality/domain-coverage and runtime-owned attestation integration; (E) packaged offline/native recovery and WP-24 performance acceptance. Do not mark A/B/D complete by content counts or activate C on definition-only status. Production tasks use TDD under the approved stable plan; none is executed by this annex.
