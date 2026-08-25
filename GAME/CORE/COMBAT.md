# Combat Runtime

framework_module_version: 0.1.2
load_when: initiative/combat, tactical threat, attacks, combat consequences

## Enter combat when initiative-scale resolution is useful

Do not force every hostile interaction into combat rounds. If violence is one-sided, trivial, impossible or better handled by another resolution method, adjudicate accordingly.

When multiple actors' timing and tactical choices matter, establish combat state and follow the campaign's D&D rules baseline.

## Mandatory mechanical gate

Combat narration never substitutes for combat resolution.

Before narrating a material combat outcome, satisfy `MECHANICS_INTEGRITY.md` and classify the step as `AUTOMATIC`, `IMPOSSIBLE`, `DETERMINISTIC_RULE`, or `RANDOM_RESOLVED`.

When a rule requires a roll/save/check/damage roll, perform it with actual RNG before stating the outcome. Do not narrate an attack as hitting/missing, assign an injury, remove HP, apply a condition, decide a grapple/control outcome, or determine survival merely because that result feels plausible or dramatic.

At `mechanics_detail: 0`, perform the full mechanics and hide their presentation; never hide them by omitting them.

## Combat state

Track at minimum when relevant:
- participants and sides;
- initiative/order;
- HP and temporary HP;
- AC/required defenses and saves/checks;
- conditions;
- concentration and ongoing effects;
- positions/ranges or zones sufficient for rulings;
- cover/terrain/hazards;
- limited-use resources;
- escape/surrender/objective conditions.

Do not rely on prose memory for mechanical state.

Procedure-local operational state — initiative order, round/turn position, active participant, action and movement budgets, and local procedure time — is owned by the active `runtime.procedure`. `world.encounter` owns durable encounter identity, participants and status and may reference that procedure; it is not a duplicate timing or action-budget owner.

If a needed participant value is undefined, establish the minimum sufficient rules-consistent mechanic BEFORE the first result that depends on it. Once materially used, keep it stable unless a causal game effect changes it.

Maintain the compact current combat resolution trace required by `MECHANICS_INTEGRITY.md` so recent rolls/calculations can be audited without reconstructing them after the fact.

## Intent and legal actions

Players may describe intended actions naturally. Translate them into rules mechanics where possible.

If an intended action is not covered directly, use `ADJUDICATION.md` rather than rejecting creativity merely because no button exists for it.

Do not quietly grant benefits beyond the rules because an action sounds cinematic; likewise do not punish creativity with arbitrary extra checks.

## Enemy behavior

Opponents act according to intelligence, goals, morale, knowledge and current tactical perception.

Not every enemy fights to the death. Retreat, surrender, negotiation, panic, pursuit or objective-focused behavior may be appropriate.

Enemies do not know PC capabilities they have not observed or learned.

## Fair challenge

Do not alter enemy HP, reinforcements, attack bonuses, save DCs or available abilities after seeing player performance merely to manufacture a desired difficulty curve.

Dynamic reinforcements/events are allowed only when they have an established or plausible in-world cause that would have existed regardless of the current dice results.

Telegraph obviously overwhelming threats when characters could reasonably recognize them.

## Tactical clarity

Before a decision whose viability depends on geometry, provide enough information about distances, obstacles, visible threats and relevant effects.

Do not exploit ambiguities in the DM's own description against the player.

## Rules uncertainty

For material combat rules, prefer already-stored/local D&D 2024/SRD 5.2.1 data.

Normal live combat remains local-first under `PLAY_POLICY.md`: if an exact minor RAW detail is unavailable, make the smallest fair temporary ruling needed to continue rather than automatically browsing the web. External source verification is for explicit player requests or a natural preparation boundary.

A temporary ruling does not waive the requirement to actually perform whatever test/randomness that ruling requires.

## Damage and death

Apply damage, healing, conditions, death/dying and resource use consistently with the active ruleset and stored character/creature mechanics.

When damage is random, generate the required damage dice. Do not choose a plausible injury severity in prose and translate it into state afterward.

Do not secretly prevent lethal consequences. Do not target the PC with arbitrary lethal escalation solely because death would be dramatic.

## Audit failure

If the player asks for recent combat calculations and the runtime discovers that required attacks/checks/damage were never actually resolved, do not manufacture retrospective numbers.

Treat the affected sequence as mechanically invalid and follow the repair/replay rule in `MECHANICS_INTEGRITY.md` from the last mechanically valid frontier.

## End of combat

Combat ends when initiative-scale timing is no longer useful, not necessarily when every opponent reaches 0 HP.

Persist according to the campaign's durability profile:
- HP/conditions/resources;
- deaths, captures, escapes and surrender;
- destroyed/changed environment;
- loot/ownership changes;
- witnesses and information spread when relevant;
- elapsed time and consequential relationships.

Do not create a GitHub commit merely because one combat round ended; persistence timing remains governed by `DURABILITY_GUARD.md` / multiplayer rules.