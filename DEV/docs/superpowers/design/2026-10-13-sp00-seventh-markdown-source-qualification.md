# SP00 seventh bounded Markdown source qualification

Date: 2026-10-13. Role: bounded machine-evidence integration. This design-path record preserves the independently reviewed source-only dispositions; it does not establish source readiness, recipe readiness, native support, or package promotion.

## Pinned inputs and source basis

| Input | Exact identity |
|---|---|
| Integration base | `39ab1b4a1c7a844f4df2e7886c4b2ac17e401243` |
| Original-source inventory | `/tmp/hdm-dev/spell-recovery/SP00-final-unreviewed-source-inventory-20261013.md`, SHA-256 `57ce2b2bf272e0afeb0274ddafec6b34412bc21d52931396ca4370757fdcfcc0` |
| Independent source review | `/tmp/hdm-dev/spell-recovery/SP00-final-unreviewed-source-review-20261013.md`, SHA-256 `8b0b85cf1d2d9b4741e0d5699182cc188e4d95c3398194870a528847e9f00b71` |
| Source-qualification fixture basis | `DEV/TESTS/fixtures/spell-source-qualification.json`, SHA-256 `87ff9f41a73b346cad7038b5f126aec44c05a5f340fd310cf2fb67853fa9846b` |
| Primary Markdown | `DEV/docs/SRD_CC_v5.2.1.md`, SHA-256 `c03c41b7c94d644646c8f979541b1664036a107e03823797ab1afac4b6e0b01e` |

The independent review accepts five `CLOSE` source subobligations across four keys and two `HOLD` subobligations across two keys. It found no disposition reversal. This integration does not redo the bounded SRD review, reconstruct the historical PDF, or claim a new visual witness. Current Markdown body spans are hashed as exact UTF-8 bytes, preserving line endings and the ending newline.

The exact subtraction remains identity-based: the 77 original source-blocking classification keys minus the 71 keys reviewed by batches one through six leaves exactly indexes `6, 30, 31, 32, 80, 81`. The five downstream-only classification indexes remain `8, 9, 10, 23, 45`; no index interval or terminal sampling was used. The six selected keys assign seven `SP00_SOURCE` subobligations. Original classifications, historical reasons, pointers, `NOT_ESTABLISHED` statuses and `RECONCILE_EXACT_QUALIFIED_SOURCE_OR_OWNER; DO_NOT_GUESS` dispositions remain historical and unchanged.

## Seven exact source subobligations

Each subobligation ID is the complete original key followed by `::` and the assigned source category. Source-pass and body-witness identities below are retained witnesses, not newly reconstructed canonical spell digests.

| ID | Original index / map entry / source-pass row / body-witness row | Disposition | Current Markdown span and SHA-256 |
|---|---|---|---|
| `source.spell.augury.unresolved.four_omen_members::source_mapping_review` | 6 / 8 / 9 / 19 | CLOSE | Augury 9666–9693 `4d975b5dc7df9709bb366aa7e6d792ee6a5fcc0d169ad8e3c74ae4eb842c7891` |
| `source.spell.find_familiar.unresolved.eligible_form_census::source_mapping_review` | 30 / 48 / 50 / 117 | HOLD | Find Familiar 11609–11629 `ab7a578e4bd70abb8a5c3d57a0733b0a5dfd33f2b444ae17b488f68437bd3b98` |
| `source.spell.find_steed.unresolved.type_to_action_mapping::source_mapping_review` | 31 / 49 / 51 / 118 | CLOSE | Find Steed 11633–11653 `7a87d4710316fd37b8ba003941f1fa41d145538844af03bd21e676c4743f3ad0`; Otherworldly Steed 11657–11696 `e301a673cec765c35720f5ebb42da309303dbd30bd98b97f44a30c6e1afe2ca2` |
| `source.spell.find_steed.unresolved.steed_numeric_cells::source_parameter` | 32 / 49 / 51 / 118 | CLOSE | Otherworldly Steed 11657–11696 `e301a673cec765c35720f5ebb42da309303dbd30bd98b97f44a30c6e1afe2ca2` |
| `source.spell.find_steed.unresolved.steed_numeric_cells::source_mapping_review` | 32 / 49 / 51 / 118 | CLOSE | Find Steed 11633–11653 `7a87d4710316fd37b8ba003941f1fa41d145538844af03bd21e676c4743f3ad0`; Otherworldly Steed 11657–11696 `e301a673cec765c35720f5ebb42da309303dbd30bd98b97f44a30c6e1afe2ca2` |
| `source.spell.warding_bond.unresolved.copied_damage_policy::source_semantics` | 80 / 136 / 138 / 329 | HOLD | Warding Bond 15811–15825 `cc1be68ce4911478cbf85ba39ea14612445549e3126ce317f8583707ce51a244` |
| `source.spell.web.unresolved.web_numeric_geometry::source_parameter` | 81 / 137 / 139 / 332 | CLOSE | Web 15863–15877 `8de7309b0b27014012feaced44d167152956b95682a7e1c3b49465af12056cc6` |

### Bounded source findings and retained qualifications

- **Augury — CLOSE source mapping only.** The table has exactly Weal → Good, Woe → Bad, Weal and woe → Good and bad, and Indifference → Neither good nor bad. The GM chooses the omen for a planned course of action within 30 minutes. The source does not account for changed circumstances. The cumulative no-answer chance on later castings before a Long Rest is a separate already-reviewed key, not a fifth omen or a machine-predicted result.
- **Find Familiar — HOLD source mapping.** The body names Bat, Cat, Frog, Hawk, Lizard, Octopus, Owl, Rat, Raven, Spider and Weasel, plus another Beast with CR 0. Those named examples are not a complete lawful form census; the underlying form must remain a CR 0 Beast, and changing its resulting type to Celestial, Fey or Fiend does not waive that predicate. Statistics and special senses follow the chosen form. The eligible SRD CR 0 Beast census is still not established, and the lawful census must not be guessed from examples.
- **Familiar qualifiers.** The familiar rolls its own Initiative, acts on its own turn, cannot attack, and may take other actions normally. The two 100-foot tests apply to telepathy and touch delivery, not a general command leash. The touch-delivery spell requires the familiar’s Reaction; sensory relay uses the caster’s Bonus Action through the start of the caster’s next turn. Gear is left behind when the familiar reaches 0 HP or enters the pocket dimension, not on every dismissal/termination. Longer-casting and Ritual qualifications remain as stated below. Native action/sense and complete eligible-form proof remain unestablished.
- **Find Steed type/action mapping — CLOSE source mapping only.** Fiend maps to Fell Glare; Fey to Fey Step; Celestial to Healing Touch. Each is a Bonus Action that recharges after a Long Rest. Fell Glare is a Wisdom saving throw against the caster’s spell save DC, targeting one creature within 60 feet of the steed that the steed can see; on failure, the target has the Frightened condition until the end of the caster’s next turn. Fey Step takes the steed and rider to an unoccupied chosen space up to 60 feet from the steed. Healing Touch restores `2d8 + spell level` to one creature within 5 feet of the steed. Slam damage types remain Celestial → Radiant, Fey → Psychic and Fiend → Necrotic. No cross-type action, recharge, or attack substitution is inferred.
- **Steed action-availability boundary.** Mapping does not establish that an action or Bonus Action is available in every mount/control state. When ridden as a controlled mount, the source’s general rule restricts its action options to Dash, Disengage and Dodge and has it move on the rider’s turn. The special Incapacitated-caster protective turn is distinct. Do not grant an ordinary independent turn or unrestricted Slam from the stat block. The absence of a rider is not source proof that Fey Step is categorically forbidden.
- **Find Steed numeric cells — CLOSE source parameter only.** The owning stat block supplies Large; choice of Celestial/Fey/Fiend; Neutral; AC `10 + 1 per spell level`; HP `5 + 10 per spell level`; one d10 Hit Die per spell level; Speed 60 feet and Fly 60 feet only with a level 4+ spell; scores/modifiers/saves Str 18/+4/+4, Dex 12/+1/+1, Con 14/+2/+2, Int 6/−2/−2, Wis 12/+1/+1 and Cha 8/−1/−1; Passive Perception 11; caster-only 1-mile telepathy; no CR and 0 XP; and Proficiency Bonus equal to the caster’s. Life Bond triggers when the caster actually regains Hit Points from a level 1+ spell; if within 5 feet, the steed regains the same number of Hit Points the caster actually regained—not rolled/nominal healing or overheal. The block also supplies Slam modifier/reach/die/type and the exact three type-limited Bonus Actions above. Upcasting uses the slot level. Preserve U+2212 in the negative Int (`−2/−2`) and Cha (`−1/−1`) modifier/save cells; Wisdom is positive (`+1/+1`). Unlisted values are not zero and rideable appearance does not import an ordinary horse/animal block.
- **Find Steed displaced-block mapping — CLOSE source mapping only.** The spell body names Otherworldly Steed; the accepted owning block is lines 11657–11696 and ends before the Find the Path heading. The existing reconstruction witness accepts the Find Steed body and stat block and excludes the foreign Find the Path continuation and furniture; machine support remains `NOT_ESTABLISHED`. Historical page/header and body hash witnesses are distinct from the current block span. No fresh PDF visual check is claimed.
- **Warding Bond — HOLD source semantics.** The source states a willing touched target, two worn platinum rings worth 50+ GP each, one hour without Concentration, +1 AC/saves and Resistance to all damage while within 60 feet, and same-amount damage to the caster each time the target takes damage. It ends at the caster’s 0 HP, separation beyond 60 feet, or recast on either connected creature. General Resistance order does not establish copied-event type/defense/recursion, and the caster’s separate Concentration effects still follow their own damage rule. Warding Bond itself is not a second Concentration spell. Preserve the explicit recast ending; choose no recursive-bond default, copied damage type, blanket unreducibility, or coupled health/Concentration ordering. Later native damage/health/Concentration proof remains a separate future obligation.
- **Web — CLOSE source parameter only.** The spell states 60-foot range, a 20-foot Cube, Difficult Terrain and Lightly Obscured area; support between two solid masses or layering across floor/wall/ceiling; otherwise collapse and ending at the start of the caster’s next turn; 5-foot depth on a flat surface; the first-entry-on-a-turn/start-own-turn Dexterity save; Restrained while in the webs or until escape; an action for Strength (Athletics) against the caster’s spell save DC; each local 5-foot Cube exposed to fire burns away in one round; and 2d4 Fire to creatures starting their turn in that fire. Duration is Concentration up to one hour. Do not replace Cube with radius, erase the entire area for one burned section, allow repeated entry without the source’s turn predicate, or make fire damage immediate on contact.

## Common-rule qualifications carried with the batch

| Common source span | Lines | SHA-256 | Qualification preserved |
|---|---:|---|---|
| Longer Casting Times | 9159–9161 | `cf31fedb40e11967b8806caa5c42a5613692ef85112fdd6ad27e1309187a88f1` | Spells taking at least one minute require the Magic action each turn and Concentration even when their own duration is Instantaneous; interruption fails without spending the slot and requires restart. |
| Range | 9165–9175 | `179d9da6357281de3a4e376fa4c89f5debd85dfd8751b0f095bc5843dcb38003` | Range governs where an effect originates; it is not a generic post-creation leash. Familiar’s explicit 100-foot predicates stay distinct. |
| Mounted Combat | 1328–1344 | `236ea4cd79407b1b1fdc5cffe5f1a655dfe567653144f13b376f294faceb0b6c` | A controlled mount moves on its rider’s turn and has only Dash, Disengage and Dodge action options; an independent mount retains its own Initiative and acts as it likes. This does not resolve every steed Bonus Action state. |
| Combining Spell Effects | 9255–9257 | `459f8f4b95b21ee5993d23fc47d7fb0e5de64dc118051efce761634bb655b952` | Same-spell overlap rules do not replace Warding Bond’s explicit end-on-recast clause. |
| Resistance and Vulnerability | 1434–1450 | `70acc27702623bfdce1f86419498e1b345cc5bc470cda3b6d183abdf1fc38378` | Adjustment → Resistance → Vulnerability remains the common damage order; it does not establish Warding Bond’s copied-occurrence identity, recursion or lifecycle ordering. |
| Cube [Area of Effect] | 16360–16364 | `46c701d69e86c32fec52eee71f624b7c2919619e719ca21b9a3b2c8c84cf53da` | Cube origin may be anywhere on a face; side length defines size; origin is excluded unless the creator chooses otherwise. It is not presumed centered. |
| Concentration | 16296–16304 | `04c55227b54b4481f715a64b6a517f63f5733171d475640db0f6f43d355cc1be` | Concentration checks for the caster’s separate effects retain their own trigger and DC; this does not make Warding Bond itself Concentration. |
| Restrained [Condition] | 17066–17074 | `534f630cbdb2b9eee71b37543cb5f29af4617f829c0ab4b905604f69bfdbcf3c` | Restrained sets Speed to 0 so it cannot increase, gives Advantage to attacks against the creature and Disadvantage on its attacks and Dexterity saves. |
| Ritual | 17078–17080 | `3f4bc6da069b6634f84d1f834314e621a2b601f777d57d06e74d39bcd7514866` | A prepared Ritual spell takes ten minutes longer, spends no slot and cannot be upcast. |

## Cumulative accounting and preserved lanes

All counts below derive from exact key/category identities and the seven validated evidence arrays. They are not inferred from record counts alone.

| Measure | Before seventh batch | Seventh delta | Cumulative after seventh |
|---|---:|---:|---:|
| Reviewed source-blocking keys | 71 | 6 | 77 |
| Source evidence/subobligation records | 74 | 7 | 81 |
| Source-closed keys | 56 | 4 | 60 |
| Source-closed subobligations | 59 | 5 | 64 |
| Source-held keys | 15 | 2 | 17 |
| Source-held subobligations | 15 | 2 | 17 |
| Active source-blocking keys | 21 | −4 | 17 |
| Active source-blocking entries | 20 | −3 | 17 |

All 15 prior `SOURCE_HELD` subobligations remain held with their existing residuals unchanged: Aid health normalization; Arcane Lock destruction/access; Create or Destroy Water container/extent; Detect Magic aura overlay; Gentle Repose corpse/revival binding; Locate Animals or Plants eligible search domain; Magic Missile grouping; Magic Mouth episode frequency; Mending repair/missing matter; Pass without Trace selection timing; Prayer of Healing responder census; Ray of Frost movement floor; Resistance damage grouping; Spike Growth displacement/distance; and Unseen Servant subject classification. The two new holds are Familiar’s complete eligible-form census and Warding Bond’s copied-damage policy. No old hold is absorbed into the selected key subtraction.

All 33 original `FUTURE_PROOF` subobligations remain `NOT_ESTABLISHED`. Find Familiar and Warding Bond retain their distinct downstream native-proof obligations. The `source_unknown_classifications` array remains the original 82-key classification/history; the derived active source set changes only through exact closed source subobligation IDs.

The conditional Thunderclap installed-default repair remains `REQUIRED_BEFORE_PACKAGE_PROMOTION`; this batch selects no replacement and does not alter legacy snapshots or accepted work. Word of Recall’s source-modeling residual remains `NOT_ESTABLISHED`; no redesignation, replacement, survival, latest-wins or automatic-cap rule is inferred. Public source mapping, materialization, source-decomposition/support, and default-repair blockers remain independent. Source qualification remains not established; no 339-spell source-ready declaration, recipe completeness, consumer admission, native execution/recovery, or package promotion follows.

## Scope and impact

The bounded integration changes the existing source-qualification schema, positive fixture, validator, focused tests, and rejected fixture only for additive seventh-batch negatives; it adds this design evidence record. The rejected fixture’s prior 18 base negatives and 11 sixth-batch negatives remain unchanged. Original source registry roots, historical map/index values, all earlier evidence arrays, common qualifiers, 15 holds, 33 future-proof obligations, Thunderclap default repair and Word of Recall residual are preserved.

No source recipes, GAME/runtime members, package identities, native consumers, content eligibility, database/persistent contracts or execution behavior are changed. The source-only record adds no runtime spell ID, Activity, capability, action entitlement or output claim.

**VERSION_IMPACT: NONE** — this is an additive pre-release DEV-only evidence extension to the existing draft source-qualification schema version 1. It does not change a released persistent/runtime protocol, runtime package member, compatibility generation or digest contract. The schema remains version 1 under `DEV/RELEASE/VERSIONING.md` §§4 and 7 and the canonical versioning policy §§2 and 12; no GAME/DEV projection is affected.

**SYSTEM_IMPACT: NONE** — source disposition/evidence only; the held source members and every downstream/native obligation remain explicit.

This work includes material from the System Reference Document 5.2.1 ("SRD 5.2.1") by Wizards of the Coast LLC, available at <https://www.dndbeyond.com/srd>. The SRD 5.2.1 is licensed under the Creative Commons Attribution 4.0 International License, available at <https://creativecommons.org/licenses/by/4.0/legalcode>.
