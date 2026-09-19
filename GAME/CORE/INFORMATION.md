# Information, Clues and Mysteries

framework_module_version: 1.0.6
load_when: investigation, mystery, lore discovery, perception, hidden information

## Information layers

Maintain explicit separation between native owners:
- `world.lore_fact` — objective proposition identity, truth status and lifecycle;
- `world.knowledge` — one current fictional subject-to-fact relation, with accepted native evidence;
- `runtime.disclosure` — material information emitted to one human recipient;
- `runtime.message` — accepted communication evidence, not proposition truth.

Visibility, possession, narration, repository readability, cache/index presence and Story availability do not establish knowledge or disclosure. A knowledge transition requires accepted native evidence; legacy embedded PC/NPC/Faction knowledge arrays are migration input or derived convenience, never parallel writable authority.

Before player-facing emission, validate recipient-scoped disclosure references against eligible source evidence. One outbound message and its material disclosure transitions form one semantic closure; delivery to one recipient never advances another recipient's disclosure or any PC's knowledge.

During a selected LIVE epoch, `live_facts`, perception lists and other physical LIVE material are bounded evidence/input only. Normalize material information through the selected `LiveRouting` entry, exact current source and the native lore/knowledge/disclosure/message owners; a missing, orphaned, superseded or stale source, recipient mismatch or legacy visibility field fails closed. LIVE physical presence never creates a second knowledge or disclosure authority, and campaign-base/current-scene projections never substitute for the selected source.

Knowledge requires a source: observation, testimony, inference, magic, prior history, records or another established mechanism.

## Character knowledge is perspectival

Information legitimately received from another character, document, observation or other source may become part of a PC/NPC's working knowledge or belief even when the DM does not know that statement to be objectively true.

Do not promote testimony, rumor, interpretation, identification, expertise-based judgment or remembered information into objective world truth merely because a character currently accepts it. Conversely, do not require the Master to verify every received statement against all objective records before allowing the character to believe or act on it.

Different PCs/NPCs may hold different, incomplete or mutually incompatible views of the same event, person or object. This is valid world state and is not a canon conflict by itself. Differences may arise from source reliability, experience, expertise, perception, memory, deception, incomplete identification or ordinary interpretation.

When later evidence changes what a character reasonably believes, update that character's knowledge/belief state from the new source. Do not retroactively erase the fact that they previously believed something else, and do not rewrite objective truth merely to make the earlier belief correct.

For rules adjudication, subjective understanding does not replace objective canonical mechanics. A character may misunderstand an item's capabilities or another creature's competence while the DM still resolves actual effects from the applicable canonical state/rules.

Persist these distinctions only when future play may depend on them. Do not create extra records or perform repository-wide consistency checks merely to represent harmless differences of perspective.

## Do not gate the campaign behind one point of failure

Important conclusions should normally have multiple independent routes of discovery.

For a conclusion required to keep a scenario moving, prepare redundant clues/routes rather than relying on one check, one NPC or one location.

A failed check may reduce detail, consume time, create risk or force another route, but should not arbitrarily erase an objectively obvious clue the character is already examining.

## Clues are facts, not rails

A clue provides information that helps players form their own plans. It is not an instruction telling them which scene the DM wants next.

Prefer clues that can support multiple interpretations/actions when the world naturally allows it.

## Floating clues with constraints

Session preparation may include location-independent secrets/clues that can be revealed through whichever credible source the characters encounter.

This is preparation flexibility, not retroactive reality editing.

Once a clue is concretely established as originating from a particular source/event, that origin becomes canon.

Never place a clue somewhere merely because the player asked whether that place contains something useful.

## Perception and obvious facts

Do not require rolls for information a competent character would automatically notice under the circumstances.

Use uncertainty only for genuinely hidden, subtle, contested or time-sensitive information.

When a character searches a precisely relevant place with ample time and no meaningful failure state, consider giving the basic fact automatically and reserving rolls for speed, additional detail, interpretation or avoiding cost.

## NPC testimony

NPC statements are not automatically true. NPCs may:
- know;
- infer;
- misunderstand;
- remember imperfectly;
- lie;
- omit;
- repeat rumor.

Persist the distinction when it matters.

## Mystery hygiene

Before running a mystery, internally distinguish:
- solution / objective truth;
- evidence;
- possible conclusions players may draw;
- false beliefs/rumors that exist in-world;
- red herrings that have an actual cause rather than being arbitrary noise.

Do not change the true solution after seeing the players' theory merely to surprise them.

## Information density

Give enough sensory/context information for a meaningful decision, but do not dump every latent fact in the scene.

When the player asks a focused question, answer what the character can determine from the current state rather than expanding the scene with unrelated hooks.
