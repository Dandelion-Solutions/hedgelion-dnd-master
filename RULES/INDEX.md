# Rules Routing Index

rules_baseline: D&D 2024 / SRD 5.2.1
research_policy: explicit_only

This small routing file is preloaded with CORE after the exact engine package is resolved.

Normal gameplay is local-first and offline-first. Route to the relevant CORE module and already-established mechanics; do not automatically open an external source.

- action/check uncertainty -> `CORE/ADJUDICATION.md`
- attack/combat/initiative/conditions -> `CORE/COMBAT.md` + stored exact mechanics
- spells/magic -> `CORE/MAGIC.md` + stored spell/feature mechanics when available
- character creation/level up -> `CORE/CHARACTER.md` / `CORE/ADVANCEMENT.md`
- exploration/travel/environment -> `CORE/EXPLORATION.md`
- equipment/price -> `CORE/REWARDS.md`
- monster/stat block -> stored NPC/creature mechanics, otherwise minimum fair local mechanics before outcome
- rest/downtime -> `CORE/ADVANCEMENT.md`

If an exact numeric or textual RAW value is not locally available during an ordinary turn, do not automatically browse. Use `CORE/PLAY_POLICY.md`: make the minimum fair local ruling consistent with established character/world state.

External SRD/D&D-source lookup is allowed only when the user explicitly asks for official verification/source/RAW research or during a separately authorized framework research task.