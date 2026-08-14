# Causal Chronology Regression Cases

These cases verify causal consistency without imposing unnecessary timestamp simulation or a mandatory global clock.

## C01 — Cause precedes effect
An artifact causes a magical disaster.
Pass: the disaster cannot be chronologically established before the artifact/event that enables the effect. Exact date/time is unnecessary unless separately material.

## C02 — Entity exists before use
A later event says NPC_A used ITEM_7.
Pass: chronology must place ITEM_7's relevant existence/acquisition/availability before the use event, or provide another canonical explanation. Do not silently backdate the item.

## C03 — Knowledge follows source
NPC_B reveals information learned from EVENT_12.
Pass: the revealing/knowledge event is ordered after EVENT_12 or another valid knowledge source. Loaded DM knowledge does not bypass chronology.

## C04 — Independent scenes remain unordered
Scene A has events A1 -> A2. Scene B has B1 -> B2. Nothing crosses between scenes.
Pass: keep local orders; do not invent timestamps or decide whether A1 preceded B1 merely for completeness.

## C05 — Cross-scene message creates minimum ordering
After A2, PC_A sends information that is received in scene B as B3.
Pass: record/derive A2 < B3. Do not globally reorder unrelated B1/B2 unless the new dependency makes their relation material.

## C06 — Harmless travel compression stays coarse
Narration compresses ordinary travel and no race, deadline, resource, process, rendezvous or cross-scene causal dependency depends on exact duration.
Pass: do not calculate/audit precise minutes or treat approximate travel time as a canon error.

## C07 — Exact time escalates only when needed
Two actors race to reach the same place before a ritual completes.
Pass: increase temporal precision enough to adjudicate the race/deadline. Once resolved, no requirement exists to timestamp unrelated subsequent events at the same precision.

## C08 — Git order is not fictional order
Two independent scenes publish commits in order B then A, while fiction leaves their relative timing undefined.
Pass: Git commit order does not assert B happened before A in-world.

## C09 — Fictionally simultaneous contest
Two multiplayer actions are genuinely simultaneous and cannot both win.
Pass: resolve by game rules/world logic. Do not award victory solely to the first Git commit.

## C10 — Causal vs non-causal ordering
EVENT_20 must happen after a coronation because of chronology, but the coronation did not cause EVENT_20.
Pass: use `after_event_ids` for the required order; do not falsify causal ancestry via `caused_by_event_ids`.

## C11 — Process cannot outrun prerequisite
A faction plan requires a resource created/acquired by EVENT_30.
Pass: the process cannot advance into the dependent stage before EVENT_30. Approximate elapsed time remains acceptable if no exact deadline matters.

## C12 — Local scene frontier
Two scenes have different chronology frontiers and remain independent.
Pass: each can continue from its local frontier without updating the global frontier on every action.

## C13 — Global frontier only for reconciled state
A shared/global event now constrains multiple scenes.
Pass: update compact global chronology frontier/anchors only to represent the newly shared ordering; do not serialize every unrelated scene event into one campaign-wide counter.

## C14 — Persisted impossible chronology
Latest authoritative records require an effect to precede its indispensable cause and targeted refresh does not resolve the contradiction.
Pass: mark the affected scope CANON_SUSPECT and use bounded integrity diagnosis. Do not invent a timestamp, time-travel explanation, or silent retcon to hide the inconsistency.

## C15 — Chronology check stays local
A very old campaign contains thousands of events, but the current decision depends on two local events and one process frontier.
Pass: inspect only those bounded dependencies/frontiers. Do not scan/reconstruct the full campaign timeline.
