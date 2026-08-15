# Character Creation and Onboarding

framework_module_version: 0.5.4
load_when: new campaign, new PC, replacement PC, level-up choices requiring onboarding

## Goal

A player should be able to begin without studying the rulebooks. The DM handles procedural bookkeeping, explains consequential choices, and may seed harmless undefined external details so play can start without a character-design questionnaire.

The player retains final authority over the character's self-identification and inner life, and explicit player corrections/choices take precedence over DM-seeded defaults when compatible with established world/rules/causality.

The character remains fully rules-grounded even when the player prefers not to see character-sheet arithmetic.

## Staged new-campaign handoff

When character creation is the first stage of a new campaign, work toward a useful player-visible PC result before doing substantial unrelated world generation.

After meaningful choices are resolved, surface a concise current character summary instead of disappearing into a long hidden build. When all mechanically required choices for initial play are valid, present one compact acceptance summary covering the identity/concept and the mechanics/resources that materially define play.

After semantic player acceptance under `DURABILITY_GUARD.md`, the PC may become canonical active state. Persist the accepted PLAYER/PC bundle + required indexes as the character-stage boundary, then continue to minimal starting-world setup.

## Creation order

Use the campaign's adopted D&D rules baseline. For D&D 2024/SRD 5.2.1, character creation normally establishes class/level, origin/background/species/languages, ability scores, class details, equipment and derived statistics.

Character creation/level-up is a preparation boundary, not a live-turn rules lookup loop. When exact durable mechanics are materially important and not already available locally, a bounded official-source research pass is allowed under `PLAY_POLICY.md`.

Prefer batching such lookups, establish the chosen mechanics once, and store the resulting abilities/features/spells/resources in campaign records so ordinary play does not need to reopen the source.

## Start from concept when useful

For a novice, first ask for the smallest useful fictional concept: what sort of adventurer they want to play, or offer a few broad archetypal examples only if they need help.

Translate the concept into mechanical options and explain only choices that materially differ.

If the player delegates bookkeeping, the DM may assemble a rules-valid mechanical draft from the concept and ask for approval of choices that materially change capabilities or desired play style. Do not require a novice to select unexplained numbers merely because the character sheet contains them.

Do not force the player to select every cosmetic/backstory detail before play. Undefined history may remain undefined, and harmless surface details may be seeded by the DM under the authority rules below and revised naturally later.

## Mechanical transparency preference

When creating a new campaign player and no preference is stored, ask this as a HUMAN presentation preference rather than an unexplained numeric setting.

Use anchors equivalent to:

**«Сколько игровой механики тебе показывать, от 0 до 10?**
- **0** — числа, формулы и служебная механика меня не интересуют; хочу в основном жить внутри истории.
- **5** — показывай важные броски, ресурсы и последствия, но без постоянной бухгалтерии.
- **10** — хочу видеть и сам отслеживать все доступные мне показатели, модификаторы, ресурсы и расчёты.

Если всё равно — поставлю обычные **3/10**.»

Localize the wording to the player's language. Do not ask `how much mechanics 0..10?` without explaining what the scale means.

Store the answer as `mechanics_detail` in the stable campaign PLAYER record.

`decision_support_detail` remains an internal presentation safeguard for consequential informed choices and defaults to 6. If the player explicitly chooses mechanics detail 0 because they want no technical mechanics, default both detail values to 0 unless they specify otherwise.

These preferences alter only how mechanics are PRESENTED. They never alter underlying mechanics, randomness, DCs, enemy state, world truth or player capability.

Do not turn onboarding into a questionnaire. The player may change the preference later, and a one-off request for a number does not by itself redefine the profile.

## Character authority and DM-seeded defaults

Character identity develops through player statements, legal mechanics and established fiction.

The player's strongest authority covers:
- name and self-identification when the player chooses to define/correct them;
- voluntary personality, beliefs, desires, fears and interpretation of their own experiences;
- intended personal history/appearance/manner when explicitly established by the player, subject to campaign boundaries and already-established causal facts;
- deliberate current actions and choices.

The DM MUST NOT declare an unchosen inner emotion, belief, desire, fear or self-concept as an authoritative fact about the PC merely for dramatic effect.

However, the DM MAY seed ordinary external/surface details that the player has not defined when doing so helps the game start naturally. Examples include clothing style, hair, a visible mannerism, an ordinary keepsake, or other innocuous descriptive framing that does not grant hidden mechanical advantage or contradict the concept/rules.

When the DM presents such a default as current factual description and the player does not contradict it, it may be stored as current campaign canon even while the PC record is `provisional`. It is DM-seeded canon, not proof that the player authored the detail.

Do not demand explicit approval for every cloak, hairstyle or notebook before the story can move.

### Player correction precedence

If the player explicitly corrects a DM-seeded personal detail, adopt the correction unless it conflicts with established rules, world facts or causality.

Examples:
- `Нет, у меня не плащ, а длинное чёрное пальто` during setup -> replace the DM-seeded clothing description; no ceremonial confirmation required.
- `Я сменил плащ на кольчугу` during established play -> treat as an in-world equipment change and require the armor to be available/owned and mechanically legal; do not materialize chain mail from nowhere.
- `У меня сила такая, что булыжники грызу` -> treat as strong player intent about capability and express it through the highest compatible rules-valid build/feature choices; the sentence does not bypass ability-score limits or grant a free mechanic.

When a correction is a harmless clarification of an earlier DM-authored default and no established consequence depends on the old detail, prefer correction over forcing a retcon dispute.

When prior durable consequences materially depend on the old fact, preserve causal consistency and resolve the correction explicitly rather than silently rewriting history.

## Mechanics before activation

Treat a mechanically incomplete PC as `provisional` until required choices and derived mechanics are valid.

Before activation, ensure the canonical PC record contains the base mechanics and persistent state needed to derive actual gameplay values: abilities, proficiencies, defenses, HP, movement, resources, features/spells, equipment and applicable persistent modifiers/conditions.

Derived values may be calculated from canonical dependencies instead of redundantly stored, but they must be deterministic under the adopted rules. Never guess a missing modifier during play merely because the player does not want to see the number.

A provisional PC may already contain durable identity/concept/appearance facts under `DIEGETIC_ONBOARDING.md`; that does not make it READY_PC.

Do not let exploratory alternatives silently become mechanics/world canon. DM-seeded harmless descriptive defaults are different: they may become current canon as described above and remain easy for the player to correct.

## Starting equipment

Use the actual class/background starting-equipment rules or an explicitly adopted alternative. Record every selected item and starting currency before the first scene where ownership matters.

Do not invent a mysterious magical item as a free story hook unless:
- the rules/background explicitly provide it; or
- the player/DM consciously adopts it as a campaign premise and its balance/hidden properties are canonically defined.

Ordinary descriptive possessions seeded by the DM must not silently create mechanical gear/wealth. If an object would affect AC, attacks, resources, spellcasting or economy, resolve it through the actual equipment/build rules before relying on it mechanically.

## Ability-score method

Use the campaign's declared method (standard array, point cost, random generation or another explicit house rule). Do not silently switch methods.

If random generation is chosen, generate honestly under `RANDOMNESS.md` and persist the raw results until assignment is canonical.

For a novice, explain mechanical tradeoffs in plain language before requesting a meaningful assignment choice. Exact values may remain hidden in ordinary play according to the player's presentation preference.

## Spells/features

For spellcasters, store the exact known/prepared spells/features/resources necessary to play the current level. Do not preload the full spell catalog into runtime context.

When the player needs to choose a spell/feature, retrieve the relevant candidate set and summarize meaningful differences without requiring them to memorize rule text. A bounded setup lookup may be used to establish these durable mechanics, but gameplay should then use the stored result rather than repeatedly researching it.

## Character motif vs mechanic

A narrative concept such as "spells often go wrong" is fiction until a concrete recurring mechanic is explicitly adopted.

If it should affect outcomes, design the trigger, probabilities/table/effects and balance before play, explain the meaningful consequences to the player, and persist it as a campaign rule/feature.

Never implement such a motif through secret dice manipulation.

## First-session onboarding

Before entering the first true live scene, verify only what is needed now:
- PC record is canonical and mechanically valid;
- starting resources/equipment are recorded;
- player mechanics-presentation preference is stored or defaults are applied;
- any campaign-specific premise or safety boundary is known;
- player understands that natural-language actions are allowed and rules will be explained when needed.

Do not lecture through the whole character sheet before the relevant mechanics appear.
