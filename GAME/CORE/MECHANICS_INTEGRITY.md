# Mechanical Resolution Integrity

framework_module_version: 1.0.1
load_policy: ALWAYS_DURING_GAMEPLAY
precedence: authoritative for proving that a mechanical outcome actually exists before narration

## Purpose

D&D mechanics may be hidden from the player, but they may never be skipped.

`mechanics_detail: 0` means **hide mechanical presentation**, not disable, approximate, narratively substitute, or postpone the underlying rules resolution.

This module is a correctness gate between RULES/RANDOMNESS and CONSEQUENCES/NARRATION. If older text permits narration to imply an uncertain mechanical result without actually resolving it, this module wins.

## Resolution gate

Before narrating any material action outcome, classify the outcome internally as exactly one of:

- `AUTOMATIC` — no meaningful uncertainty exists and the rules/fiction permit the result without a roll;
- `IMPOSSIBLE` — established rules/fiction make the intended result unavailable;
- `DETERMINISTIC_RULE` — an exact mechanic resolves the result without randomness;
- `RANDOM_RESOLVED` — uncertainty exists and the required real random test(s) have been completed.

A material outcome has not been resolved merely because a plausible sentence about it can be written.

If none of the four classes can yet be justified, STOP before consequence/narration and resolve the missing mechanics first.

## Requirements for RANDOM_RESOLVED

Before a random result may become fiction, the runtime must have fixed enough information to reproduce the ruling:

- actor and intended effect;
- applicable rule/test/action;
- relevant canonical or newly established mechanical inputs;
- target/DC/opposition/defense when applicable;
- advantage/disadvantage or equivalent modifiers when applicable;
- exact dice/random expression;
- ACTUAL generated random value(s);
- arithmetic/comparison required by the rule;
- resulting mechanical state delta and consequence.

Do not replace any of these with an intuition such as `вероятно попал`, `похоже не успел`, `получился хороший удар` or another prose-level guess.

## Actual RNG is mandatory when the rule needs randomness

Use `RANDOMNESS.md`.

A die result must come from a real available RNG mechanism/tool. Natural-language generation is not RNG.

When several independent rolls are known in advance, they may be generated efficiently in one local RNG/tool operation. When later rolls depend on earlier results, preserve rule order rather than pre-generating outcomes that may never be needed.

Do not browse the web merely to roll dice.

If no trustworthy RNG is available, do not silently substitute narration. Use the explicit fallback in `RANDOMNESS.md`.

## Combat state barrier

When initiative-scale combat is active, keep a mechanical combat working set sufficient for the current resolution. At minimum when relevant:

- participants/sides and turn/order state;
- HP/temp HP;
- AC/defenses and required save/check values;
- conditions, concentration and ongoing effects;
- positions/ranges/zones sufficient for the current rule;
- limited resources/actions/reactions required by the active mechanics.

Missing NPC mechanics that materially affect an outcome must be established BEFORE observing the outcome, using the minimum sufficient rules-consistent state. Do not invent them afterward to justify narration.

An attack that requires an attack roll cannot become `попал`, `промахнулся`, `сломал нос`, `ранил`, etc. until the attack mechanics have actually resolved. Damage that requires dice cannot be assigned without actual damage dice. The same applies to saves, checks and other uncertain combat mechanics according to the active ruleset.

Cinematic wording never bypasses this barrier.

## Hidden mechanics still maintain a resolution trace

Maintain a compact in-memory **resolution trace** for the current unresolved/recent action sequence or encounter.

For each material mechanical step retain enough to answer an immediate audit request, typically:

- resolution class;
- mechanic/test;
- relevant inputs;
- raw RNG result(s), if any;
- arithmetic/comparison;
- resulting state delta.

This trace is operational hot state, not a requirement to persist every die roll to GitHub. It may be compacted/dropped at a safe scene/encounter boundary once durable consequences are represented elsewhere and no audit/recovery need remains.

At low mechanics presentation detail, keep the trace hidden. Do not omit it while the trace is still required by the active resolution/audit scope.

## Explicit audit request overrides display suppression

If the player asks to see the actual rolls/calculations for recent actions, show the existing resolution trace for the requested scope even if `mechanics_detail` is normally low.

Do not fabricate a retrospective table, roll, modifier or HP value merely to satisfy the request.

If the trace is missing/corrupt/unavailable, first determine whether mechanics themselves were genuinely skipped before acceptance or whether an already accepted mechanics/RNG/ID/consequence basis exists elsewhere. Trace loss alone does not decide that question.

## Correction: distinguish mechanically unsupported narration from downstream trace loss

A missing, corrupt or unavailable resolution trace **alone does not prove that accepted mechanics never existed** and does not invalidate an already accepted mechanical consequence.

If accepted mechanics/RNG/stable IDs/consequences can be established from the applicable accepted native basis, preserve them through downstream trace, persistence, publication, presentation, Context, diagnostic or recovery failure:

- do NOT replay or re-resolve the accepted action;
- do NOT reroll or replace accepted RNG;
- do NOT reallocate or replace accepted stable IDs;
- do NOT rewrite accepted consequences merely to repair evidence projection;
- diagnose/recover the missing downstream artifact under its native owner while carrying the accepted basis forward.

Pre-acceptance correction is permitted only when evidence establishes that an uncertain narrated outcome was **genuinely mechanically unsupported** and that **no valid accepted mechanics/RNG consequence ever existed** for that affected action sequence.

Only in that case:

1. stop propagating the mechanically unsupported narrated outcome;
2. identify the last mechanically valid frontier preceding the unsupported sequence;
3. preserve facts/state established independently of the unsupported outcome;
4. do NOT invent retrospective dice, numbers, IDs or accepted results;
5. replay/re-resolve only the genuinely unsupported affected action sequence from that valid frontier using real mechanics and fresh legitimate RNG;
6. repair/persist only canon that was based on genuinely unsupported mechanics.

Narrative continuity is subordinate to honest mechanics, but accepted mechanics are also continuity. Do not keep a mechanically unsupported result merely because correction is inconvenient, and do not destroy an accepted result merely because a later evidence projection degraded.

## Presentation separation

Mechanics visibility affects only what is shown to the player.

At `mechanics_detail: 0`, narration may omit die values, modifiers, HP, AC and formulas, but the runtime still performs the same checks, resource accounting and state transitions it would perform at detail 10.

Do not simplify the actual simulation because the player requested a story-first presentation.

## Latency discipline

Mechanical integrity should normally be local and fast:

- use already-loaded character/entity mechanics;
- cache deterministic derived values while inputs remain unchanged;
- batch independent RNG where safe;
- do not perform GitHub or web reads merely to prove a normal roll that can be resolved locally;
- keep the trace compact rather than producing a verbose ledger every turn.

Fast narration is valuable only after the outcome actually exists.