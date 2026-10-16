# Spike Growth — distance remainder and damage-instance Decision Brief

Status: **PROPOSED — TWO BOUNDED PO CHOICES; NO POLICY SELECTED**
Date: 2026-10-16
Source basis: `be6ac3305e258fcaea910f29a95e22d3bfb802cc`; later S3 code changes
do not alter the cited SRD or accepted spatial/health semantics.
Independent source/owner reviewer: `ses_ebdd5598cffeK9YpSEOvZ26vyH`.
Human decision required: **YES**. Recommendation confidence: **MEDIUM**.

## Recommendation

1. Retain partial qualifying distance **per creature + exact spell-root
   application until that application ends**, including genuine exit/reentry.
2. Resolve **one separate 2d4 Piercing damage instance at each completed five-foot
   threshold**, with its own applicable defenses/health/Concentration consequences.

These interpretations change gameplay outcomes and are not selected by generic
rounding, a movement budget, existing chunking, or another spell's damage policy.
Approval would allow their exact formalization; native state/producer/recipe proof
and the appropriate implementation/version gates remain separate.

## Source-grounded boundary — unchanged under either choice

SRD `DEV/docs/SRD_CC_v5.2.1.md:15009–15023` transforms ground within a20-foot-radius
Sphere, creates Difficult Terrain and deals2d4 Piercing per5feet actually traveled
into/within qualifying area. Preserve Concentration/up-to10minutes and its existing
unseen-at-casting Search/recognition rules.

- Movement **cost is not distance**.5feet through Difficult Terrain remains5feet,
  although its cost is10feet. No voluntary-only restriction or once-per-turn cap.
- Teleportation traverses no intervening space; arrival invents neither5feet nor
  flat entry damage. Carry/drag/fall eligibility depends on the actual accepted
  path and affected ground, not category labels or the carrier's path alone.
- A Sphere does not turn its entire air volume into spiked ground. Missing scene
  facts use existing exact spatial-input contracts, not invented thorn height.
- Five internal1-foot chunks must have the same consequences as one established
  5-foot traversal. Caller/command/transaction boundaries, retry, save/load and
  index rebuild cannot create reset or aggregation rules.
- With the same accepted rules/policy, source applicability, prior progress and
  native state, equivalent established traversal must have identical consequences
  regardless of technical partition. Fictional fact establishment cannot choose
  between unresolved mechanical interpretations.

## Choice 1 — lifetime of a partial five-foot remainder

| Option |3feet, genuine exit, later2feet under the same application|
|---|---|
| **Application lifetime — recommended** | Completes one5-foot threshold. |
| Continuous qualifying occupancy | Exit discards3feet; later episode has2feet and no damage yet. |

Application lifetime avoids an unsourced exit reset and repeated short-entry
avoidance. Its weakness is retaining small exposure across separated visits;
occupancy-local accumulation is a credible passage-based interpretation, but
adds that genuine-exit reset. Neither option resets on technical subdivisions,
new invocations, action/turn boundaries or recovery.

**Proposed qualification included with application lifetime:** retain already
accrued remainder while that exact application is suppressed or loses same-spell
overlap arbitration; accrue nothing for it while inapplicable. If it resumes,
continue its own remainder and remaining duration, without retroactive credit.
Terminate future accumulation eligibility on actual expiry/dispel/support-ending
of that application; retain protected retry/recovery evidence until lawful discharge.
Do not pool or
transfer progress between creatures, casts/applications or changing overlap
winners. Existing suppression law preserves identity/deadline; this proposed
distance-progress consequence is part of the choice, not claimed already RAW.

## Choice 2 — damage-instance boundary

| Option | Ten qualifying feet |
|---|---|
| **Each completed5feet — recommended** | Two separate2d4 Piercing instances at successive crossings. |
| Semantic traversal aggregate | One combined instance, e.g.4d4, with a separately defined gameplay traversal boundary. |

For raw threshold results3and3:
- Piercing Resistance: separate instances give1+1=2; aggregate gives3.
- Resistance then Vulnerability: separate gives4; aggregate gives6.
- Still-concentrating recipient with sufficient HP: twoDC10 checks versus one.
  No further check after Concentration actually ends.
- Supported character policy, initially active/current2/max4, no temporary HP,
  damage modifiers, Resistance, Vulnerability, Immunity or intervening healing,
  and two raw2d4 results of3:
  with a lawful continued forced traversal after unconsciousness and the zone
  still applicable/its caster still concentrating, separate3then3 reaches dying,
  then adds a damage-at-zero failure. Aggregate6 has4remaining after zero and
  causes immediate death. Voluntary movement cannot be assumed to continue after
  the first unconsciousness; actual source/support/health rules still govern.

Per-threshold resolution follows the repeated source unit and permits earlier
health/support consequences to affect later travel. Aggregation reduces repeated
checks/work but needs a semantic traversal boundary and interruption/health
timing rules. Processing convenience cannot supply that boundary. Magic Missile
or Warding Bond grouping is not authority for this different spell.

## Acceptance scope and remaining proof

Requested reply: **1 application lifetime / occupancy; 2 per5feet / semantic
aggregate**. Recommended **application lifetime (with the qualification above)
+ per5feet**. Neither choice selects a new world-state owner or progress schema.

Preserve fixed threshold/cause/draw identities, no reroll/duplicate on recovery,
and native health/progress/source-currentness/atomic closure. Fractions are
distance progress, not proportional damage. No native implementation, consumer
admission, package qualification, broader source readiness or latency is proved.
Key75's SOURCE hold remains until a complete accepted interpretation is
synchronized into its owner and source evidence. Its FUTURE_PROOF remains
NOT_ESTABLISHED until actual native producer/consumer and composed recovery proof
pass. No other source hold is discharged by this proposal. The aggregate option
requires an exact gameplay traversal boundary and interruption/intermediate-health
timing before source closure; occupancy-local accumulation similarly needs its
own inapplicability/reset qualification. A bare direction cannot authorize code
to invent these outcomes.

## Evidence route

Primary SRD: movement/Difficult Terrain1191–1209,16493–16509; conditional grid
1165–1177; grapple/carry16629–16649; falling16593–16609; teleport17321–17325;
Round Down574–576; damage/defenses1396–1456; Concentration16296–16304;
same-spell arbitration9255–9257; Sphere17191–17195.

Accepted owners: `DEV/ARCHITECTURE/DOMAIN_RULES_COVERAGE.md` distinguishes budget,
location and applicability; `HEALTH_EFFECTS_RECOVERY.md` owns actual health and
LifeState; local-spell execution/lifecycle annexes own exact instance grouping,
source-bound ground/spatial facts, participation and native transitions; Step3
and Step5 own fixed causal/retry/recovery and chunk-equivalence invariants.
Current movement budget/relocation schemas do not supply qualifying distance or
its remainder semantics. Occupancy/cost must not impersonate that source input.

Original key `source.spell.spike_growth.unresolved.displacement_and_distance_policy`,
classification/history index75, current map127, source-pass row129, body witness291;
retained `SIXTH-08` source span15009–15023 SHA256
`c5fb06ec056006712ee2c9a8a995391eb7e3e35134d4ad077339f447a6025dd1`.
The complete source review read these primary bodies/owners; no fresh PDF,
runtime/deployed/hosted-CI proof is claimed. VERSION_IMPACT:NONE for this proposal;
future accepted policy/evidence/materialization assesses actual namespaces.
