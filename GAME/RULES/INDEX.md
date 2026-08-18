# Rules Routing Index

rules_baseline: D&D 2024 / SRD 5.2.1
research_policy: latency_aware

This small routing file is preloaded with CORE after the exact engine package is resolved.

## Live turn

Normal gameplay is local-first. Route to the relevant CORE module and already-established mechanics; do not automatically open an external source.

- action/check uncertainty -> `CORE/ADJUDICATION.md`
- attack/combat/initiative/conditions -> `CORE/COMBAT.md` + stored exact mechanics
- spells/magic -> `CORE/MAGIC.md` + stored spell/feature mechanics when available
- character creation/level up -> `CORE/CHARACTER.md` / `CORE/ADVANCEMENT.md`
- exploration/travel/environment -> `CORE/EXPLORATION.md`
- equipment/price -> `CORE/REWARDS.md`
- monster/stat block -> stored NPC/creature mechanics, otherwise minimum fair local mechanics before outcome
- rest/downtime -> `CORE/ADVANCEMENT.md`

If an exact numeric/textual RAW value is not locally available during an ordinary turn, do not automatically browse. Use `CORE/PLAY_POLICY.md`: make the minimum fair local ruling consistent with established character/world state.

External RAW lookup during a live turn is allowed when the user explicitly asks for official verification/source/RAW research.

## Setup and preparation

During character creation/level-up, a bounded official-source lookup MAY establish exact durable mechanics once, after which those mechanics should be stored and reused rather than re-researched each turn.

During world/lore prep, `PLAY_POLICY.md` permits bounded trustworthy-source research for enrichment. Rules-source authority and lore-source authority are not the same thing; forums/community material may inspire worldbuilding but do not become exact mechanical authority.