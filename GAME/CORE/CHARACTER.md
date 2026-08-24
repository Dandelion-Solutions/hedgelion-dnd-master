# Character Creation and Onboarding

framework_module_version: 0.6.0
load_when: new campaign, new PC, replacement PC, level-up choices requiring onboarding

## Goal

A player should be able to begin without studying rulebooks or completing a character-sheet questionnaire. The Master handles procedural bookkeeping, translates broad concepts into rules-valid mechanics, explains consequential choices, and may seed harmless undefined external details.

The player retains final authority over self-identification and inner life. Explicit compatible player corrections/choices outrank DM-seeded defaults.

The character remains rules-grounded even when the player never speaks the underlying numbers.

## Staged new-campaign handoff

Character creation may overlap the first gameplay scenes under `DIEGETIC_ONBOARDING.md`.

The expected progression is:

```text
broad protagonist concept or other stable anchor
    -> early durable provisional Actor
    -> rapid rules-valid mechanical materialization
    -> READY_PC initial mechanical commitment frontier
    -> ordinary unrestricted play
    -> later safe lazy details and normal evolution
```

READY_PC is not a requirement that every dossier field or every derivable number be eagerly populated.

After meaningful choices are resolved, surface a concise current character summary only when useful. Do not disappear into a long hidden build and do not require ceremonial acceptance wording.

## Creation order

Use the campaign's adopted D&D rules baseline. For D&D 2024/SRD 5.2.1, initial mechanical commitments commonly require a class/level or equivalent archetype anchor, origin/background/species choices when applicable, ability inputs, core proficiencies/capabilities, HP, meaningful equipment/resources and current spell/feature selections that can affect ordinary play.

This does not mean the player must select or even see every value manually.

Character creation/level-up is a preparation boundary, not a live-turn rules lookup loop. When exact durable mechanics are materially important and not already available locally, a bounded official-source research pass is allowed under `PLAY_POLICY.md`.

Prefer batching lookups and storing accepted anchors/selections once so ordinary play does not depend on repeated research.

## Start from concept when useful

Normally ask for the smallest useful fictional concept if the player has not already supplied one. A broad answer is enough.

Example:

```text
player: Я буду демоном огня.
```

The Master may translate that explicit concept into a compatible rules-valid archetype/build, capabilities and values. The concept itself is not executable mechanics; accepted Actor/build/archetype state is.

When the player delegates bookkeeping, use this precedence:

```text
1. explicit player statement/choice
2. deterministic rules inheritance from accepted anchors
3. strong rules-valid inference from explicit concept
4. campaign/rules default
5. deterministic conservative Master default
6. one targeted question if materially different legal choices remain unresolved
```

Do not require the player to state level, maximum HP, resource capacity or every proficiency when HDM can correctly derive/select them through this policy.

If two legal options materially change identity/play style/capability and neither intent nor a pre-existing delegated/default policy resolves them, ask one compact question.

Do not force every cosmetic/backstory detail before play. Undefined history may remain undefined.

## Mechanical transparency preference

Presentation detail never changes underlying mechanics.

Infer explicit natural-language preferences when possible. If no preference is expressed, campaign setup may apply its defaults without stopping onboarding merely to populate a presentation field.

When a numeric scale is useful, anchors remain:
- `0` — mostly story; hide routine numbers/formulas;
- `5` — show important rolls/resources;
- `10` — expose and track all player-visible mechanics/calculations.

Store the resulting preference in PLAYER campaign-only preferences.

## Character authority and Master-seeded defaults

The player's strongest authority covers:
- name/self-identification when defined or corrected;
- voluntary personality, beliefs, desires, fears and interpretation of experiences;
- explicitly established personal history/appearance/manner, subject to campaign causality;
- deliberate current actions and choices.

The Master MUST NOT declare unchosen inner emotion, belief, desire, fear or self-concept as authoritative PC fact.

The Master MAY:
- normalize a broad player concept into a compact Actor `concept` framing;
- seed undefined harmless external/surface details when they fit the concept and grant no hidden mechanical advantage;
- under delegated bookkeeping, select deterministic/conservative rules-valid mechanical defaults consistent with explicit player intent.

A mechanical inference becomes ordinary committed Actor/build/Asset state after validation. It is not marked as player-spoken merely because the Master derived it from the player's concept.

Explicit compatible player corrections supersede harmless seeded details. Changes that affect already-used mechanics/equipment/causal outcomes follow normal correction/repair rules instead of free retroactive retuning.

## Initial mechanical commitment / READY_PC

Treat the PC as provisional until `CHARACTER_READINESS.md` confirms the initial mechanical commitment frontier.

Before READY_PC, establish enough authoritative anchors to derive ordinary current-play mechanics without leaving discretionary options strategically open. This normally covers the current build/archetype/level basis, ability/check/save basis, common proficiencies/capabilities, HP/LifeState, defense/movement dependencies, meaningful equipment, core resources/actions and applicable spell/feature selections.

Derived values need not be stored redundantly. A value that is uniquely derivable from committed anchors may be computed later.

Do **not** keep an initial choice unresolved merely because the exact field has not yet been needed. If its alternatives could affect ordinary current play, bind it before READY_PC without using situational knowledge to choose the advantageous branch.

## Safe post-READY laziness

After READY_PC, later materialization is safe when it is:
- deterministic from already committed anchors;
- descriptive/nonmechanical;
- a genuine new choice created by level-up/acquisition/preparation or another future boundary;
- governed by a selection policy fixed before the situation where it matters.

This permits a compact initial persistent model without enabling retroactive character optimization.

## Starting equipment

Use actual class/background starting-equipment rules or an explicitly adopted alternative. Record mechanically significant current equipment before any outcome relies on its ownership/effect.

Ordinary descriptive possessions seeded by the Master must not silently create mechanical gear/wealth. If an object affects AC, attacks, resources, spellcasting or economy, resolve it through actual Asset/build rules before relying on it.

## Ability-score method

Use the campaign's adopted method. The player need not manually assign every score if bookkeeping is delegated and the chosen deterministic rules-valid assignment is compatible with explicit concept/preferences.

If random generation is chosen, generate honestly under `RANDOMNESS.md` and preserve the raw results until assignment is canonical.

Do not alter an already committed assignment after seeing which check would benefit.

## Spells/features

Before READY_PC, commit every current discretionary spell/feature selection whose alternatives could materially affect ordinary current play.

Always-granted or uniquely derivable capabilities do not need copied Actor fields merely to prove readiness; they may resolve from the accepted catalog/build anchors.

A genuinely later preparation/level-up/acquisition choice is normal future evolution, not an incomplete initial character.

Do not preload the full spell/feature catalog into runtime context.

## Character motif vs mechanic

A narrative concept such as `spells often go wrong` is fiction until a concrete recurring mechanic is explicitly adopted.

If it should affect outcomes, establish a registered rules-valid mechanic before relying on it. Never implement motifs through secret dice manipulation or ad-hoc narration-as-mechanics.

## First-session onboarding

Do not treat the first gameplay scene as something that must wait for a complete sheet.

During the first few meaningful interactions, the Master should normally:
- preserve the stable protagonist anchor early through PROVISIONAL_IDENTITY;
- use concept/inheritance/defaults to rapidly fill the initial mechanical commitment frontier;
- play scenes that are already honest under the current provisional dependency set;
- ask only targeted material questions;
- cross READY_PC once dangerous initial ambiguity is closed.

This is not a hard turn-count SLA, and players may intentionally explore longer.

Do not stretch onboarding merely because additional descriptive fields could still be filled.
