# Rewards, Economy and Treasure

framework_module_version: 0.1.1
load_when: payment, loot, prices, treasure, favors, reputation, property, economic consequences

## Rewards follow world logic

Compensation depends on patron resources, perceived difficulty/risk, scarcity, local economy, urgency and bargaining position. Do not set reward values primarily to signal which quest the DM wants chosen.

## Consistency

When prices/pay scales become relevant, establish a local economic baseline and keep it approximately coherent. Retrieve official D&D equipment/service prices where the rules define them; use explicit campaign/world assumptions elsewhere.

## Multiple reward forms

Rewards may include money, items, information, access, favors, status, property, safe passage, training, alliances or removal of a threat. Do not convert every benefit into gold.

## Treasure

Use official treasure/magic-item guidance when exact mechanical balance or rarity matters. Significant magic items use stable `world.asset` records bound to reusable `definition.asset` mechanics. Per-PC identification or belief is subjective knowledge recorded through `world.knowledge`; it is not an objective asset property.

## No reward inflation

Do not escalate payment/loot every time the player ignores a hook. A small task may matter because of relationships or information; an enormous reward needs an enormous in-world reason.

## Ownership

Unique/significant item transfer, theft, destruction and loss are persistent world changes. In multiplayer they are race-sensitive shared changes and should be published promptly.
