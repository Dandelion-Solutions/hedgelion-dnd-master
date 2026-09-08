# Mechanical Integrity Regression Cases

These cases protect the distinction between hidden mechanics, genuinely skipped pre-acceptance mechanics, and downstream loss/degradation of evidence for mechanics that were already accepted.

## M01 — mechanics_detail 0 hides output, not rules
Player preference is `mechanics_detail: 0`.
Player attacks in an uncertain combat situation.
Pass: Master resolves the same applicable attack/save/damage mechanics and real RNG as at higher detail, but narrates primarily fiction. No rule/roll is skipped because numbers are hidden.

## M02 — uncertain outcome needs a resolution class
Player attempts a material uncertain action.
Pass: before narration the runtime internally classifies the result as `RANDOM_RESOLVED` and possesses test inputs, real RNG output and state delta. A plausible prose outcome without those is failure.

## M03 — automatic action does not invent a roll
Outcome is truly automatic under established rules/fiction.
Pass: classify `AUTOMATIC`, resolve directly, no meaningless RNG merely to satisfy the gate.

## M04 — impossible action does not invent a roll
Outcome is impossible under established capability/world constraints.
Pass: classify `IMPOSSIBLE`, explain through play; no fake low roll.

## M05 — attack requires real attack resolution
NPC or PC makes an attack that uses an attack roll under the active rules.
Pass: establish attack modifier/target defense and actual d20 result before hit/miss narration. On hit, roll required damage before changing HP/injury state.

## M06 — enemy mechanics exist before result
An NPC/creature's AC, HP, save or attack value is required but was not previously stored.
Pass: establish minimum sufficient rules-consistent mechanics before observing the outcome; never choose values after seeing PC performance or desired narration.

## M07 — combat ledger exists even when invisible
Low-detail combat is ongoing.
Pass: hot working set still tracks participants/order, HP/defenses, conditions/resources and the current resolution trace. Prose memory alone is failure.

## M08 — explicit audit reveals real trace
After several hidden-mechanics actions, player says `покажи честные расчёты за последние ходы`.
Pass: show existing non-secret raw rolls/modifiers/comparisons/state deltas for the requested recent scope. Do not answer that no table exists if those actions were validly resolved.

## M09 — genuine skipped mechanics permit pre-acceptance correction
Player requests audit and evidence establishes that previous uncertain narration was produced without actual mechanics, no valid accepted mechanics/RNG consequence ever existed, and no downstream evidence merely went missing.
Pass: admit mechanics were skipped; do not manufacture old dice or values. Mark only the genuinely unsupported affected sequence invalid and replay/re-resolve from the last mechanically valid frontier using real mechanics and fresh legitimate RNG.

## M10 — cinematic phrase does not grant success
Player says an evocative action such as `разбегаюсь и выбиваю ему два зуба`.
Pass: interpret intended attack/effect, apply the appropriate mechanic, and let the result determine whether/how the fiction occurs. Do not convert declared color into automatic success.

## M11 — NPC attacks are mechanically equal
Enemy swings an axe at the PC.
Pass: enemy action uses the same honest resolution discipline as a PC attack; no automatic enemy hit or narratively chosen wound.

## M12 — control/grapple/disarm follows active rules
Player tries to seize a weapon, grapple, shove or otherwise control an opponent.
Pass: use the applicable active D&D rule/local ruling and execute its actual test/save if required. Do not assume a generic contested check or automatic success merely from prose.

## M13 — actual RNG, not language-model randomness
A d20/damage/random result is required.
Pass: use an actual available RNG mechanism/tool. A number selected in prose is failure.

## M14 — batch independent RNG safely
Several independent dice are already known to be required.
Pass: they may be generated in one local RNG operation for latency, while preserving independence and mapping each result to its mechanic. Conditional later dice are not pre-generated before needed.

## M15 — hidden secret roll remains honest
A roll must remain hidden because revealing it leaks secret state.
Pass: use actual RNG and trace internally; suppress only disclosure, not resolution.

## M16 — correction repairs only canon based on genuinely unsupported mechanics
Several narrated combat beats are proven never to have had valid accepted mechanics/RNG consequences.
Pass: stop propagating those unsupported beats, return to the last mechanically valid frontier, retain independently established facts, and replay only the unsupported actions honestly. If unsupported consequences were persisted, explicitly repair only canon derived from those unsupported mechanics.

## M17 — mechanics gate adds no network ritual
Normal action has all state/rules locally loaded and uses local RNG.
Pass: no GitHub read or web lookup merely to satisfy mechanical integrity.

## M18 — persistence stays separate from resolution
A combat roll changes SOFT singleplayer state but no durability boundary fires.
Pass: mechanics resolve honestly now; GitHub save may remain deferred under DURABILITY_GUARD. Hidden mechanics and sparse persistence are independent concerns.

## M19 — missing downstream trace does not erase accepted mechanics
An accepted mechanics/RNG consequence already exists, but its resolution trace is later missing, corrupt or unavailable.
Pass: missing/corrupt/unavailable downstream trace alone does not invalidate the accepted result. Preserve accepted mechanics, RNG, stable IDs and consequences; recover/diagnose the trace projection under its native owner. NO replay / reroll / reallocation.

## M20 — downstream persistence/presentation/recovery failure cannot rerun accepted action
Accepted mechanics/RNG/IDs exist, then persistence, publication, presentation, Context, diagnostics or recovery fails.
Pass: preserve the accepted causal basis and handle the downstream failure separately. NO replay / reroll / reallocation of accepted work merely to regenerate a trace or presentation artifact.
