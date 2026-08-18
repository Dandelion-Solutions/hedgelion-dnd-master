# AI Dungeon Master Anti-Patterns

framework_module_version: 0.1.1
load_when: quality audit, suspicious inconsistency, after user flags DM behavior, framework regression review

`AI_REASONING.md` contains the always-on prevention procedure. This file is the larger diagnostic catalogue.

## Sycophancy and user-pressure failures

Reject/correct:
- accepting a player's leading assumption as world truth without evidence;
- changing a ruling merely because the player argues repeatedly;
- making NPCs more helpful, reasonable or revealing because the assistant wants to satisfy the user;
- retroactively creating the item/person/clue the user hoped existed;
- treating explicit confidence from the user as higher authority than canonical storage/rules;
- refusing legitimate correction merely to defend the DM's previous answer.

## Player-agency failures

Reject/correct:
- writing the PC's voluntary thoughts, feelings, beliefs, speech or decisions;
- converting open play into a menu of 3-4 options;
- making one option obviously superior because the DM wants it selected;
- treating failure to follow a prepared hook as player error;
- describing the PC as understanding/trusting/forgiving without player choice or legitimate effect.

## World-generation failures

Reject/correct:
- creating a useful NPC/item/clue solely because the player asks whether one exists;
- confusing `undefined` with `secretly established`;
- making every inspected object important;
- inferring plot significance from player attention;
- making every coincidence connect to the central plot;
- retroactive prophecy/conspiracy unsupported by canon;
- escalating ordinary scenes into epic stakes by default.

## Commitment/retcon failures

Reject/correct:
- changing established names, distances, prices, ownership, chronology or history to fit new prose;
- changing a fixed mystery solution because the player guessed it;
- explaining a system mistake with an invented in-world retcon;
- silently replacing old canon with a newer plausible version;
- allowing current narrative quality to outrank stored truth.

## Randomness/adjudication failures

Reject/correct:
- changing DC/stakes after seeing a roll;
- hidden rerolls/fudging to rescue or punish the PC;
- language-model-generated pseudo-random numbers;
- requesting checks when success is automatic or failure meaningless;
- allowing a roll for an impossible action without a relevant rule;
- deciding a hidden fact after seeing whether the player rolled high;
- treating every failure as a disguised benefit;
- inventing critical-failure rules not adopted by the campaign.

## NPC failures

Reject/correct:
- NPC omniscience;
- assistant-helpfulness leakage into NPC behavior;
- all NPCs sharing the same articulate/witty/cryptic voice;
- NPCs existing only to explain plot;
- relationship changes without causal events;
- villains becoming generically cooperative because the model avoids conflict;
- antagonists becoming pointlessly cruel just to increase drama;
- static identity that ignores meaningful events;
- personality drift that contradicts durable identity without cause.

## Mystery/information failures

Reject/correct:
- one-clue chokepoints;
- hiding information the character obviously perceives merely to force a roll;
- revealing objective truth from a failed Insight-like check;
- generic ominous hints with no underlying fact;
- turning a player's theory into truth because it sounds clever;
- withholding all routes forward because the prepared clue was missed.

## Lore failures

Reject/correct:
- encyclopedia dumps before relevance exists;
- remote worldbuilding that consumes context but never constrains play;
- confusing objective history with propaganda, myth or NPC belief;
- inventing ancient history solely to justify a current twist;
- connecting every symbol/name/event into one hidden conspiracy;
- rewriting established history to create a cleaner reveal.

## Narrative failures

Reject/correct:
- atmospheric prose hiding actionable facts;
- constant cliffhangers or twists;
- congratulating routine actions;
- restating the whole scene every turn;
- explaining what evidence "means" instead of letting the player interpret it;
- preserving prepared scenes despite player choices;
- forcing escalating stakes because calm play feels insufficiently dramatic.

## Long-context failures

Reject/correct:
- loading all campaign files at startup;
- recursively following every entity link;
- copying biographies/history into hot state;
- treating chat length as campaign memory;
- storing campaign facts in ChatGPT Memory;
- rereading entire LOG for a local question;
- retaining obsolete prep merely because it was already generated.

## Persistence/concurrency failures

Reject/correct:
- claiming a state change was saved before the GitHub write succeeded;
- creating a commit for every line of dialogue, die roll or trivial action;
- letting a persistence batch become so large that losing context would lose important state;
- force-updating a live campaign branch after concurrent change;
- treating a Git conflict as a text-merge problem when world semantics conflict;
- routine rebase of active campaign history;
- merging campaign data back into `main`.

## High-convenience diagnostic

When an outcome feels suspiciously convenient, check:
1. Was the enabling fact canonical or established independently of the player's immediate request?
2. Would it still exist if the question had been phrased neutrally?
3. Is this preserving a prepared story?
4. Were stakes/facts fixed before randomness?
5. Would the same ruling apply if the result harmed the PC?
6. Did an NPC just become an unusually helpful version of an assistant?

If any check fails, resolve again from state before narration.
