# SP00 source interpretation - independent targeted re-review

Status: **REVIEW COMPLETE; SIX NARROW OUTCOME POLICIES REMAIN NEEDS_PO. Unsupported equal-alternative framing corrected; no gameplay policy selected.**
Date: 2026-10-14.
Pinned source HEAD: fc3ffd5cb92c71676e92447df71f4d36942730c8.
Role: HDM Architect / targeted Senior source-and-owner reviewer. Two disjoint independent reviewers checked A/D/F and B/C/E against the same source; neither authored a gameplay choice or changed code.

## Bounded dependency subgraph and Source Manifest

The scope is the six held SP00 keys in the 2026-10-13 Decision Brief, their exact SRD bodies and shared arithmetic/lifecycle consumers. It is not a complete339 re-audit, implementation review or permission to reopen accepted mechanisms.

| Source | Exact relevant anchors / qualification |
|---|---|
| Current AGENTS.md, CHATGPT_WORK runtime, both DESIGN_PROCESS owners, PROJECT_MAP, CURRENT_PROGRESS and Wave05 execution-status | Current role, Connector-only transport, genuine human versus agent decisions, existing source holds and independent continuation |
| DEV/docs/SRD_CC_v5.2.1.md | Current blob45392ab96e8adfeba66694bca8950b6ce1a71797; exact decoded UTF8 read through Connector fetch_blob. fetch_file returned empty for the1.586MB file and was not used as evidence. |
| SRD A/B/C/D/E/F | Aid9305-9321; Magic Missile13255-13273; Pass without Trace13733-13747; Ray of Frost14270-14286; Resistance14388-14401; Warding Bond15809-15825 |
| SRD shared consumers | Ordinary damage1396-1400; shared saving-throw damage1412-1418; types1426-1430; defenses1434-1456; source-specific exceptions around525; same-spell arbitration9255-9257; Concentration16296-16304; actual simultaneous ordering17143-17147; Speed17163-17169; zero-Speed consumers1215/16541/16603/17032; targeting9225-9231 and Emanation16547-16549 |
| DEV/ARCHITECTURE/HEALTH_EFFECTS_RECOVERY.md | Health/LifeState26-44, sole physical amounts and maximum clamp; native lifecycle extension102-106; generic clamp is not complete spell-specific current-bonus expiry policy |
| 2026-10-04 spell main/execution/lifecycle accepted specifications | Mainsection section 10/14/26; executionsection section 5/6 exact normalization/group/instance closure; lifecyclesection section 6/7/8 damage grouping, concentration and turn occurrence |
| MECHANICAL_CONTEXT, CALCULATION_SELECTOR_METADATA, PORTABLE_ACTIVITY_VALUES, ACTOR_MODEL, DOMAIN_RULES_COVERAGE | Existing read/normalization/continuity/native/procedure constraints; no newly selected source-specific policy inferred from generic module name |
| Current character-mvp-seed.json | Magic Missile ordered bounded dart bindings around687-705 are structural seed evidence; not final complete producer/RNG/Concentration/simultaneity authority. Existing source hold is not discharged by fixture iteration. |
| Current official Sage Advice Compendium | https://www.dndbeyond.com/sources/dnd/sae/sage-advice-compendium retrieved2026-10-14; bounded searches of these names/damage/Concentration. The temporary-HP Concentration clarification confirms taking damage differs from physical current-HP loss. No found answer closes the exact six operational policies. External guidance is corroboration, not silently admitted HDM law. |
| Separately labeled2014 compendium | https://www.dndbeyond.com/sources/dnd/sac/sage-advice-compendium checked for applicability only.2014 generic shared-roll rationale, designer tweets and secondary reposts are not2024/SRD5.2.1 authority. |

Evidence was extracted with source-versus-inference qualifiers, negative alternatives and concrete outcome witnesses. All six exact bodies and relevant general-rule clauses were read; headings or a representative spell did not substitute for coverage.

## Per-item disposition

### A - Aid: narrow the question to the complete effective-bonus transition

Source increases both maximum and current HP for its duration, and same-spell arbitration already excludes independent stacking. Therefore clamp-only and reversible current contribution do not have equal textual support. Health's generic maximum clamp is required in either model but does not override the current-increase duration.

Genuine gap remains after damage/healing/zero-floor and winner changes: exact effective current-bonus expiry/application delta, and associated LifeState consequence. Proposed profile: change current HP only by the change of the effective applicable Aid bonus, respect current maximum and zero floor, preserve independent damage/healing, never restore entry HP or repeatedly heal from equivalent arbitration. Winner selection follows highest potency/latest equal potency. This is a recommendation, not an accepted arithmetic policy.

Distinguishing witnesses: max20/current12, bonus5, damage8 leaves9 before end; clamp-only leaves9 and removing effective5 leaves4. Current2 before expiry can reach0 without taking damage; no invented damage/death-save failure. Entry while dying/stable/dead, stronger/weaker overlap, suppression/resumption and current healing need explicit accepted cases. Aid current increase is not temporary HP.

Confidence: HIGH that complete operational semantics remain unresolved; HIGH that reversible duration-bound interpretation is textually stronger.

### B - Magic Missile: separate RNG default from damage-instance choice

Each dart has its specified damage dice; ordinary rolling rules support an independent draw per dart. The current shared-roll rule applies to simultaneous saving-throw damage and does not apply to this no-save spell. Shared draws are an explicit departure requiring authority, not an equally justified2024 default. Separate draw fixed-result/retry handling is ordinary source realization.

A narrower material policy remains: simultaneous darts against one creature grouped as independent damage instances/checks versus one per-target combined instance. Concentration text does not define simultaneous dart aggregation; accepted lifecyclesection 6 expressly requires source-local count/order closure. Separate dice alone do not prove separate saves.

Recommendation: per-dart draws and per-dart native damage/Concentration instances, all in the same simultaneous group. Three damaging darts can require three saves if the target is still concentrating; required checks are not universally or fictionally sequential attacks. Required simultaneous choice follows the actual turn controller; engine row order cannot replace it. Health/zero/death-save/reduction/rounding and early concentration end must be joined consistently.

Confidence: HIGH on ordinary separate draws; HIGH on remaining instance-policy gap.

### C - Pass without Trace: membership timing remains unresolved

The source fixes current aura occupancy plus chosen membership, not the time or cost of updating that membership. General targeting/geometry do not fill that omission. Spirit Guardians around15041 explicitly locates its designation at casting; that contrasting wording is not permission to import its timing into Pass without Trace.

Recommendation: commit selected identities at casting, keep selection through lawful leave/reentry, activate benefits only while inside the current aura; do not add free reassignment or a new ongoing caster-to-target range leash. A later previously unselected entrant distinguishes outcomes. This is an HDM interpretation proposal.

Confidence: HIGH on genuine timing gap.

### D - Speed: do not disguise public semantics as a representation detail

Speed denotes coverable distance; a final nonnegative distance is the strongest domain interpretation. Nevertheless, the source's0-or-less rule is specifically remaining movement after switching speeds, not an explicit universal floor on derived Speed. Accepted policy-profile admission demands exact minima/composition but does not choose that floor.

Signed public Speed changes exact-zero checks for Dodge, voluntary Prone, standing and flying. Therefore silently retaining-5 is not harmless internal arithmetic. Recommendation: floor the final derived movement capability at0 after the lawful applicable composition, retain raw negative contributions and exact special-speed changes, test all zero consumers. Do not clamp each modifier independently or claim a schema minimum supplies runtime behavior.

Confidence: HIGH on observable difference; MEDIUM on whether a future explicit nonnegative-domain owner clarification can be purely technical. At this reviewed gate, the result-changing interpretation remains explicit pending judgment.

### E - Resistance: automatic occurrence is source-supported; allocation remains a choice

The source prescribes reduction when eligible chosen-type damage occurs and grants no elective withholding or Reaction. Automatic first eligible positive damaging occurrence of each actual turn is the source-grounded rule; a player-selected later occurrence adds unsupported optional agency and is not an equal reading. The ordinary damage-adjustment-before-defense order is already selected by the SRD.

Only mixed-type allocation remains genuinely unresolved. Proposed bounded policy: subtract one fixed d4 only from the chosen-type subtotal, with zero floor and no spill to unrelated types, then apply each ordinary type defense. Do not roll per component or give a new arbitrary component-allocation choice. This allocation is a recommendation awaiting PO, not already-established RAW. Fully prevented damage, effect-ordering and actual grouped occurrence eligibility must be specified without consuming the gate merely because a raw component exists.

Golden witness:5Fire+5Cold, selectedFire, ordinary Fire Resistance, d4=3: chosen-type-only produces floor((5-3)/2)+5=6; Cold allocation produces floor(5/2)+(5-3)=4. Equal proportional allocation has its own integer-remainder choice and is not a cost-free technical substitute.

Technical correction: lifecyclesection 7 formerly said per target turn. The source says each actual turn;section 8 already stores the target-local gate by actual turn occurrence. Correct the wording to a target-local gate usable once per actual turn, including other creatures' turns. This restores existing source law; it does not choose mixed allocation or activate a producer.

Confidence: HIGH on automatic occurrence and each-turn correction; HIGH on unselected mixed allocation.

### F - Warding Bond: ordinary defenses and linked damage are not direct HP subtraction

The copied amount begins with damage the target takes after its defenses, not the original attack amount and not merely lost current HP. Temporary HP can absorb damage while the target still takes damage. Ordinary recipient defenses apply generally; the spell does not expressly declare their bypass.

Genuine narrow gap is whether the stated equal amount denotes the caster's damage input or an exceptional final equality, and exact copied type/component/cause semantics. A blanket direct-HP-loss interpretation is not an equally source-supported default. Recommendation: preserve the actual target damage components as linked typed input, apply caster's ordinary defenses and temporary-HP buffer, retain the causal link. Target taking5Fire leads to caster taking2 with Fire Resistance before its own temporary-HP allocation. Do not automatically copy every original origin/bypass attribute: Warding Bond is the new proximate cause and source-specific attack/origin exceptions need exact qualification.

Required witness: target takes damage entirely into temporary HP, so current-HP loss0 does not erase the bond cause. Recast/range/caster-zero termination and both actual Concentration obligations remain source-governed. No reciprocal recursive bond is silently permitted.

Confidence: HIGH on general defenses/no explicit bypass; MEDIUM on the complete amount/type/proximate-cause profile. Retain that narrowed interpretation judgment.

## Review findings and repair boundary

| Finding | Disposition |
|---|---|
| SPI-01: Magic Missile shared draw presented as equally ordinary2024 interpretation | Correct brief: independent dart draws source-grounded; shared draw requires explicit departure; remaining decision is exact instance/Concentration policy |
| SPI-02: Resistance elective withholding presented as equally source-grounded | Correct brief: automatic prescribed occurrence is baseline; actual pending choice is mixed allocation |
| SPI-03: lifecycle Resistance per target turn wording | Correct exact owner phrase to once per actual turn, gate target-local; no new product policy |
| SPI-04: Warding copied amount equated with final current-HP loss / wholesale origin copying | Correct amount basis and qualified type/cause/ordinary-defense recommendation |
| SPI-05: Aid duration-bound increase and Speed zero consumers understated | Preserve narrower complete arithmetic/domain decisions, include their zero witnesses and source asymmetry |

Two independent source-and-owner reviewer lanes confirmed the decisive distinctions and the Resistance wording defect. The Architect synthesized the result and owns documentary repairs. No source registry HELD entry is closed by this review; full SP00/SP03/SP04/P2/native/corpus/performance readiness is not claimed.

## Decision-ready proposed package - not selected

A reversible effective Aid bonus with explicit zero/overlap/LifeState cases; B per-dart damage/Concentration grouping with ordinary separate draws and simultaneity; C fixed cast-time membership/current aura eligibility; D final nonnegative Speed; E automatic source occurrence plus chosen-type-only reduction before ordinary defenses; F target-taken typed linked input with caster ordinary defenses and exact proximate cause.

The source-grounded pieces do not require repeated PO permission. The six narrower outcome profiles still require the explicit accepted interpretation gate. Ordinary independent technical/source-evidence/auth-turn work remains authorized; neither a checkpoint nor this review stops those lanes. After acceptance, perform exact candidate/critic/resolution/canonical owner propagation and source evidence synchronization before production claims.

VERSION_IMPACT: NONE for source-framing/control/report and exact source-conformance wording repair. No GAME/code/schema/catalog/package bytes, active profile contract generation, engine identity, migrations or gameplay support are changed. Verification is exact source/owner comparison and documentary integrity/readback; no future tests, latency or release build claim.
