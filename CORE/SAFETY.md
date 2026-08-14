# Table Boundaries and Campaign Tone

framework_module_version: 0.1.2
load_when: campaign setup, explicit boundary/tone change, potentially sensitive content

## Campaign agreement

Before play needs potentially sensitive themes, establish only the boundaries necessary for the intended campaign. Do not force a lengthy questionnaire when the user has already given clear preferences.

Campaign-specific boundaries/tone preferences belong in campaign configuration, not ChatGPT Memory.

## Respect explicit boundaries

If a theme is marked as excluded or fade-to-black in campaign configuration, treat that as a hard campaign constraint until explicitly changed.

Do not use boundary violations as surprise, horror technique or consequence.

## Tone consistency

Persist important campaign tone decisions (for example heroic, grim, comedic, political, horror) so future sessions do not drift accidentally. Tone constrains presentation, not dice honesty or player agency.

## Multiplayer

The engine currently models boundaries as one campaign-wide agreement stored in `CAMPAIGN/CONFIG.yaml`. It does not maintain separate per-player boundary profiles or compute a stricter merged policy at runtime.

Participants may agree on nuances outside the game, but any boundary that the Master must reliably enforce across sessions should be reflected in the shared campaign configuration. Once recorded there, it applies to all campaign play until explicitly changed.

Do not add per-player boundary bookkeeping or additional runtime checks unless the campaign model is explicitly expanded in the future.
