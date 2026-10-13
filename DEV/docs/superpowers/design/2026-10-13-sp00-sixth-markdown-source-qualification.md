# SP00 sixth bounded Markdown source qualification

Date: 2026-10-13. Role: bounded machine-evidence integration. This design-path record preserves source provenance and the accepted source-only dispositions; it is not a source-readiness or native-support decision.

## Pinned inputs and source basis

- Integration base: `afca759c38480f0e4a5629236b08c9d401ecd10d` (`v1/engine-rearchitecture` published target observed at this base after a successful fetch-and-prune refresh).
- Source extraction: `/tmp/hdm-dev/spell-recovery/SP00-sixth-source-extraction-20261013.md`, RAW_UTF8 SHA-256 `dc9600ae20c80c0f2a653dddb095246ea752b49c8a5493f3ad7411c6f44573a9`.
- Independent source review: `/tmp/hdm-dev/spell-recovery/SP00-sixth-source-review-20261013.md`, RAW_UTF8 SHA-256 `862aa04b0a27fa977b099bd0b4c19b1d9151a1313aaafcb8364c23b622f63ca1`.
- Both inputs name base `afca759c38480f0e4a5629236b08c9d401ecd10d`, fixture basis `c6d37201cab0a4dc2be1981762066f3d6d7b8be7`, unchanged reviewed keys 68–79 and no substitutions. The extraction selects 12 keys, 11 distinct spell bodies and 13 `SP00_SOURCE` subobligations.
- Primary Markdown: `DEV/docs/SRD_CC_v5.2.1.md`, RAW_UTF8 SHA-256 `c03c41b7c94d644646c8f979541b1664036a107e03823797ab1afac4b6e0b01e`. Exact current body spans and shared-rule spans are independently hash-checked by the validator. Historical source-pass and body-witness hashes remain distinct identity witnesses and are not normalized into current span hashes.
- The inherited asset identity is `srd52_en` / `SRD_5_2_1`, PDF URI `https://media.dndbeyond.com/compendium-images/srd/5.2/SRD_CC_v5.2.1.pdf`, hash `8974902d109d6e63672d7c490bde9ccf052410503d9cfa768237154fbc5e3d87`. No PDF is reopened or reverified here.

## Required source-review wording corrections

1. Suggestion's common Charmed wording is bounded to: **the Charmed creature cannot attack the charmer or target the charmer with damaging abilities or magical effects** (SRD Markdown lines 16272–16278, especially 16276). Charmed also grants the charmer Advantage on social-interaction ability checks. This does not create a general prohibition on every possible indirect or incidental harm. Suggestion's separate source requirement to pursue the suggestion remains distinct.
2. Concentration on an existing effect ends **the moment its creator starts casting another spell that requires Concentration**, or activates another effect requiring Concentration (lines 16296–16304, especially 16300). Completion of the new casting is not the trigger. The creator may end Concentration at any time without an action; damage uses DC max(10, half the damage rounded down), capped at 30; Incapacitated or dead ends it.

Casting components remain qualified by lines 9199–9201: the caster needs a free hand for Material components; a hand used for a Material component can also perform Somatic components; materials are not consumed unless stated; pouch/focus substitution applies only to nonconsumed, unpriced materials and where an applicable feature authorizes the focus. This compact integration does not replace the full pinned casting span.

## Item-level source evidence and dispositions

Every selected item retains its original unresolved-key classification, historical unresolved-record pointer, current mapping-entry pointer and historical source-pass/body-witness join. The exact source subobligation ID is the complete key plus `::` plus the category shown below. Current source span hashes are UTF-8 bytes of the inclusive 1-based Markdown lines, preserving line endings and the ending newline.

| ID | Original index / map entry / source-pass row / body-witness row | Exact key suffix | Source category | Disposition | Source span and SHA-256 |
|---|---|---|---|---|---|
| SIXTH-01 | 68 / 107 / 109 / 257 | `resistance.unresolved.damage_grouping_order` | `source_semantics` | HOLD | Resistance 14389–14401 `c8eb5178fade2834aa5ad5c504723c2499bcbfaeeb821d120b5dbc729ab3432c` |
| SIXTH-02 | 69 / 108 / 110 / 261 | `rope_trick.unresolved.boundary_location_profile` | `source_semantics` | CLOSE | Rope Trick 14457–14471 `0c387a71023cea2267db52607ba19c49db32d8ef43ff41ca02d2bb51ef958fa8` |
| SIXTH-03 | 70 / 110 / 112 / 263 | `sanctuary.unresolved.retarget_cost_chain` | `source_semantics` | CLOSE | Sanctuary 14493–14505 `c262ace6d5dc07b1dbf518b054b3c5ffb9450d41159b8409cc59affb91a41dda` |
| SIXTH-04 | 71 / 111 / 113 / 264 | `scorching_ray.unresolved.target_kind_policy` | `source_mapping_review` | CLOSE | Scorching Ray 14509–14523 `1a099cfc3c6ca8497b63350f4b7b3d0f1290533987e90a7748a242789d07356f` |
| SIXTH-05 | 72 / 123 / 125 / 285 | `sorcerous_burst.unresolved.permitted_type_members` | `source_mapping_review` | CLOSE | Sorcerous Burst 14897–14913 `6d590ba135423b140efa1ef1126985b28239d1d6ad2111e33c38dfe8d73e19fc` |
| SIXTH-06 | 73 / 124 / 126 / 286 | `spare_the_dying.unresolved.range_thresholds` | `source_parameter` | CLOSE | Spare the Dying 14917–14931 `d7166779d01e13af3f7f44a0f0bba46c3046c8f766fba5a9744dc718593d76ac` |
| SIXTH-07 | 74 / 125 / 127 / 287 | `speak_with_animals.unresolved.influence_option_census` | `source_mapping_review` | CLOSE | Speak with Animals 14935–14949 `06af8988a16d5c17090ee53692e53453a60171d9afb29c2495c482c29c1045a8` |
| SIXTH-08 | 75 / 127 / 129 / 291 | `spike_growth.unresolved.displacement_and_distance_policy` | `source_parameter` | HOLD | Spike Growth 15009–15023 `c5fb06ec056006712ee2c9a8a995391eb7e3e35134d4ad077339f447a6025dd1` |
| SIXTH-09A | 76 / 130 / 132 / 299 | `suggestion.unresolved.agency_and_word_limit` | `source_parameter` | CLOSE | Suggestion 15161–15175 `b379e6c0272739ada33bf0839c78f841942e0c1f5c3f73a509ab8038de698a15` |
| SIXTH-09B | 76 / 130 / 132 / 299 | `suggestion.unresolved.agency_and_word_limit` | `source_semantics` | CLOSE | Suggestion 15161–15175 `b379e6c0272739ada33bf0839c78f841942e0c1f5c3f73a509ab8038de698a15` |
| SIXTH-10 | 77 / 131 / 133 / 308 | `thaumaturgy.unresolved.exact_mode_bounds` | `source_mapping_review` | CLOSE | Thaumaturgy 15411–15435 `4bdca80fdecc504d47b7dfc9d447256d5d8477ea9da1503434043162ea8aff31` |
| SIXTH-11A | 78 / 134 / 136 / 320 | `unseen_servant.unresolved.subject_health_classification` | `source_semantics` | HOLD | Unseen Servant 15641–15655 `0f32649763cb95c6ce7d3fde0e844325df5af09d74932110ecec545a9a5265b6` |
| SIXTH-11B | 79 / 134 / 136 / 320 | `unseen_servant.unresolved.force_numeric_profile` | `source_parameter` | CLOSE | Unseen Servant 15641–15655 `0f32649763cb95c6ce7d3fde0e844325df5af09d74932110ecec545a9a5265b6` |

The nine closed keys represent ten closed source subobligations because Suggestion has two distinct source categories. The three held keys/subobligations are Resistance damage grouping/choice, Spike Growth qualifying displacement, and Unseen Servant subject classification. The three holds are retained despite extractable numeric or other source facts; no implied native-only classification replaces them.

### Bounded semantic record

- **Resistance:** the exact selected type is one of the source-ordered eleven; chosen-type damage reduces total damage taken by 1d4 once per turn. HOLD remains because occurrence grouping/choice and defense-consumer reconciliation are not supplied. No reaction, first-hit consumption, pooling, shared die or extra defense order is inferred.
- **Rope Trick:** preserve the 3-by-5-foot portal, climb/pull/drop entry, eight Medium-or-smaller occupancy, outward sight, effects barred both ways and anything inside dropping out at expiry. No 60-foot legacy limit, interior capacity, generic object-transfer permission, safe landing or portable-storage proof is added.
- **Sanctuary:** an attack roll or damaging spell targeting the warded creature invokes the Wisdom save; failure means retarget or lose that attack/spell, and areas bypass. The ward ends on the warded creature's attack roll, any spell cast or damage dealt. This does not create free attacks, a general slot-refund rule or a universal cost algorithm.
- **Scorching Ray:** three rays, separate ranged spell attack per ray, 2d6 Fire per hit, one additional ray per slot above 2. The body does not restrict target kinds; common attack text allows creature/object/location aims, but a location aim does not become a damage-bearing entity. Do not collapse rolls or infer automatic hits/object defenses.
- **Sorcerous Burst:** the source's exact types are Acid, Cold, Fire, Lightning, Poison, Psychic and Thunder. Base hit damage is 1d8; cantrip scaling is 2d8/3d8/4d8 at character levels 5/11/17. A rolled 8 permits an added d8, capped by spellcasting ability modifier per cast. No recursion, minimum-one rule or RNG/choice recovery is asserted.
- **Spare the Dying:** 15-foot range, doubled at levels 5/11/17 to 30/60/120 feet; target is a creature at 0 HP and not dead, which becomes Stable. Stabilization consequences are separately sourced; no immediate healing, temporary HP, resurrection or native LifeState proof follows.
- **Speak with Animals:** communication is with Beasts and any Influence skill option is available. Preserve the source's limited nearby/past-day perceptions and GM-owned willing/unwilling/hesitant handling, default DC and repeated-attempt wait. No automatic truth/cooperation, charm, free action or animal-handling-only restriction is added.
- **Spike Growth:** preserve 150-foot range, 20-foot-radius Sphere, Difficult Terrain, 2d4 Piercing per 5 feet actually traveled into/within the area, with no once-per-turn cap. Terrain movement cost does not turn 5 feet traveled into 10 feet traveled. HOLD remains for exact qualifying forced displacement; no voluntary-only, universal forced-motion, endpoint-only or fractional-distance rule is invented.
- **Suggestion parameter:** the full-body activity description is no more than 25 words; no tokenizer/punctuation semantics are added.
- **Suggestion semantics:** visible creature within 30 feet able to hear/understand; the activity must sound achievable and not obviously deal damage to target/allies. Wisdom failure produces Charmed plus the separately stated best-ability pursuit; duration, completion or caster/allies damaging target ends the spell. Damage to others is not automatically this spell's break trigger.
- **Thaumaturgy:** preserve all six named effects, their stated 30-foot range, V-only component, one selected effect per cast and up to three concurrent minute effects; completed instant effects do not consume that duration cap. Booming Voice's Charisma (Intimidation) Advantage is mechanical. No ignition, damage, lock bypass or numeric light/sound/tremor model is inferred.
- **Unseen Servant numbers:** AC 10, 1 HP, Strength 2, no attack and spell ends at 0 HP. Once on each caster turn, a Bonus Action command allows up to 15 feet movement and object interaction. A commanded task that would move it over 60 feet away ends the spell; this is not an ambient caster-motion leash.
- **Unseen Servant classification HOLD:** “Invisible, mindless, shapeless, Medium force” and its stats do not establish creature/object classification or target eligibility. Preserve the existing L02-C01 owner constraint; infer neither creature admission nor categorical noncreature legality. Native Actor/Asset/health admission remains future proof.

## Common source spans and preserved qualifiers

All 13 common-rule witnesses are bound in the machine contract and independently hash-checked from the full current Markdown bytes:

| Common span | Lines | SHA-256 |
|---|---:|---|
| Casting Spells | 9068–9257 | `48ccc959d306e2f349b56e2dea465f9b119c47d414105011fc44104384aa0702` |
| Making an Attack | 1248–1264 | `35bea2d0812d4a44be7fa07300bf0a7cf90dd6d8c0ad1dba7717889da7908b5e` |
| Ranged Attacks | 1286–1302 | `e32e0f321ea5b06703118555d745cd620d585d782b7bb925011670f948331e7c` |
| Damage Rolls | 1396–1400 | `3bab0640f9638faa8e732906e9ad79fb1941a7cbcfd1bba78b1e8bf69124ac15` |
| Resistance/Vulnerability order | 1434–1450 | `70acc27702623bfdce1f86419498e1b345cc5bc470cda3b6d183abdf1fc38378` |
| Stabilizing a Character | 1516–1520 | `e52fc17397fe17a22c9054a12d28e355584547809a85b42b7d82fb1aa55b9f5a` |
| Movement and Difficult Terrain | 1191–1203 | `1a15d99db21350e9d3cb9c53f846a225c3bf03fe6bc6f601bffdb735c3b8a127` |
| Charmed | 16272–16278 | `59b73e22432dc652c3dfda5cc7f578c8b1819da2054c8edc8246fbe9bfb064e3` |
| Concentration | 16296–16304 | `04c55227b54b4481f715a64b6a517f63f5733171d475640db0f6f43d355cc1be` |
| Difficult Terrain glossary | 16493–16509 | `e9e0afb99ffc82ef3458a05377b6d59b5d7fe85332f5afe676e2b57a52946dd1` |
| Influence / full options table | 16777–16797 | `eb96f2b41eb6a99c11ec3ac0301626e4a6a1366f8252a1c044b9380935071319` |
| Teleportation | 17321–17325 | `d5d19757d0bf00d0bc58f4ddc10e59a48067004bae7c67f6b4758d15b62dee1c` |
| Invisible | 16809–16817 | `cbf3644671e39a3df5e040933a31a70300194f8cfadffe6b1ff4e68d9e91b73c` |

## Preservation and computed accounting

- Original unresolved classification/history/current-map arrays, source-mapping definitions, all prior source-review records and cumulative totals are preserved. Existing 12 `SOURCE_HELD` keys are unchanged; this set adds exactly three further holds.
- All 33 original `FUTURE_PROOF` subobligations remain `NOT_ESTABLISHED`. The seven selected mixed-key future-proof records are indexes 68, 69, 70, 74, 75, 78 and 79, each retaining category/ID suffix `downstream_domain_consumer_admission_native_proof`; none is discharged.
- `/content_owner_default_repair` remains `REQUIRED_BEFORE_PACKAGE_PROMOTION` for the unqualified Thunderclap existing-extra lane. No replacement default or raw-unknown/default association is selected; no new PO gate is introduced.
- `/source_modeling_residuals/0` remains `NOT_ESTABLISHED` for Word of Recall sanctuary redesignation/replacement/survival. No latest-wins rule or automatic cap is inferred, and the residual is not conflated with the selected Sanctuary spell.
- Derived from the integrated registry and validated source subobligations: **71 reviewed unique keys / 74 source evidence records; 56 closed keys / 59 closed source subobligations; 15 held keys / 15 held source subobligations; 21 active source-blocking keys across 20 entries.** The selected delta is 12 keys / 13 source records, nine closed keys / ten closed source subobligations and three held keys / three held source subobligations. Counts are computed by the validator from exact key/category identities and dispositions; they are not a readiness claim.
- The roster remains the inherited **82 classifications / 77 originally source-blocking / 5 downstream-only**. The 33 future-proof count and the separate default/Word of Recall residual lanes are retained.

## Scope, verification limits and impact

This integration changes only the existing SP00 schema, source qualification fixture, rejected fixture, validator, focused test module, and this new design evidence record. It adds exact registry binding, original-pointer/provenance checks, full body/common-span hashes and count-derived sixth cumulative output. It does not change source recipes, GAME/runtime members, package identity, class entitlements, execution support or any native consumer.

Verification was local to a detached real Git clone at base `afca759c38480f0e4a5629236b08c9d401ecd10d`: focused source-qualification tests, cold evidence mutation regressions, Ruff checks, maintenance audit and package/runtime identity checks are recorded in the separate integration receipt. No commit, push, cursor update, main-checkout write or shared-index mutation is part of this worker task. No claim is made for source readiness, recipe readiness, native support, package promotion, the full 339 roster readiness gate, all 339 source bodies or remote publication.

**VERSION_IMPACT: NONE** — this is an additive pre-release DEV-only evidence extension to the existing draft `schema_version: 1` source-qualification contract and fixture. It neither changes a released/persistent/runtime protocol nor changes package members or compatibility meaning; `DEV/RELEASE/VERSIONING.md` §§4 and 7 and its canonical compatibility policy §§2 and 9 permit development-only draft-schema evolution without a release namespace bump, while required schema version remains 1 as specified by SP00. No GAME/DEV projection or package identity is altered.

**SYSTEM_IMPACT: NONE** — source disposition/evidence only; unresolved holds and downstream/native proof remain explicit.

This work includes material from the System Reference Document 5.2.1 ("SRD 5.2.1") by Wizards of the Coast LLC, available at <https://www.dndbeyond.com/srd>. The SRD 5.2.1 is licensed under the Creative Commons Attribution 4.0 International License, available at <https://creativecommons.org/licenses/by/4.0/legalcode>.
