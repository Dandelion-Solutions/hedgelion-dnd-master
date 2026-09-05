# R2.7 WP-19 — Bootstrap / Campaign Creation / Initial Materialization — Architecture Task Brief

Status: **STEP 1 COMPLETE — PO INPUT INTEGRATED / CRITIC RE-RUN COMPLETE — MANDATORY SENIOR REVIEW**

Date: 2026-09-05

Original Step-1 execution basis: `5fc24905be5c9e1b47929ee9e7b49ea8b9f2a053`

Senior-recovery basis: `df5fe6441c2b85e9cbffcb6f83caa885501da794`

Product-Owner integration basis: `4b7411b10b30cc191141826aacb3b0c88e7eeb37`

This Task Brief frames WP-19 Step-2 evidence/research only if later Senior-authorized. It now incorporates the accepted Product Owner requirements `PO-001` and `PO-002` in addition to the recovered bootstrap/materialization and verification framing.

It does not authorize or begin Step 2, Senior review, WP-20, implementation planning, gameplay bootstrap, campaign creation, or substantive runtime/schema/template/test implementation.

Companion artifacts:

- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-source-manifest.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-bootstrap-campaign-creation-initial-materialization-task-brief-critic.md`;
- `DEV/docs/superpowers/design/2026-09-05-r2-7-WP-19-product-owner-input-integration-checkpoint.md`.

Accepted Product Owner semantic authority:

- `DEV/docs/superpowers/specs/2026-09-05-hdm-gameplay-retrospective-and-campaign-exit-owner-decision.md`.

---

## 1. Problem statement

WP-19 audits the complete campaign entry/creation/initial-materialization path and the immediately adjacent interaction-routing/navigation contracts that determine what happens once a campaign is selected and how the current selected gameplay context may be exited safely.

The creation path remains:

```text
storage selection / baseline
    -> explicit campaign/New Game choice
    -> exact runtime + exact ruleset-set resolution
    -> neutral branch / creator provenance
    -> exact scaffold materialization
    -> first campaign-specific publication
    -> initializing
    -> low-friction setup / optional PROVISIONAL_IDENTITY
    -> READY_PC
    -> PLAY_READY
    -> active normal play
```

The expanded interaction-routing contract is:

```text
selected active + gameplay authorized
    -> ordinary D&D Master gameplay
    -> retrospective/history questions remain ordinary gameplay

selected active + readable but gameplay denied
    -> read-only Commentator

selected completed + readable
    -> read-only Commentator
```

The expanded exit contract is:

```text
explicit save-and-exit
    -> satisfy existing save/durability promise
    -> applicable session/live closure
    -> only after successful required closure terminate current gameplay context
    -> clear selected-campaign gameplay working binding
    -> return to ordinary campaign-selection/menu state
```

WP-19 must prove that these transitions compose existing owners without creating duplicate authority, lifecycle states, memory/history stores, disclosure rights, campaign menus, membership transitions or global multiplayer stop semantics.

The reverse audit still applies: every current bootstrap/runtime instruction, template/schema/tool/test/scenario and new PO consumer route must map back to an accepted owner or explicit disposition.

---

## 2. Goals

If and only if Senior later authorizes Step 2, WP-19 must establish:

1. **Creation preconditions and explicit selection authority** — storage/campaign choice and creator/access gates remain unambiguous.
2. **Exact runtime/ruleset creation identity** — selected package provenance and `ruleset_set_sha256` flow reconstructively into the campaign.
3. **Branch/materializer/initial-publication contract** — neutral ancestry, generated root tree, creator provenance and failure/currentness semantics compose correctly.
4. **Initial campaign data model/materialization** — every generated root/field/projection has an owner or explicit stale/derived disposition.
5. **Lifecycle/readiness composition** — scaffold, PROVISIONAL_IDENTITY, READY_PC and PLAY_READY remain distinct and honestly resumable.
6. **Player/PC/multiplayer authority** — initial PLAYER/PC and creator/join rules consume closed access architecture without reopen by overlap.
7. **Low-friction player-facing setup** — technical infrastructure stays invisible; no compulsory questionnaire or broad pre-generation.
8. **Architecture <-> machine <-> verification closure** — executable tests and scenario catalogs are reverse-conformance consumers, not semantic owners.
9. **Campaign interaction routing after selection** — active/playable enters ordinary gameplay; active readable/non-playable and completed readable enter read-only Commentator; no additional mode hierarchy.
10. **PO-001 retrospective consumer** — an authorized active player can ask natural-language history questions in ordinary gameplay, with bounded history retrieval, player/PC eligibility, no-spoiler disclosure and proper-source escalation.
11. **PO-002 save-and-exit consumer** — save correctness precedes exit; exit clears selected gameplay context and re-enters the existing menu without implicit pause/completion/archive/membership/control/global-live changes.
12. **Downstream acceptance routing** — leave concrete runtime/test destinations for later authorized realization without beginning implementation planning.

---

## 3. Non-goals and explicit boundaries

WP-19 Step 1/2 must not:

- run a real campaign or player bootstrap during architecture work;
- begin Step 2 before explicit Senior GO;
- begin WP-20 or future migration/evolution design;
- preserve obsolete unreleased scaffold structures for backward compatibility;
- reopen accepted Story/continuity, truth/knowledge/disclosure, access/multiplayer, readiness, House-Rules, persistence or ruleset architecture merely because new consumers use them;
- create a new Story/history/memory owner, disclosure authority or retrospective database;
- require an authorized active player to enter Commentator merely to ask about campaign history;
- add a second mode hierarchy above ordinary gameplay/read-only Commentator routing;
- treat Story/repository visibility as player entitlement to hidden information;
- make a retrospective question itself mutate world truth, PC knowledge or campaign state;
- introduce a new lifecycle value such as `exited`;
- treat exit-to-menu as automatic `paused`, `completed`, `archived`, membership leave, PLAYER deactivation, PC-control transfer, mode change or campaign-global stop;
- close a multiplayer live epoch merely because one participant's chat exits unless the existing live owner independently requires closure/consolidation;
- create a second campaign-selection/menu authority;
- treat test existence/CI green as architecture authority;
- rewrite runtime/schema/template/test surfaces during Step 1 merely to make the framing tidy;
- start implementation planning or substantive implementation.

---

## 4. Established accepted constraints

### 4.1 Existing recovered WP-19 creation constraints remain controlling

The previously recovered Step-1 constraints remain in force:

- explicit campaign choice precedes campaign-specific work;
- New Game resolves storage schema-v3 `engine.baseline` to one exact runtime package;
- branch ancestry and first generated campaign tree are distinct;
- creator derives from first campaign-specific commit provenance;
- `init_campaign.py` is the exact scaffold materializer and requires `ruleset_set_sha256`;
- current bootstrap prose omits that required ruleset input and must later be reconciled (`F19-S1-01` remains closed as a framing finding);
- stale Storage-v2 projections are not compatibility requirements;
- package provenance is package-owned, not reconstructed from mutable tag state;
- card/README are projections only;
- scaffold, provisional onboarding, READY_PC and PLAY_READY are semantically distinct;
- setup infrastructure is normally invisible;
- campaign discovery is card-first;
- initial multiplayer consumes closed access architecture;
- House-Rules template presence does not reactivate House-Rules design;
- verification catalogs are consumers and may contain stale expectations.

`F19-S1-*` and `SR19-01` are retained/closed.

### 4.2 Campaign selection now has an explicit interaction route

The Product Owner has settled:

```text
active + gameplay participation allowed
    -> ordinary D&D Master gameplay

active + readable + gameplay participation denied
    -> read-only Commentator

completed + readable
    -> read-only Commentator
```

Access/lifecycle owners determine the facts. `CAMPAIGN_CARD` is only a cheap display hint and cannot grant or deny final gameplay authority.

No extra mode hierarchy is introduced.

### 4.3 Retrospective/history questions are ordinary gameplay for an authorized active player

Examples such as “remind me what happened”, “who is this NPC?”, “why did they act that way?”, “tell me about that session/place” remain inside the ordinary Master interaction. The existing OOC `Master` channel may carry such a question without advancing fictional time.

The runtime must not route the player into Commentator merely because the question is retrospective.

R2.4's statement that Commentator is a separate mode remains valid for spectator/read-only serving. It is **qualified by the new explicit consumer binding**: Commentator is not the required history interface for a normal authorized active player.

### 4.4 Retrospective evidence does not widen disclosure

The answer pipeline must preserve:

```text
current request/purpose/player/PC
    -> R2.3 eligibility + bounded retrieval
    -> R2.1/WP-18 Story/history orientation where eligible
    -> current/native owner escalation when claim is material/current/source-specific
    -> world.knowledge / runtime.disclosure / Step-5.12 eligibility
    -> ordinary Narrator-visible answer
```

Story/history availability is not truth/currentness/knowledge/disclosure authority. Repository readability is not character knowledge. Exact historical wording must not be fabricated when only semantic evidence exists.

The question itself does not create new PC knowledge or canon merely by being asked.

### 4.5 Save-and-exit is not the same intent as save-and-stop

The older save/durability contract correctly says `save and stop` composes:

1. explicit save;
2. a separately intended lifecycle/session stop/pause under applicable rules.

The new Product Owner requirement is different:

```text
save and exit to campaign selection
    = explicit save
      + current gameplay-context/navigation exit
      + campaign-menu re-entry
```

It does **not** contain a pause/lifecycle mutation unless the player separately asks for one.

### 4.6 Save success must precede successful exit acknowledgement

An explicit save-and-exit cannot clear/discard the current selected gameplay working context before the existing save promise and applicable session/live durability closure are safely satisfied.

If required save/publication fails:

- do not say `saved`;
- do not falsely say the requested save-and-exit fully succeeded;
- preserve/adopt the strongest truthful recovery-safe current context/frontier;
- report only the minimal actionable failure;
- do not manufacture rollback or alternate lifecycle state.

### 4.7 Exit-to-menu is context navigation, not campaign-state mutation

By itself exit must not:

- set `paused`, `completed` or `archived`;
- leave multiplayer membership;
- deactivate PLAYER;
- relinquish/transfer PC control;
- switch campaign mode or join policy;
- stop the entire multiplayer campaign;
- close a live epoch solely because one chat ended.

Membership leave/removal remains a separate explicit access-control transition. `LIVE_SCENE.md` explicitly says not to close a live epoch merely because one player's chat ended while differently controlled PCs still share the scene.

### 4.8 Same-chat menu re-entry reuses the existing selection gate

After successful exit from the selected gameplay context, the runtime returns to the same campaign-selection/menu state already owned by bootstrap/card/access rules. A new chat is an alternative entry path, not the only path.

Once back at campaign selection, no campaign-specific work resumes until another explicit campaign choice is made.

### 4.9 Verification state is mixed and the new PO flows need dedicated acceptance coverage

Earlier SR19-01 stale/current dispositions remain valid, including stale B12/B22/B23/C12/T13 and qualified B25/access/update cases.

For the new inputs:

- `REGRESSION_CASES:T04/T08` support knowledge separation and bounded old-history retrieval;
- `EXPLICIT_SAVE_CASES:S07` proves save alone does not pause;
- `S08` is current only for true save+stop intent, not exit-to-menu;
- `S15/S16` support success/failure ordering;
- `MULTIPLAYER_MEMBERSHIP_CASES:M01/M10` prove leave/removal/live revocation are separate explicit transitions;
- card/install cases support menu presentation/choice;
- there is no current direct end-to-end acceptance case for full PO-001 or PO-002 semantics.

That missing coverage is a later verification obligation, not authority to edit tests in Step 1.

---

## 5. Quality attributes

Step-2 alternatives/recommendations must preserve:

- authority correctness and no duplicate owners;
- deterministic/reconstructive engine/ruleset identity;
- honest resumability;
- player agency and explicit campaign choice;
- information eligibility / spoiler containment;
- bounded historical retrieval with proper-source escalation;
- ordinary-gameplay continuity for active-player retrospective questions;
- navigation correctness: save success before context exit, then exact menu re-entry;
- lifecycle/membership/live non-interference;
- low latency and bounded I/O;
- atomic/current publication where native owners require it;
- projection safety;
- testability and traceability across current owners and scenario/executable consumers;
- maintainability: no stale scenario or ambiguous `stop`/`exit` wording can become implementation authority.

---

## 6. Step-2 evidence questions after Senior GO

The existing storage/package/materializer/readiness/multiplayer/verification questions remain required. The expanded basis adds these mandatory groups.

### K. Campaign selection -> interaction routing

43. After a campaign is selected, which authoritative lifecycle/access facts determine ordinary gameplay versus read-only Commentator?
44. Where is the exact consumer routing represented without creating a second mode hierarchy?
45. How does completed-readable routing enter Commentator without treating completion as resumable gameplay?
46. How are card hints revalidated against actual creator/PLAYER/access owners before selecting interaction mode?

### L. PO-001 retrospective/history inside ordinary gameplay

47. Which ordinary runtime intent/OOC interaction surface recognizes retrospective/history questions without switching to Commentator?
48. What registered R2.3 purpose/need profile supplies bounded history retrieval for that request?
49. Which player/PC/role eligibility filters are applied before Story/history evidence can reach visible output?
50. When Story is insufficient, stale, too coarse or noncurrent, which current/native owner supplies stronger evidence?
51. How is exact wording distinguished from semantic reconstruction?
52. How does the runtime ensure repository/Story visibility cannot reveal NPC motives, secrets or future/hidden information unavailable to the current player/PC?
53. Does the retrospective response remain nonmutating unless a separate gameplay/knowledge event independently occurs?
54. Which runtime instruction and acceptance-test destinations prove the active player stays in ordinary gameplay?

### M. PO-002 save-and-exit to campaign selection

55. How is save-and-exit intent distinguished from plain save, save-and-stop/pause, explicit leave, campaign completion and new-chat abandonment?
56. Which native save/session/live domains must complete before exit may be acknowledged successful?
57. What exact failure state is retained when one required save domain fails or publication outcome is ambiguous?
58. At what point may selected-campaign hot/working context be cleared safely?
59. Which selected-campaign bindings/caches are session-local and must be cleared, and which campaign/PLAYER/PC state must remain untouched?
60. How does same-chat bootstrap/menu re-entry avoid accidentally treating the old campaign as still selected?
61. Which explicit selection barrier applies after exit before any next campaign-specific read/runtime resolution?
62. In multiplayer, when does an explicit save require live consolidation, and when must the live epoch remain active for other participants?
63. How do tests prove exit does not cause `paused`, `completed`, `archived`, PLAYER deactivation, membership leave, PC-control transfer or global campaign stop?
64. Which existing `save and stop` scenarios need qualification so they cannot be reused as exit-to-menu semantics?

### N. Expanded Product Owner/process gate

65. Does every applicable PO route now have an accepted owner plus current or valid deferred consumer destination?
66. Did the critic find any true CONTRADICTION or MATERIAL INSUFFICIENCY rather than a new consumer binding?
67. Is any remaining issue genuinely Product Owner-owned under the six-category decision gate?
68. If no, keep all remaining reconciliation agent-owned and do not manufacture NEEDS_PO.

---

## 7. Expanded dependency subgraph requirement

Step 2 must start from, but not be limited to:

```text
PO ledger + PO process + accepted owner decision

campaign bootstrap/creation graph
    -> INSTALL / BOOTSTRAP_RUNTIME / NEW_CAMPAIGN_FAST_PATH / CAMPAIGN_SETUP
    -> STORAGE / branch / access / ruleset identity / materializer
    -> campaign templates/schemas/projections
    -> persistence/readiness/session/multiplayer
    -> executable + scenario reverse-conformance

PO-001 graph
    -> Step-4 truth/knowledge/disclosure/role context
    -> Step-5.12 delivery/disclosure
    -> R2.1 continuity/history
    -> R2.3 Context Runtime
    -> R2.4 ordinary TurnEnvelope / Narrator / Commentator distinction
    -> WP-18 final Story/continuity owner
    -> RUNTIME / PLAY_POLICY / INFORMATION / NARRATIVE
    -> history/knowledge/disclosure tests/scenarios

PO-002 graph
    -> Step-5.5 save durability
    -> SAVE_CONTRACT / PERSISTENCE / DURABILITY_GUARD
    -> SESSION / RUNTIME
    -> BOOTSTRAP_RUNTIME / install bootstrap / CAMPAIGN_CARD
    -> ACCESS_CONTROL / MULTIPLAYER / LIVE_SCENE
    -> save/session/menu/access/membership/live tests/scenarios
```

---

## 8. Failure scenarios later architecture must survive

The previously recorded creation/SR19-01 cases remain. Add at minimum:

23. authorized active player asks who an old NPC is; runtime incorrectly routes to Commentator;
24. Story knows a hidden motive but current player/PC is not entitled to it; retrospective answer leaks it;
25. Story summary is stale/coarse while a material current answer requires native owner evidence;
26. player asks for exact past wording but only semantic historical evidence exists;
27. retrospective question itself is treated as a new PC-knowledge/canon event without an independent information path;
28. active readable foreign singleplayer campaign is selected and runtime accidentally grants ordinary gameplay instead of read-only Commentator;
29. completed readable campaign is selected and runtime attempts normal resume instead of read-only Commentator;
30. player says save-and-exit; runtime changes lifecycle to paused solely because an older `save and stop` scenario exists;
31. save-and-exit clears the selected working context before save publication succeeds;
32. save partially fails but runtime reports both saved and exited;
33. multiplayer participant exits to menu and their PLAYER becomes inactive despite no leave request;
34. exit silently relinquishes/transfers PC control;
35. one participant exits and runtime closes/stops a still-valid shared live scene/campaign for the other participants;
36. successful save-and-exit opens a second ad-hoc menu implementation rather than the normal card-first selection gate;
37. same-chat menu re-entry keeps old campaign implicitly selected and performs campaign-specific reads before the next explicit choice;
38. implementation relies on supporting old tests while no direct PO-001/PO-002 acceptance case exists.

---

## 9. Product Owner decision status on expanded basis

The Product Owner already settled the relevant semantics:

- active authorized retrospective questions are ordinary gameplay;
- Story/history is constrained by current knowledge/disclosure/no-spoiler owners;
- active non-playable readable and completed readable campaigns route to read-only Commentator;
- save-and-exit returns to campaign selection only after required save/session/live closure;
- exit alone is not pause/completion/archive/leave/deactivation/control transfer/global stop;
- no extra mode hierarchy is desired.

The expanded evidence found no contradiction requiring those decisions to be reopened. Remaining exact consumer placement, context assembly, runtime state clearing, live/save composition and verification realization are technical architecture/implementation work.

```text
HUMAN_DECISION_REQUIRED: NO
UPSTREAM_REOPEN_REQUIRED: NO
```

No `NEEDS_PO` entry is warranted.

---

## 10. Step-1 exit criteria after PO integration

```text
[x] Pre-input Source Manifest/Task Brief/SR19-01 evidence retained as historical basis.
[x] Applicable PO-001/PO-002 ledger entries and shared immutable context inspected.
[x] Product Owner Input Process applied.
[x] Accepted PO owner decision incorporated into the Source Manifest and Task Brief.
[x] PO-001 dependency graph expanded through current information/history/disclosure/ordinary-gameplay owners and consumers.
[x] PO-002 dependency graph expanded through current save/session/bootstrap/menu/access/multiplayer/live owners and consumers.
[x] Campaign interaction routing recorded without a new mode hierarchy.
[x] `save and stop` and `save and exit-to-menu` explicitly distinguished.
[x] Relevant tests/scenarios dispositioned; direct PO acceptance gaps recorded downstream.
[x] Original F19-S1-* and SR19-01 findings retained/closed; none reopened without contradiction.
[x] Whole-project Task-Brief critic rerun independently on expanded basis.
[x] Every mechanically resolvable BLOCKING/SIGNIFICANT new framing defect repaired.
[x] Product Owner boundary rerun; HUMAN_DECISION_REQUIRED=NO.
[x] UPSTREAM_REOPEN_REQUIRED=NO.
[x] Step 2 remains unauthorized/unstarted.
[x] WP-20 remains unstarted.
[x] Implementation planning/substantive implementation remain unstarted.
```

The next process action is **mandatory Senior review of the expanded Step-1 package**. Only explicit Senior GO may authorize WP-19 Step 2.