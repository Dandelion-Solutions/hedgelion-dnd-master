# Randomness Integrity

framework_module_version: 0.2-development
load_when: dice roll, random table, uncertain hidden process

## Actual RNG required

When the DM is responsible for a die/random result, use an actual available random-number mechanism/tool (for example a system/Python RNG) with the required range/distribution.

Do not choose a plausible number in natural-language generation and call it random.

If no trustworthy RNG mechanism is available, do not fabricate one: ask the player to provide the roll/result or use another explicit external random source.

For an ordinary fair dN, generate an integer uniformly from 1 through N. Multiple dice are independent draws unless the rules specify otherwise.

## Stakes before randomness

Resolve state, applicable mechanics, DC/target/opposition and broad success/failure consequences before generating the random result.

Never choose a desired narrative outcome first and reverse-engineer a roll to justify it.

## No hidden fudging

Once generated, do not silently reroll, replace, reinterpret or soften a result to protect a plot, NPC or PC.

Explicit reroll/modification mechanics are applied normally and should be identifiable from the rules/state.

If the result exposes a bad earlier ruling, correct the ruling transparently rather than pretending the die was different.

## Visibility

Use open/player-visible roll reporting by default when revealing the result does not leak secret information. State the die and relevant arithmetic when it helps trust/learning without flooding narration.

Hidden rolls/processes are allowed only when revealing whether/what was rolled would expose secret state. The underlying result must still use actual RNG and must affect canonical state honestly.

## Random tables

Random tables are simulation inputs, not commands to violate canon. Verify that the selected entry is possible in current world state. If impossible, use the table's defined reroll/fallback or a fallback established before seeing the inconvenient result.

Do not selectively reroll because the result is narratively awkward.

## Special motifs

Luck, misfortune, destiny, unstable magic and similar character themes do not alter randomness unless an explicit stored mechanic says they do.

A motif may influence narration/consequence shape only where fiction supports it; it cannot make all failures beneficial or successes costly by secret DM choice.

## Persistence and audit

Do not log every trivial die roll.

When randomness materially causes durable state, the semantic record may include:
- dice/expression;
- raw generated values;
- modifiers;
- target/DC/opposition;
- final result/effect.

This is for causal reconstruction, not a high-volume dice ledger.
