# SP00 Find Familiar source-census integration

Status: **BOUNDED SOURCE-ONLY INTEGRATION EVIDENCE**

This record closes one existing Find Familiar source-mapping subobligation from an independently reviewed, frozen SRD census. It does not create or admit a runtime creature, action, sense, spell, package member, native consumer, or full-spell readiness claim.

## Frozen source basis

| Evidence | Exact identity |
|---|---|
| Integration base | `75bc49af2fc6ca3159c18c4e59fd63befaa0894b` |
| Accepted R2 mechanical census | `/tmp/hdm-dev/spell-recovery/SP00-familiar-full-census-20261014.json`, SHA-256 `f3671f452d6d382abdae3f89318da03ac79743ba60bfa0a159c24dafac4eec0d` |
| Accepted R2 typed prerequisite ledger | `/tmp/hdm-dev/spell-recovery/SP00-familiar-prerequisites-20261014.json`, SHA-256 `5869ec71cf99487e28c6d0400e3583ceee80daafc300559e9483818c7dd7800f` |
| Frozen R2 manifest | `/tmp/hdm-dev/spell-recovery/SP00-familiar-R2-manifest-20261014.json`, SHA-256 `44d8c10b03f1e3276bf11ad0fc0f29dd9761d91decbcfaf7010fb50a3a51f0c7` |
| Independent full R2 source review | `/tmp/hdm-dev/spell-recovery/SP00-familiar-full-census-R2-review-20261014.md`, SHA-256 `bd878a6746e71705db8d2d7c0947cb2ed8239086a93d932a275832e57d6a6405`; ruling: `PASS` for F01–F03 and all PR01–PR37 |
| R1 body-review identity reused by R2 | SHA-256 `2867feaa6d9bbd62c59fbddcfc4f6681305b2ceb5c86db273123c608d4d0d55c` |
| Primary SRD | `DEV/docs/SRD_CC_v5.2.1.md`, Git blob `45392ab96e8adfeba66694bca8950b6ce1a71797`, raw UTF-8 SHA-256 `c03c41b7c94d644646c8f979541b1664036a107e03823797ab1afac4b6e0b01e` |
| Current Find Familiar body | Lines 11609–11629, SHA-256 `ab7a578e4bd70abb8a5c3d57a0733b0a5dfd33f2b444ae17b488f68437bd3b98` |

The separate R2 review is the accepted independent semantic review: PASS for F01–F03 and PR01–PR37, recommending SOURCE_CLOSED only for the original census source-mapping subobligation. Its finite adopted-SRD scope and five separately qualified input boundaries remain binding; native admission, packaged execution and FUTURE_PROOF remain NOT_ESTABLISHED. R1's unchanged 24-body review is reused. This integration reuses that ruling and frozen identity; it does not claim to repeat the independent review. The repository fixtures retain the complete ordered 151 source-reference rows and all 673 root/member-body joins, all 37 root meanings, subject roles, applicability, predicates/outcomes, conditional contexts and non-goals. Exact source prose remains recoverable from the tracked primary SRD spans rather than being duplicated.

## Exact scope closed

The sole resolved key is `source.spell.find_familiar.unresolved.eligible_form_census`, original classification index **30**, subobligation `::source_mapping_review`, current-map entry **48**. Its historical classification, original reason/evidence, source-ready blocking flag, map row, and seventh-batch `SOURCE_HELD` record remain unchanged. The new ninth source-evidence record resolves only that one source subobligation; it does not overwrite the historical HOLD or the separate `::downstream_domain_consumer_admission_native_proof` obligation.

The accepted source predicate is exactly **creature type Beast AND Challenge Rating equal to 0**. The adopted Monsters A–Z / Animals source domain contains **330** statblocks: 235 Monsters A–Z and 95 Animals. The disjoint accounting is 330 = 24 eligible CR 0 Beasts + 5 CR 0 non-Beasts + 60 nonzero-CR nonswarm Beasts + 7 swarms + 234 other nonzero-CR non-Beasts. **“Swarm” is not an independent eligibility exclusion predicate**; the seven actual source swarms are excluded by their exact source type/CR records, and the machine proof must not manufacture a broad future swarm ban.

The 24 complete source bodies remain in the pinned primary SRD and are linked by their exact original spans/raw hashes in `DEV/TESTS/fixtures/spell-familiar-source-census.json` (fixture SHA-256 `28c16ff9717cb066a316bbd8442944dc7cbd3400079f1cd88a460b76e3fc05ae`). The named eleven remain examples; the additional thirteen are a positive catch-all result, not an expansion beyond the predicate. No source size restriction is added. All 23 source attacks are prohibited for a familiar. Seahorse Bubble Dash remains an underwater-only Action; Octopus Ink Cloud remains a conditional 1/Day Reaction. The three Pack Tactics traits remain attack-roll benefits only. No attack relay is classified by this source ledger.

The complete bounded prerequisite ledger is retained in `DEV/TESTS/fixtures/spell-familiar-source-prerequisites.json` (fixture SHA-256 `8fcde530c41b8f67b85f71b679f9236d9f434615e9bc6ab69b64e3824b55ad63`). Its entries losslessly retain the accepted R2 root carriers, 151 source references, 673 member-body joins and all five input qualifications. References resolve to the spell body, the census's indexed original 49 support-clause catalog, or the 33 new clause locators. The validator derives the ordered reference digest from retained rows, resolves every collection/index/span/hash and member index/span/applicability, and checks complete accepted semantic identity. Counts and digests supplement these durable rows; they do not replace them. The general non-attack action roster remains eleven: Dash, Disengage, Dodge, Help, Hide, Influence, Magic, Ready, Search, Study, and Utilize.

`DEV/TOOLS/build_spell_familiar_source_evidence.py` is a deterministic stdlib-JSON producer for the prerequisite fixture. The coordinator authorized this derivative-only tool for the durability repair. Explicit `--census` and `--prerequisites` historical inputs must match the two accepted raw SHA-256 identities before generation; duplicate keys and non-closed input shapes fail. `--check` verifies byte-for-byte regeneration without writes. The producer adds no semantic rule, review ruling, source closure or gameplay authority. Historical scratch paths above are provenance labels only: ordinary validation and cold recovery use tracked fixtures, the schema and the tracked SRD, with no producer execution, network or external scratch dependency. A changed source requires new accepted evidence and review, not an automatic roster update.

Help stabilization and knockout first aid are separate conditional applications of Help/Action. Stabilization applies to an eligible other creature at 0 HP with a successful DC 10 Wisdom (Medicine) check; no Medicine proficiency requirement is invented. Stable still means Unconscious, and damage ends Stable status. Knockout first aid ends only the applicable knockout Unconscious state and grants no healing. Creating the knockout state requires a melee attack and is not a familiar permission. A familiar at 0 HP disappears; no on-scene self-stabilization exception is created. The source supports no universal hands, voice, language, proficiency, tool, or spellcasting defaults for forms.

The declared terminals remain bounded source clauses, not a native graph. Actual selected touch spells, separately granted features/items/spells, objects or improvised tasks, environmental states, and affected targets/effects remain five parameterized inputs. The selected touch spell's attack/save/statistic classification remains undecided here. The spell's 100-foot predicates apply to telepathy and touch delivery; this integration does not introduce a universal command or sensory leash. Completeness is bounded to the adopted SRD 5.2.1 Markdown index, Monsters A–Z and Animals domains plus the declared finite terminals; it is not universal transitive game-content closure. Other editions/books, delivered spells/items/objects, templates and custom variants are outside this census. No fresh PDF visual recheck is claimed. A source/domain change requires recomputation and independent review rather than reuse of this roster.

## Derived registry disposition

All counts are derived from exact existing keys, source subobligations, and dispositions—not hand-entered as replacement totals:

| Measure | Before this integration | Delta | Derived result |
|---|---:|---:|---:|
| Original classifications / source-blocking keys / downstream-only keys | 82 / 77 / 5 | 0 / 0 / 0 | 82 / 77 / 5 |
| Distinct resolved keys | 66 = 60 SOURCE_CLOSED + 6 OWNER_DECIDED | +1 source closure | **67 = 61 SOURCE_CLOSED + 6 OWNER_DECIDED** |
| Resolved subobligations | 70 | +1 | 71 |
| Current source HOLD keys / source subobligations | 11 / 11 | −1 | **10 / 10** |
| Resolution records | 87 | +1 | 88 |
| Future-proof subobligations | 33 | 0 | 33, all `NOT_ESTABLISHED` |

Derived source closure: 67 resolved keys = 61 SOURCE_CLOSED + 6 OWNER_DECIDED; 10 source HOLDs remain. The exact remaining ten source holds are Arcane Lock destruction/access, Create or Destroy Water container/extent, Detect Magic aura overlay, Gentle Repose corpse/revival binding, Locate Animals or Plants eligible search domain, Magic Mouth trigger/episode frequency, Mending repair/missing matter, Prayer of Healing responder census, Spike Growth displacement/distance, and Unseen Servant subject classification. The accepted six-section A–F owner decision remains unchanged at its original source path/SHA-256/Git blob and exact six-key scope. `Word of Recall` remains `NOT_ESTABLISHED`; the conditional Thunderclap installed-default repair remains `REQUIRED_BEFORE_PACKAGE_PROMOTION`.

The registry still has 82 historical classifications and source-map obligations; source closure of this one key does not turn the 339-spell map into a closed source roster. Other unresolved source lanes, the 33 future-proof obligations, native consumer proof, package promotion, and source-ready admission remain open. `source_qualification_status` remains `NOT_ESTABLISHED`; `source_ready_gate.ready` remains false. Boundary: native consumer admission, action execution, and full-339 readiness remain `NOT_ESTABLISHED`. No native archetype, feature, Activity, selector, recipe, executor, runtime member, release, or installed package readiness is established.

## Change and impact boundary

Changed owners are limited to the DEV source-qualification schema, its positive/rejected fixtures, validator/test, two bounded source-evidence fixtures, the derivative-only evidence producer, and this design evidence. Original classification rows, source history, all earlier resolution batches, six owner decisions, default repair, Word of Recall residual, and prior fixture identities are retained. No `GAME/` path, source map, production catalog, 339-entry inventory, cursor, shared Git index, commit, or publication is in scope.

**VERSION_IMPACT: NONE.** The accepted W05.SP00 owner treats this as additive DEV-only evidence within source-qualification draft `schema_version: 1`; no released package/protocol, runtime module, catalog generation, semantic package member, persistent schema, or digest contract changes.

**SYSTEM_IMPACT: NONE.** This closes only the existing bounded source subobligation. It introduces no runtime/executable primitive, consumer, state, authority, package admission, source-ready gate, or user-facing behavior.

This work includes material from the System Reference Document 5.2.1 (“SRD 5.2.1”) by Wizards of the Coast LLC, available at https://www.dndbeyond.com/srd. The SRD 5.2.1 is licensed under the Creative Commons Attribution 4.0 International License, available at https://creativecommons.org/licenses/by/4.0/legalcode.
