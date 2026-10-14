# Local-spell A–F source interpretations — accepted owner decision

Status: **ACCEPTED PRODUCT OWNER DECISION — IMPLEMENTATION-FACING LAW**
Date: 2026-10-14
Source/review basis: `1f4c28fbe87e7c97ca12b29ced0e6ec46dafa6f8`
Review provenance: `../design/2026-10-14-sp00-source-interpretation-review.md`.

## Authorization and authority

The Product Owner explicitly accepts the complete proposed A–F package and adds:
“Принимаю весь предложенный набор, включая chosen-type-only для Resistance:
уменьшение применяется только к выбранному типу урона, без переноса остатка на
другие типы.” This closes the six interpretation judgments, not production proof.

This is the sole final owner of these six HDM interpretations. The prior review
and Decision Brief retain their historical proposals/findings and route here.
Source-grounded ordinary dice/defense/turn rules remain distinguished from the
accepted interpretations; do not relabel every chosen interpretation as explicit
SRD wording. This decision supplements the accepted execution/lifecycle contracts
without adding a state owner, query language, primitive or general adjudication.

## A. Aid — reversible effective current-HP contribution

Let b_before/b_after be the effective applicable Aid bonus before/after a lawful
application, expiry, suppression/resumption or overlap-winner transition. Same-
spell highest-potency/latest-equal arbitration remains unchanged. Change current
HP by delta = b_after - b_before, then normalize to zero and the current derived
maximum. Use actual current HP, preserving intervening damage/healing; never
restore entry HP. Replacing an equal bonus changes provenance, not current HP.
No independent stacking or repeated healing from unchanged arbitration.

Actor HP remains the sole amount. The bonus/provenance is not temporary HP or a
second mutable health balance. Native health and required bound LifeState changes
share the lawful atomic closure. Ending at zero is not damage and creates no
invented death-save failure; apply the existing zero/LifeState policy. A positive
current increase must reconcile dying/stable state under that policy; no revival
of dead subjects or exemption from target eligibility is granted.

Required witnesses: max20/current12 before Aid, bonus5, damage8 gives current9
before expiry and4 after removal; current2 minus effective5 floors0 without a
damage failure; stronger5->10 adds only5; unchanged/equal winner delta0; lawful
return to an applicable weaker bonus removes only the effective difference.
Also qualify first application at zero/stable/dead, healing, suppression and
winner expiry without restoring snapshots or inventing lifecycle authority.

## B. Magic Missile — per-dart instances in one simultaneous group

Each dart uses its ordinary independent1d4+1 draw. Each damaging dart is a distinct
native damage instance with its own Concentration obligation while the recipient
is still concentrating. All darts of the cast retain the source's simultaneous
group: distinct instances are not sequential fictional attacks.

Draw/request/instance/group identity comes from exact accepted source/occurrence,
not caller list order or new ambient RNG. Retry/recovery reuses fixed results and
accepted identities. Apply actual-turn-controller simultaneous ordering under
existing source/Step3 rules; engine iteration cannot substitute for a lawful
choice. Do not perform unnecessary saves after Concentration actually ends.

Required witnesses: three damaging darts against one still-concentrating target
can require three checks, not one per-target aggregated check; failed earlier
Concentration or health/death ending changes remaining applicability. Reconcile
reduction/rounding, zero-HP/death-save and simultaneous ordering with the same
source-defined instances. Shield/no-damage and invalid-target branches remain
their existing source law. The private fixed-literal route witness proves none
of this production damage/RNG behavior.

## C. Pass without Trace — cast-time membership

Commit the selected creature identities at casting. Preserve that membership
through lawful leave/reentry; benefits apply only while a selected creature is
inside the current aura. A previously unselected later entrant gains no benefit
by arrival alone. No free reassignment, new update action or generic ongoing
caster-to-target range leash is granted. Existing caster benefit, target legality,
moving aura geometry, current occupancy and source duration remain unchanged.

## D. Speed — final nonnegative movement capability

After the complete lawful applicable modifier composition, floor each resulting
derived movement capability at0. Retain raw negative contributions and exact
special-speed propagation/remaining-movement rules. Never floor each contribution
independently or use source order to choose a result.

Exact-zero consumers observe the final nonnegative capability, including Dodge,
voluntary Prone, standing and flying as applicable. Base5 minus10 yields0, not−5.
Test additive modifiers, special speeds and every implicated zero predicate;
schema minima alone do not realize this behavior.

## E. Resistance — automatic chosen-type-only reduction

Use the first eligible positive damaging occurrence of each actual turn,
automatically and without a new Reaction or elective withholding. The gate is
target-local but keyed to the actual turn, including other creatures' turns.
Mere presence of a raw component is not enough to consume it when the relevant
damage is fully prevented; use the exact prospective eligibility/interception
closure rather than physical current-HP loss as a substitute for damage taken.

One fixed d4 reduces only the selected damage-type subtotal: result = max(0,
selected_subtotal - reduction). No excess reduction spills into any other type;
do not roll once per component or grant arbitrary component allocation. Apply
the admitted ordinary type defenses after the reduction. Preserve origin/bypass
qualifications and trace; subtotal aggregation must not erase materially distinct
defense applicability. An unsupported outcome-sensitive decomposition holds that
consumer rather than inferring permission/order or another damage policy.

Required witness:5Fire+5Cold, selectedFire, ordinary Fire Resistance and d4=3
gives floor((5-3)/2)+5=6. Reduction exceeding selected Fire floors that subtotal0
and leaves Cold unchanged. Test fully prevented damage, multiple same-turn
instances, other creatures' turns, mixed components and fixed-result reuse.
Gate consumption and accepted health changes share native causal/atomic closure.

## F. Warding Bond — linked typed input with ordinary caster defenses

Copy the damage the target takes after its defenses, before allocation into its
temporary/current HP. Neither raw attack damage nor physical current-HP loss is
the copied amount. Damage absorbed entirely by temporary HP still supplies the
bond's linked cause.

Prepare target-taken typed components as a new linked input to the caster, apply
the caster's ordinary defenses and then its temporary-HP buffer. Warding Bond is
the new proximate cause: retain the original causal link/type/amount evidence,
but do not blindly copy attack/origin/bypass attributes whose source conditions
do not apply to the new cause. No exceptional final-loss equality or unexpressed
defense bypass is selected.

Target taking5Fire leads to resistant caster taking2 before its own temporary HP.
Target current-HP loss0 through temporary HP does not erase this link. Preserve
explicit recast ending on either connected creature, range/caster-zero termination,
and each participant's actual separate Concentration; the bond is not itself a
Concentration spell. No reciprocal recursive-bond default or post-commit rewrite.

## Traceability, proof and remaining gates

A–F resolve the respective held keys for Aid health normalization, Magic Missile
instance/Concentration grouping, Pass without Trace selection timing, Ray of Frost
movement normalization, Resistance mixed allocation, and Warding Bond copied
damage. Machine source evidence must bind this owner decision and synchronize
its exact dispositions/provenance before declaring those registry keys closed.
Existing17 HELD counts are not silently changed by normative publication alone.

Implementation must retain exact consumer/profile/source bindings, native owner
currentness, zero/free-probe safety, fixed RNG, simultaneous causes and atomic
health/progress/recovery closure. No active schema/catalog/profile/recipe is
registered here. Package/admission/native/end-to-end/latency proof, other source
holds, default/Word of Recall/future-proof lanes and auth/turn bridges remain.
Wish and all previously accepted mechanisms are unchanged.

VERSION_IMPACT: NONE for this accepted DEV-only interpretation and routing
checkpoint: no active machine schema/profile/module/catalog/package or persisted
contract is changed. Actual materialization assesses affected source/policy/module/
profile/package/digest namespaces and synchronizes required projections. Owner
acceptance does not assert package compatibility or full-spell readiness.
