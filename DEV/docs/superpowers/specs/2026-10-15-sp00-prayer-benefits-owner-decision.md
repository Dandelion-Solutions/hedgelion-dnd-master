# Prayer of Healing — accepted benefits interpretation

Status: **ACCEPTED PRODUCT OWNER DECISION — IMPLEMENTATION-FACING LAW**
Date: 2026-10-15. Canonicalization candidate awaits independent critic, Senior Stop2 and coordinator integration/publication; no self-GO.

## 1. Authorization, scope and ownership

The Product Owner's exact reply **“да, все три”** accepts the final three recommendations in the [R2 Decision Brief](../design/2026-10-15-sp00-prayer-benefits-decision-brief.md): **BROADER-7 / NO mount-pace renewal / DIFFERENTIATED restrictions**. This is the sole final normative owner of those Prayer interpretations and their affected-target qualification. They are accepted HDM source interpretations, not a claim that every bridge is literal SRD wording. The former fourth question was already resolved mechanically from common source; it is not a fourth policy approval.

This decision supplements [execution](2026-10-04-local-spell-execution-contracts.md) §§2,4,6,10 and [lifecycle](2026-10-04-local-spell-lifecycle-contracts.md) §§5,8 under the [main spell specification](2026-10-04-local-spell-execution-canonical-spec.md) §§23,25–27. [Health/rest](../../../ARCHITECTURE/HEALTH_EFFECTS_RECOVERY.md) continues to own actual RestPolicy qualification and native health/recovery closure. No new state owner, generic rest domain/service, universal completion event or blanket GM adjudication follows. The [A–F decision](2026-10-14-sp00-source-interpretation-owner-decision.md) is unchanged.

The accepted policy is fixed for later exact recipe/profile/source binding. Implementation proof must satisfy it; absence of a consumer is a hold, not permission to narrow benefits or choose another bridge. This document selects no active registry member, machine generation, executable profile or recipe. Later policy changes require an explicitly superseding accepted decision, not a favorable post-outcome ruling or silent reinterpretation of accepted work.

## 2. Benefits-only grant and conditional census

Source: [adopted SRD5.2.1](../../SRD_CC_v5.2.1.md), R13973–13987; R17125–17142; Recharge R22038–22042. R denotes inclusive one-based Markdown lines. Whole source RAW_UTF8 SHA256: `c03c41b7c94d644646c8f979541b1664036a107e03823797ab1afac4b6e0b01e`.

At completion of the 10-minute, V casting, up to five chosen creatures must have remained within 30ft for the entire casting. Eligible recipients gain Short Rest benefits and separate direct healing of 2d8, plus 1d8 per slot level above2. No casting-ability addend is imported. Actual health/LifeState eligibility, prohibitions and caps remain native; absence of a positive-HP target condition is not resurrection permission.

Prayer grants legal benefits, **not RestActivity completion**: no elapsed hour, ordinary positive-HP rest-start predicate or ordinary-rest interruption rule is imported. It supplies no missing feature, class/subclass, equipment, spellbook study, attunement, focused/contact identification activity, item-use action or Reaction. Source-specific prerequisites still apply.

The [full census JSON](../research/2026-10-15-prayer-short-rest-responder-census.json) retains each `sourceID`, full `sourceSpan` text/hash/bounds, `sourceDependency`, actual-grant `condition`, `resetOptionality`, `quantitySubject` and `LongRestTargetGate`, plus item-level match/exclusion dispositions. These are evidence locators, not admitted machine IDs. Corrected partition, using one-based rows and zero-based `/responders/N`:

- **107 ordinary rows:** 1–11,15–17,20,22–27,29–114.
- **7 completion-benefit rows:** 12,13,14,18,19,21,28, accepted below.
- **114 conditional source records total**, not114 benefits for every recipient. The declared mechanical search accounts for50 Short-Rest and87 numeric-Recharge match lines;86 concrete numeric monster features are rows29–114. This is bounded adopted-corpus membership, not universal rest-domain coverage or native support.

The [historical report](../research/2026-10-15-prayer-short-rest-responder-census.md) and [verification](../research/2026-10-15-prayer-census-verification.json) retain their original108+6 labels and77/67/10-era state. Tireless moves into the seven-row interpretation set; no source row is added or removed. Their pre-acceptance gap/status wording is historical and superseded here, not reconstructed as if originally accepted. Every retained row's Prayer-specific guard is qualified by §§4–5: an affected target consumes its gate, while proved all-blocked selection alone does not. No historical rest-eligibility/dependency label imports ordinary rest-start predicates.

### Ordinary benefits remain exact per actual grant

- HD spending is optional, one native available recipient die at a time, with another choice after each roll; heal `max(1, die roll + recipient Constitution modifier)` before applicable source modifiers/cap. Mixed class dice and actual stat-block dice remain distinct; do not invent dice for magically created creatures lacking them. No spent-HD refill or caster-derived quantity.
- Recover exactly each feature's one/all/limited amount. Rage, Cleric/Paladin Channel Divinity, Wild Shape and Second Wind regain one expended use; their separate pools remain separate. Tactical Mind consumes the same Second Wind pool. Action Surge recharge is availability, not an immediate extra action/turn. Font-enhanced Bardic Inspiration, Focus, Pact Magic, Adrenaline Rush and Signature free castings retain their own capacities/identities. Relentless Rage resets DC10; Stroke of Luck/Boon of Fate regain availability, not immediate success.
- Natural Recovery and Arcane Recovery retain selected expended slots totaling at most ceil(actual class level/2), each below6; Sorcerous Restoration retains at most floor(actual Sorcerer level/2) expended points. Use consumes each feature's independent until-own-Long-Rest gate; Prayer never resets it. Arcane Recovery still requires actual spellbook study. Ordinary Spellcasting slots, Natural Recovery's separate free Circle casting, Magical Cunning, Mystic Arcanum, Innate Sorcery and other Long-Rest-only uses do not refill.
- All86 actual numeric Recharge features, **including Recharge6**, refresh without a recharge d6 at this benefit edge. Turn-start recharge rolls remain separate; `X/Day` remains Long-Rest-only. Cloaker Phantasms refreshes its actual rest-use grant; secondary dragon actions without independent recharge annotation are not extra resets.
- Hat Unknown Spell resets only its used successful-cast property for an actual attuned Wizard user; Quarterstaff Attack Deflection resets the spent property for its actual attuned user, retaining form/holding/trigger/Reaction requirements. Neither grants attunement or performs the use.
- Actual form/acquisition/retention/suppression and body/Constitution/HD bindings determine current grants. Periapt of Wound Closure, Potion of Vitality and Sewer Plague retain their source-specific HD-healing modifiers; they do not generically modify Prayer's spell d8s. Life-domain casting/healing features retain their actual feature/slot/recipient/timing predicates; no default addend or automatic attribution to HD healing follows. Full modifier composition remains native proof, not a new census claim.

## 3. Exactly three accepted choices

### BROADER-7 — include these possessed completion opportunities

| Row / JSON pointer | Source span | Accepted benefit and retained limit |
|---|---|---|
| 12 / `/responders/11` Tireless | R4860–4867 | Actual Ranger10+ feature decreases Exhaustion, if any, by1. Never refills its Long-Rest-only temporary-HP action uses; no general Exhaustion relief for others. |
| 13 / `/responders/12` Hunter's Prey | R5009–5016 | Actual Hunter3+ feature may exchange Colossus Slayer and Horde Breaker; no subclass grant or both-options grant. |
| 14 / `/responders/13` Defensive Tactics | R5019–5026 | Actual Hunter7+ feature may exchange Escape the Horde and Multiattack Defense; no new feature grant. |
| 18 / `/responders/17` Pact of the Tome | R6124–6131 | Actual invocation conjures its Book of Shadows in hand, with three cantrips and two level1 Ritual spells from any class list, not already prepared; they function as Warlock spells and are prepared while the book is on the recipient. Replacement makes the old book disappear; death also ends it. Its focus property remains source-owned. Prayer grants no invocation or arbitrary spell list. |
| 19 / `/responders/18` Fiendish Resilience | R6351–6354 | Actual Fiend Patron Warlock10+ feature chooses a non-Force damage type; Resistance lasts until another feature choice. No random type or generic refill. |
| 21 / `/responders/20` Memorize Spell | R6500–6503 | Actual Wizard5+ feature and actual spellbook study may replace one prepared level1+ Wizard Spellcasting spell with another level1+ spell from that book. Prayer supplies neither book nor study. |
| 28 / `/responders/27` Erinyes Magic Rope | R25109–25116 | Actual trait may fully restore its own damaged/destroyed rope. No unrelated gear repair; rope bearing/action and destruction rules remain source-owned. |

### NO — mount-pace renewal

R1087–1090 requires an actual Short or Long Rest after the doubled-distance hour. Prayer alone does not renew that travel pace. A fatigued riding horse may receive eligible recharge/HD/direct healing without becoming eligible for another boosted hour. Feather-token bird downtime (R19542), Rod of Security's elapsed-hour HD-like healing (R20960), and other elapsed/rest-activity requirements remain separate; no elapsed time or cooldown reset is fabricated.

### DIFFERENTIATED — taking-rest prohibition versus benefit denial

| Restriction | Accepted Prayer behavior |
|---|---|
| Simulacrum, R14825–14840 | Cannot take Short/Long Rests, but may receive otherwise-eligible **nonhealth** recharge/completion benefits on actual retained grants. Its HP remains repair-only: during its creator's Long Rest, within5ft,100GP components per HP. No Prayer direct HP healing or HD healing bypasses that law. It is a separate Actor with its **own** Prayer gate; creator Long Rest/repair never resets it. Under the current no-rest rule it cannot itself finish the required Long Rest. |
| Incubus Restless Touch, R27244–27255 | Until its curse ends (24h or incubus death), deny Prayer's **entire rest-benefit branch**, including HD and BROADER-7. Separate direct spell healing is not denied by this curse; it still requires independent health eligibility. |
| Rakshasa Cursed Touch, R29285–29298 | While cursed, deny that same whole rest-benefit branch; separate direct healing still follows actual health law. Preserve its broader Short/Long-Rest-benefit denial, not Incubus's timed curse or Simulacrum's taking-rest prohibition. |

## 4. Affected-target qualification, cost and replay

Common Effects R9217–9219 and Invalid Targets R9223–9235, healing cap R1470 and Prayer R13985 govern this mechanically resolved boundary:

1. A lawful benefit/application or eligible opportunity affects the creature even with **zero numerical delta** or declined optional HD/recovery. Full HP, already-full eligible pools and declining optional benefits do not permit repeated Prayer applications.
2. If **all** benefit applications are actually prohibited/inapplicable, nothing happens to that target. Selection/casting completion alone does not consume its gate; the gate cannot bootstrap its own consumption as a separate detrimental effect.
3. **Unknown eligibility is not all-blocked.** Missing source/grant/health/dependency completeness is a scoped hold, not proof of absence, successful effect or an unconsumed/allowed state. Proved no effect cannot clear an already consumed gate.
4. No refund: a slot actually used remains expended under R9235; all other actual source costs remain. A genuine new casting requires normal time/components/slot/agency and costs. No automatic retry loop or free reroll is granted. Replay/recovery of the **same accepted attempt** reuses fixed RNG/results and identities; neither spending nor application occurs twice. Countered/interrupted/no-slot cases retain their existing exact source costs, not a blanket expenditure or refund rule.

The recipient-native target gate retains lifecycle §8's `{consumed, reset_boundary_id, last_transition_occurrence}` and target identity; only **that target's own accepted Long Rest** resets it. Another caster, higher slot, another creature's/party's rest, creator repair or Prayer's own rest benefits do not reset/bypass it. It is neither the common caster slot gate nor IntentPlan/clause authentication.

## 5. Required cases and later native proof

These are implementation acceptance obligations, **not executed tests**:

| Case | Required outcome |
|---|---|
| Seven completion opportunities | Hunter10 with Tireless and Exhaustion1 can reduce it to0 and exchange either possessed Hunter option; no Tireless temporary-HP-use refill. Tome replacement retains exact choices/old-book cleanup; Fiend choice excludes Force; Wizard without actual book/study cannot Memorize or Arcane Recover; Erinyes restores only its own rope. Missing feature/grant never becomes eligible from census membership. |
| Native HD/resources | Optional recipient dice spend with correct modifiers, mixed dice and no refill; exact one/all/limited recovery and independent feature gates; Recharge6 refresh without d6 versus unchanged X/Day; absent/retained/form grants and item prerequisites checked. Full eligible pool or declined recovery still counts as affected. |
| Benefits, not rest | Zero-HP otherwise-lawful creature is not excluded merely by ordinary rest-start predicate; actual LifeState/health law still applies. No hour/RestActivity/identification/attunement is manufactured. Mount receives lawful healing without renewed doubled pace. |
| Differentiated branches | Cursed wounded Fighter gets eligible direct healing but no Second Wind recovery or other rest benefit. Replica with spent actual Pact Magic can recover eligible slots but no HP; subsequent cast is barred by its own consumed gate. Creator repair/Long Rest does not reset it. |
| PRAYER-ZERO-ALL-BLOCKED | Replica under active Incubus or Rakshasa curse: rest branch denied, HP healing repair-only; with complete evidence no lawful benefit survives, so application does not newly consume its gate. Uncursed replica lacking every otherwise-eligible nonhealth benefit is the same edge only if absence is proved. |
| PRAYER-ZERO-LAWFUL | Full-HP recipient with an eligible lawful application/opportunity or declined HD is affected despite0 delta; consumes its own gate. Replica with lawful nonhealth benefit is affected despite0 HP repair. Do not use HP delta as gate predicate. |
| PRAYER-UNKNOWN | Incomplete grant/health/absence evidence holds affected scope; cannot infer all-blocked or grant permission. Neither unknown nor proved no effect clears a previously consumed gate. After curse expiry, a later real cast checks current grants and existing gate anew. |
| Native TargetGate/cost/replay | Couple lawful benefit/HP/resource/Effect/Asset changes and target-gate consumption under complete native currentness/atomic closure; prove stale, denied and partial-preparation negatives. Same accepted attempt across crash/replay preserves fixed RNG, identities, costs and single application. Genuine new cast pays again; another caster/slot/other target Long Rest cannot bypass the consumed gate. Only recipient accepted Long Rest resets it. |

Native owners remain separate: HP/LifeState on Actor, resources at their source-owned Actor/Asset/Procedure, Effects/assets/progress on their accepted owners. Preserve source-defined choice and simultaneous closure; the source does not impose an invented universal ordering between optional HD and direct healing. Missing exact consumer support holds admission rather than granting arbitrary resources, broad GM repair or a generic rest event.

Original key62 `source.spell.prayer_of_healing.unresolved.responder_census` remains **SOURCE_HELD** until the registry/source mapping binds this decision and exact census/prerequisites. `/source_unknown_classifications/62`, `/source_mapping_lanes/0/mapping_payload/unresolved_key_index/62`, current `/source_mapping_lanes/0/mapping_payload/entries/98` and its separate downstream native-proof obligation remain unchanged here. Normative approval is not source-registry closure, fixture acceptance, full339 support, native conformance or production readiness. Current machine accounting77 reviewed/70 resolved/7 held is preserved; default/Word of Recall/33 future-proof and independent auth/turn lanes retain their actual gates.

**VERSION_IMPACT: NONE.** This DEV-only accepted interpretation and routing changes no active module/profile/schema/catalog/package, persisted contract or digest-generation rule. Future actual materialization must assess every affected namespace and synchronize required projections under the [version owner](2026-09-05-hdm-versioning-namespace-compatibility-policy.md). **PRODUCTION_CLAIM: NONE; SOURCE_READY: false; FUTURE_NATIVE_PROOF: NOT_ESTABLISHED.** [Canonicalization provenance and propagation](../design/2026-10-15-sp00-prayer-owner-canonicalization.md) records the bounded source basis and pending review/integration gates.
