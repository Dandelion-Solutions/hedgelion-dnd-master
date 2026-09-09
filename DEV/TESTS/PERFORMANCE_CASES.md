# Runtime Reasoning Performance Regression Cases

These cases verify that ordinary gameplay stays responsive without reducing correctness, fairness, agency, NPC nuance or narrative variety.

## P01 — Ordinary attack stays local
A PC attacks a nearby creature. Attack modifier, target defense, applicable conditions and damage mechanics are already loaded.
Pass: resolve from the current working set in one bounded adjudication pass; do not inspect unrelated abilities, future tactical branches, Git history or unused rules.

## P02 — Performance budget is not a reasoning ceiling
A turn involves several interacting effects whose ordering materially changes the legal outcome.
Pass: deepen reasoning until the interaction is resolved correctly. Do not choose the simpler interpretation merely because it is faster.

## P03 — Nuanced NPC is not flattened
A loaded NPC has conflicting incentives, a specific relationship with the PC and limited knowledge relevant to the conversation.
Pass: use those active factors to produce a situation-specific response. The performance budget does not reduce the NPC to a generic cooperative/hostile template.

## P04 — No speculative player tree
The player has declared one concrete action but many plausible follow-up choices exist.
Pass: resolve the declared action and resulting current state. Do not analyze or prepare a decision tree for unchosen future actions unless a current world process actually requires it.

## P05 — Derived mechanics cache
A PC makes several checks while abilities, proficiencies, equipment, conditions and rules affecting the modifiers remain unchanged.
Pass: reuse valid derived modifiers from the working set rather than reconstructing them every time. After a relevant condition/equipment/effect change, invalidate and recompute the affected values.

## P06 — Probability only when useful
An ordinary check uses a known modifier and DC; the player did not request odds and no decision-support comparison requires them.
Pass: resolve the mechanic without calculating/displaying an unnecessary probability distribution. If exact odds are materially requested/needed, calculate them exactly rather than using Monte Carlo sampling when the discrete rule permits exact arithmetic.

## P07 — High-impact gates still run
A surprising consequential result is about to become canon.
Pass: run the applicable truth/agency/causality/knowledge/symmetry/commitment/randomness/convenience checks even though the ordinary-turn budget favors a short pass. If a gate exposes a real issue, resolve it before narration.

## P08 — Ambiguous intent escalates only when material
A player's wording has two plausible interpretations, but they lead to the same material mechanic and consequence.
Pass: choose the natural interpretation without exhaustive clarification. If the interpretations would create materially different risks, resource use or commitments, resolve the ambiguity before adjudication.

## P09 — Creative narration remains varied
Two ordinary scenes have equally simple mechanics but different locations, NPCs, pressures and recent events.
Pass: reasoning remains bounded while narration and NPC behavior reflect the distinct fictional state; do not standardize prose or consequences merely for speed.

## P10 — Settled ruling terminates deliberation
All material state, rules, randomness and consequences for a turn are resolved and correctness gates pass.
Pass: proceed to persistence/narration. Do not continue rechecking the same ruling, searching for a better dramatic outcome, or exploring irrelevant counterfactuals.

## P11 — Mutable artifact preferred sizing target
Current owner: `DEV/docs/superpowers/specs/2026-09-09-runtime-mutable-github-artifact-sizing-bands-owner-decision.md`.
A growth-bearing mutable GitHub-backed text artifact remains at or below the approximate 10–12 KiB preferred steady-state band after the pending write.
Pass: measure exact serialized UTF-8 bytes and keep the owner-valid representation; do not add padding or split solely to approach a target number.

## P12 — Review band is not automatic rejection
A growth-bearing mutable artifact projects into the normal 13–16 KiB review zone.
Pass: perform the owning representation's bounded size/shape review. Continuing with the same file is legal when owner semantics, currentness and expected growth remain safe; the review band is not a universal validity failure.

## P13 — Above-target growth expects owner-valid partition or rollover review
A growth-bearing mutable artifact projects above approximately 16 KiB.
Pass: default to review/partition/rollover under the artifact's owning contract before indefinite further growth. Preserve exact UTF-8 measurement, required material, identity, provenance, atomicity and currentness; never truncate or invent a semantically false split to satisfy a size target. Read-only engine/reference artifacts and DEV prose are outside this mutable-growth rule unless their own owner says otherwise.
