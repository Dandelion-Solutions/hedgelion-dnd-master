# Step 5.5 — SOFT / HARD / SAVE Durability Semantics — Research Draft

Status: **RESEARCH / DRAFT — NOT CANONICAL**

Date: 2026-08-20

Basis:

- `2026-08-20-step-5-5-soft-hard-save-durability-task-brief.md`
- Step-3 canonical execution ownership
- Step-5.1 B-NARROW frontier model
- Step-5.2 canonical Resumable Runtime Closure v2
- Step-5.3 canonical A-NARROW temporal/pending continuity
- Step-5.4 canonical BARRIER-NATIVE host lifecycle/handoff
- current runtime durability/save/persistence/storage/session/integrity/shared-world contracts and regression cases

This document is research, not an owner decision and not a candidate specification.

---

# 1. Executive research result

The current runtime has the right broad product shape — established singleplayer state may remain dirty for many turns, explicit `save`/`сохрани игру` is stronger than ordinary buffering, and forced boundaries publish coherent batches — but its present `EPHEMERAL / SOFT / HARD` vocabulary conflates three different architectural questions:

1. whether a value is gameplay-significant and intended to survive;
2. whether the current established value is already durable;
3. whether some specific future semantic edge is forbidden until a required durable closure exists.

The research therefore recommends separating those axes.

Conceptually:

```text
SEMANTIC SURVIVAL CLASS
    EPHEMERAL
    ESTABLISHED

CURRENT DURABILITY STATUS
    DURABLE
    VOLATILE_DIRTY

CURRENT DURABILITY OBLIGATION
    MAY_DEFER
    MUST_BE_DURABLE_BEFORE(edge)
```

`SOFT` remains useful shorthand for:

```text
ESTABLISHED
+ VOLATILE_DIRTY
+ MAY_DEFER
```

`HARD` should not be treated as a permanent intrinsic class of a fact. The cleaner meaning is an **outstanding durability obligation attached to a specific semantic barrier edge**:

```text
MUST_BE_DURABLE_BEFORE(edge)
```

Examples of different barrier edges:

```text
shared interactive live fact
    -> durable/live-canonical BEFORE_NARRATION_OR_SHARED_REVEAL

PLAY_READY establishment
    -> durable BEFORE_FIRST_TRUE_LIVE_PLAY

explicit save
    -> durable BEFORE_SAVE_SUCCESS_ACK

controlled handoff
    -> durable BEFORE_HANDOFF_SUCCESS_AND_RELINQUISHMENT

membership/access transition
    -> durable BEFORE_NEW_AUTHORITY_IS_TREATED_EFFECTIVE

SOFT-exposure ceiling
    -> durable BEFORE_NEXT_ORDINARY_GAMEPLAY_EXTENSION
       at the first available enforcement opportunity
```

This preserves the intuitive runtime term `HARD` while removing the false implication that all HARD reasons must block exactly the same thing.

The second central result is that required publication completeness must be defined as a **durability-obligation-rooted, transitive recovery closure**, not merely “the causal files” and not automatically “every dirty record in the campaign.”

The third central result is that explicit `save` / `сохрани игру` is intentionally stronger than a narrow ordinary forced boundary: successful save should mean **all established gameplay-significant dirty state in the selected save scope, plus every required transitive recovery dependency, is actually durable**. It still does not imply pause, activation, checkpoint creation, or Story/transcript projection freshness.

The fourth result is that the current `one hour` implementation model is architecturally flawed even aside from the unapproved numerical value. Measuring exposure as `now - durable_frontier_time` can make a newly created dirty fact inherit the age of an unrelated old commit and can let an unrelated publication reset exposure for still-dirty state. The semantic exposure clock should begin when relevant established state first becomes unpublished and should reset only when that state/partition becomes durable.

The fifth result is that advisory host-capacity risk from Step 5.4 should not itself become a mandatory durability obligation. It is too unreliable. It may warn and offer handoff; explicit handoff then creates the real BARRIER-NATIVE obligation. An opportunistic safe-point flush may be a future policy optimization, not a correctness prerequisite.

---

# 2. Evidence classification

## FACT F1 — Current runtime already separates truth from remote durability

`DURABILITY_GUARD.md` and `RUNTIME.md` state that durable gameplay facts become true in the hot working set immediately, while most ordinary singleplayer changes may remain SOFT until a later boundary.

Therefore remote publication is not the semantic event that makes a normal singleplayer fact true.

## FACT F2 — Sparse singleplayer persistence is deliberate

Current regression contracts explicitly protect:

- many ordinary turns with zero GitHub traffic;
- multiple dirty domains without an automatic save;
- ordinary scene/encounter completion without an automatic save;
- zero-I/O boundary classification;
- one coherent transaction when a real boundary fires.

Any Step-5.5 design that converts “meaningful change” into an immediate publication trigger would regress an explicit product goal.

## FACT F3 — Explicit save already has a strong user-facing promise

Current `SAVE_CONTRACT.md` defines `save`, `save game`, `сохрани игру` and equivalents as materialization of all established cross-session campaign state from the hot working set into normal authoritative records.

Regression cases reject summary-only persistence, missing entity/index materialization and partial success reporting.

## FACT F4 — Explicit save is not pause/readiness/checkpoint

Current runtime and tests already distinguish:

- `save` from `pause`/`stop`;
- durability from campaign activation/readiness;
- ordinary save from checkpoint creation.

These separations remain compatible with current architecture.

## FACT F5 — Step 5.2 requires transitive required-dependency closure

A promised durable source set is valid only if every recovery-semantic dependency is durable, optional, or deterministically rebuildable.

This includes owner routing and interpretation context where required.

Therefore “publish the triggering file” is not a sufficient general HARD rule.

## FACT F6 — Reference closure is already required in current storage

When a new stable ID is created in HOT state, a transaction that first publishes a durable reference to that ID must also include the new record and required index entry.

This is a non-causal-looking but correctness-critical reference/materialization dependency.

## FACT F7 — Step 5.3 forbids split source/execution durability

A source claim referring to accepted execution that cannot be resolved is an invalid durable state. Root/routing handoff must remain continuously recoverable.

Therefore durability closure may include temporal source state, Step-3 execution state and routing even when only one side triggered the boundary.

## FACT F8 — Step 3 permits locally committed execution before remote campaign publication

ExecutionSegment is the local deterministic commit boundary for world/runtime mechanics. Earlier committed mechanical facts are not rolled back because later work fails.

Therefore a remote publication failure does not automatically make the established HOT gameplay outcome fictional or undo it. It creates an unsatisfied durability obligation and recovery exposure.

## FACT F9 — Shared/live rules already demonstrate edge-specific blocking

In active live mode a newly established interactive shared fact is published to the live authority before narration/reveal. By contrast ordinary singleplayer SOFT facts may be narrated while still volatile.

Therefore “HARD always blocks narration” is false as a universal definition; the relevant blocked edge depends on the durability reason.

## FACT F10 — Integrity validation is scope-local

Current integrity contracts validate dirty records and direct dependencies rather than scanning all campaign state/history.

A bounded required-dependency closure is consistent with current performance and integrity architecture.

## FACT F11 — Checkpoint/session are projections, not save authority

Current session and checkpoint schemas classify them as coordination/recovery metadata; checkpoint is explicitly not a snapshot/current-state authority.

Therefore a successful save cannot be defined as “checkpoint exists” or “session record advanced.”

## FACT F12 — Current one-hour regression is concrete implementation debt

`test_hourly_durability_contract.py` asserts the literal formula:

```text
now - durable_frontier_time >= 1 hour
```

The owner has explicitly withdrawn `one hour` as an approved architecture value. Machine realization will need to replace the old test contract, not merely edit explanatory prose.

## FACT F13 — Current wall-clock anchor does not measure actual dirty exposure

Consider:

```text
T0 durable campaign commit
T0 + 5h no gameplay change
T0 + 5h + 1m new SOFT fact X
```

The current `durable_frontier_time` rule immediately reports X as older than one hour even though X has been exposed for one minute.

Conversely, if dirty scope A remains unpublished but an unrelated publication of scope B occurs, a global durable-frontier timestamp can make A look fresh despite still being old volatile state.

This is a model error independent of threshold value.

## FACT F14 — No background runtime opportunity is guaranteed

Current session/runtime contracts already say no exactly timed publication can be promised while the user/host is inactive.

Any exposure ceiling is enforceable only when an authoritative execution opportunity exists, unless a future host provides background callbacks.

## FACT F15 — Step 5.4 capacity telemetry is advisory unless explicitly reliable

No trustworthy remaining message/token/context capacity is assumed. Advisory capacity estimates may be false-positive or false-negative.

They cannot be a correctness prerequisite for durability.

---

# 3. Constraints

## C1 — Truth and durability are separate axes

An established HOT fact can be true but not yet remotely durable.

Architecture must not redefine truth based on storage latency merely to simplify persistence.

## C2 — Required durability must be recovery-complete

If the engine crosses a durability-required semantic edge, surviving durable sources must satisfy Step-5.2/5.3 recovery invariants for the promised point.

## C3 — Closure must remain bounded and domain-typed

Required-dependency traversal does not justify full WORLD traversal, campaign-wide file scans or universal snapshot materialization.

## C4 — No duplicate publication owner

A durability obligation/dirty marker says what must become durable; it does not copy current owner payload as a second authority.

## C5 — No universal barrier edge

Different durability reasons can lawfully block different semantic edges.

## C6 — Explicit save is a player-facing semantic promise

A success acknowledgement must be understandable as “the established game state I asked you to save is recoverable,” not merely “some transaction was attempted.”

## C7 — No heartbeat

Elapsed real time with no dirty established state creates no durability work.

## C8 — No exact timer without execution opportunity

A configured exposure limit cannot guarantee a publication at the exact wall-clock instant it is crossed if the host cannot execute.

## C9 — Physical storage outcome remains Step 5.6

Step 5.5 defines when actual durability is required and what semantic state is blocked until it exists. Step 5.6 defines how Git publication proves/fails that outcome across transport crash windows.

## C10 — Live/shared may be stronger

Step 5.5 provides the general obligation model. Step 5.8 may bind shared/live mutations to earlier visibility/authority edges.

---

# 4. Recommended durability vocabulary

## 4.1 EPHEMERAL

A value is **EPHEMERAL** when its loss does not violate any currently promised gameplay-semantic/recovery contract.

Examples may include:

- disposable presentation texture;
- derived caches;
- unaccepted model reasoning;
- transient prompt/context state;
- scratch calculations after their authoritative result is owned elsewhere.

EPHEMERAL is primarily a semantic-survival classification.

It may later be promoted by a real semantic event, but merely existing in memory does not make it established campaign state.

## 4.2 ESTABLISHED

A value/state relation is **ESTABLISHED** when the engine has crossed the owning semantic acceptance/commit boundary and the state is part of current gameplay truth or required operational continuity.

Established state may currently be durable or volatile.

Examples:

- world mutation committed by deterministic execution;
- accepted RuntimeCommand/Resolution/Continuation state;
- active Procedure state;
- accepted Choice/Reaction offer;
- armed temporal source state;
- accepted player meaning/evidence that current durability policy promises to preserve.

## 4.3 DURABLE / VOLATILE_DIRTY

These describe whether the current established native state needed for a given recovery scope is represented by actually authoritative durable sources.

`VOLATILE_DIRTY` is not a second state owner. It is a derived relationship between current native state and known durable representation.

## 4.4 SOFT

Recommended retained shorthand:

> **SOFT = established gameplay-significant state that is currently volatile/dirty but has no outstanding durability barrier preventing the next ordinary semantic edge.**

SOFT may remain current truth across many ordinary singleplayer turns.

It is exposed to loss if the host dies before another durability boundary.

## 4.5 HARD

Recommended redefinition:

> **HARD = an outstanding requirement that a specified durability closure become actually durable before a named semantic barrier edge may be crossed.**

Conceptually:

```text
DurabilityObligation {
    reason
    affected native scope
    required roots
    barrier_edge
}
```

This is conceptual architecture, not a proposed first-class record/schema.

A fact is not permanently “HARD.” A durability reason creates an obligation over current state. Once the required closure becomes durable, that obligation is satisfied.

This is stronger and less ambiguous than the current runtime phrasing “HARD is a commitment.”

---

# 5. Barrier-edge model

The durability reason owns which edge is blocked.

Initial disposition:

| Reason | Required barrier edge |
|---|---|
| ordinary singleplayer SOFT | none yet; MAY_DEFER |
| PROVISIONAL_IDENTITY / stable readiness guard | before crossing the guard-defined setup/play edge |
| PLAY_READY | before first true mechanics-capable live play is acknowledged/framed |
| focal-location/card durability guard | before the guard-defined transition is treated as durably resumable; exact narration blocking should remain minimal |
| campaign lifecycle transition | before new lifecycle state is acknowledged/effective across session/recovery |
| explicit `save` / `сохрани игру` | before `SAVE_SUCCESS` is reported; current save handling should complete/fail before the next dependent gameplay extension |
| `save and stop` | before save success + intended stop/pause completion |
| controlled handoff | before recovery-safe handoff acknowledgement/relinquishment (Step 5.4) |
| shared/live interactive mutation | before shared reveal/narration when owning live policy requires it |
| membership/access transition | before new access state is treated effective |
| catastrophic continuity guard | before the specific post-transition gameplay edge declared by that guard |
| SOFT-exposure ceiling | before next ordinary gameplay extension at first available enforcement opportunity |

The exact inventory of runtime guard reasons is implementation/catalog policy. The architectural law is that every mandatory durability reason identifies its barrier edge; `HARD` alone is not enough information.

---

# 6. Required durability closure

## 6.1 Reject per-file HARD

Publishing only the record that happened to trigger durability can produce invalid states:

- durable reference to unpublished new ID/record;
- durable RuntimeCommand without required Continuation/RNG/context;
- durable source claim without accepted execution;
- active durable owner with missing recovery-root enrollment;
- durable world state whose required current routing still points elsewhere;
- save that has prose recap but missing native records.

## 6.2 Reject unconditional campaign-global flush for every HARD reason

Suppose dirty scene A and unrelated dirty scene B are independently writable/recoverable, and a narrow lifecycle/access/readiness guard in A becomes HARD.

If A's durability closure has no semantic/recovery dependency on B, forcing B into every A boundary:

- destroys Step-5.2 partitionability;
- increases conflict/latency in multiplayer;
- turns local reasons into campaign-global save semantics;
- creates unnecessary write coupling.

Therefore ordinary HARD does not imply global `SAVE_ALL_DIRTY`.

## 6.3 Recommended: OBLIGATION-ROOTED RECOVERY CLOSURE

For a durability obligation `D`:

```text
R0 = native owner/state roots directly required by D

R* = transitive required-dependency closure over R0
     using Step-5.2/5.3 ownership/recovery laws
```

Include as applicable:

- current authoritative owner records for required roots;
- dirty current values of those owners;
- required new referenced identities + owning records/indexes;
- bounded current routing/root membership needed to recover them;
- RuntimeCommand/Resolution/Procedure/Continuation state required to resume;
- fixed accepted RNG / pending Choice/Reaction / pending mandatory descendants;
- Step-5.3 source occurrence/claim + accepted execution closure;
- compatible accepted runtime/catalog interpretation context references/evidence;
- required causal/provenance evidence when current mechanics/recovery depends on it;
- required directly affected projections only when another owning contract makes their consistency part of the barrier promise.

Exclude:

- unrelated loaded records;
- arbitrary world-graph neighbors;
- rebuildable caches/Agenda/MechanicalContext;
- Story/transcript/editorial projection merely for freshness;
- unrelated dirty native scopes with no required dependency relation.

## 6.4 Whole-current-owner rule

If a required owner/path joins a publication closure, publish its current semantically valid state, not an artificially reconstructed older field subset merely to avoid including another dirty change co-owned by the same native record.

Partitionability is by actual semantic/writable ownership boundary, not by inventing fake field-level historical versions.

## 6.5 Closure validation

Before physical publication, local planning must establish that no published durable reference/recovery root will depend on omitted volatile required state.

This is a bounded local closure check, not a repository-wide health audit.

Step 5.6 owns physical atomicity/crash behavior once the semantic closure is frozen.

---

# 7. Forced boundary versus accumulated SOFT

Three candidate policies were tested.

## Alternative A — GLOBAL FLUSH-ALL-SOFT

Every HARD reason publishes all dirty established state in the campaign.

### Strength

Very simple mental model; current singleplayer runtime often behaves this way.

### Weakness

Overcouples independent scopes, conflicts with 5.2 partitionability, increases multiplayer conflicts and makes every narrow boundary equivalent to save.

## Alternative B — TRIGGER-ONLY

Publish only the directly HARD mutation and its file.

### Strength

Minimum write set.

### Weakness

Incorrect under recovery/reference/source-execution dependencies.

## Alternative C — OBLIGATION-ROOTED RECOVERY CLOSURE — RECOMMENDED

Publish the triggering required roots plus transitive recovery/ownership dependencies; unrelated independent SOFT remains volatile.

### Strength

Correctness-complete, partitionable, sparse and composable with 5.8.

### Cost

Requires explicit dependency-closure planning and test coverage. Some seemingly unrelated records may join when a real recovery/reference dependency exists.

### Recommendation

Adopt C for ordinary forced durability.

Explicit save intentionally uses a broader root set, described next.

---

# 8. Explicit SAVE semantics

## 8.1 User promise

Recommended canonical meaning:

> When the player explicitly requests `save`, `save game`, `сохрани игру`, or an unambiguous equivalent for the selected campaign, successful acknowledgement means that every currently established gameplay-significant dirty state in the selected save scope, together with every transitive dependency required for correct recovery, is actually durable.

This preserves the current `SAVE_ALL_DIRTY` product meaning while grounding completeness in Steps 5.2–5.4.

## 8.2 Save root set

Unlike an ordinary narrow HARD reason, explicit save intentionally seeds closure with **all established dirty native owners in the selected save scope**.

Then apply transitive required-dependency closure.

Conceptually:

```text
SAVE_ROOTS = all established dirty native owners in selected save scope
SAVE_CLOSURE = required_dependency_closure(SAVE_ROOTS)
```

In ordinary singleplayer, selected save scope is normally the current selected campaign's active established dirty state under current ownership routing.

In multiplayer/live mode, exact semantics of “selected save scope” must respect current live ownership; 5.8 must define whether a player can request campaign-wide consolidation, only their authorized scope, or a coordinated save operation.

## 8.3 Save includes operational continuity

If the current promised gameplay point contains an open:

- RuntimeCommand;
- Resolution;
- Procedure;
- Continuation;
- Choice/Reaction;
- accepted mandatory child/firing;
- generated accepted RNG needed by unfinished work;
- armed temporal owner whose current state is part of the saved scope;

then the required native continuity state/routing is part of SAVE_CLOSURE.

A successful save cannot mean “world files were written but the unfinished mechanic can no longer be resumed.”

## 8.4 Save does not require settlement

Save need not finish an open mechanic merely to reach a clean narrative point.

It may durably preserve the exact suspended/active native execution state.

This prevents save from manipulating gameplay or forcing the player toward a convenient stopping point.

## 8.5 Save does not imply checkpoint

Checkpoint remains a separate recovery optimization/evidence decision. If normal native state/routing is sufficient, save may succeed without a new checkpoint.

## 8.6 Save does not imply pause or activation

Plain save preserves current legitimate lifecycle/readiness state.

`save and stop` combines two intents; plain `save` does not stop play.

## 8.7 Save does not imply Story/transcript freshness

Canonical/current gameplay owners and required recovery evidence govern SAVE_CLOSURE.

Noncanonical Story projections may lag unless another live recovery/evidentiary contract makes a specific artifact required. Exact transcript is required only where Step 5.4/5.11 says literal evidence is irreducible.

## 8.8 No-op save

If every established state in save scope is already durable and no required derivative is stale, save may succeed without creating a heartbeat/no-op commit.

The engine may report that the game is saved/already saved without manufacturing a Git write solely to create activity.

---

# 9. Controlled handoff versus SAVE

They share the same closure machinery but have different root-selection semantics.

```text
CONTROLLED HANDOFF
    roots = every established/promised state required to resume the handed-off scope

EXPLICIT SAVE
    roots = every established dirty state in the selected save scope
```

In ordinary singleplayer these root sets will often coincide.

They should not be declared globally identical because:

- handoff can be scoped to a partition/native owner set;
- multiplayer/live ownership may keep independent scopes active;
- save is an explicit player durability intent over a selected campaign scope, not merely host transfer.

Both require actual durability before success acknowledgement.

---

# 10. Publication failure / unresolved durability obligation

## 10.1 Established HOT truth survives confirmed transport failure while host survives

If deterministic execution already committed current HOT state and remote publication fails, the engine does not invent a rollback merely because Git durability failed.

State remains current locally, but the durability obligation is unsatisfied.

## 10.2 Barrier edge remains blocked

The specific `MUST_BE_DURABLE_BEFORE(edge)` remains active until:

- required durability succeeds;
- the underlying required semantic transition is lawfully abandoned before it became established, where that is still possible; or
- the durability reason itself is explicitly abandoned when product semantics permit that reason to be optional.

## 10.3 Non-abandonable obligations

Examples expected to be non-abandonable once established include:

- shared/live commit-before-reveal requirement;
- access/membership state before treating new authorization as effective;
- controlled handoff before claiming/relinquishing safely;
- PLAY_READY before true live play when readiness boundary requires it;
- a fired SOFT-exposure safety ceiling before further ordinary gameplay extension.

Failure blocks the named edge; OOC/repair/retry may continue.

## 10.4 Explicit save failure — product-semantic question remains

If a player explicitly requests save and publication fails while the old host still safely retains HOT state, two plausible contracts exist:

### S-F1 — SAVE REQUEST IS ABANDONABLE

Report save failure. If no independent HARD obligation exists, player may explicitly choose to continue playing with known unsaved exposure.

Pros:
- storage outage does not hard-lock otherwise playable singleplayer session;
- honest state remains available in current host.

Cons:
- user who simply continues after an error may misunderstand persistence risk;
- additional unsaved state increases potential loss.

### S-F2 — SAVE REQUEST BLOCKS ORDINARY PLAY UNTIL RESOLVED

Once requested, save must succeed or be explicitly cancelled before ordinary gameplay continues.

Pros:
- clear save semantics; no accidental “failed save but kept playing” drift;
- bounded failure state.

Cons:
- transient storage failure can interrupt gameplay even though current state is still valid HOT.

Research recommendation: **S-F1 with explicit cancellation/acknowledgement, not silent automatic continuation**. A failed explicit save should return an unsatisfied save result. Ordinary play may resume only if the player explicitly abandons/cancels the save request or a configured product policy permits a clearly communicated unsaved mode. Any independent non-abandonable durability obligation still blocks its own edge.

This is a real owner-level product choice and should be presented in the decision brief.

## 10.5 Crash after failure

If the host dies before required publication succeeds, only the last actually durable compatible closure is recoverable. HOT truth that was never made durable is lost under 5.2/5.4; recovery does not reconstruct it.

---

# 11. SOFT exposure policy

## 11.1 Objective

Ordinary singleplayer may intentionally buffer SOFT, but intended loss exposure should not grow without bound when runtime continues to receive execution opportunities.

This is a risk-control policy, not a fictional timer and not a heartbeat mechanism.

## 11.2 Reject `time since any durable frontier`

Current `durable_frontier_time` conflates:

- age of repository activity;
- age of specific unpublished state.

Those are not equivalent.

## 11.3 Recommended exposure anchor

For each durability partition/scope that currently contains established unpublished state, derive/track:

```text
oldest_unpublished_established_at(scope)
```

Conceptual semantics:

- when a clean scope first acquires established SOFT, set its exposure start to that establishment time/opportunity;
- further dirty changes do not make the oldest exposure younger;
- a successful publication clears/resets exposure only for the state/scope actually made durable;
- an unrelated publication in another scope does not reset it;
- if a required owner migration/repartition occurs, preserve the conservative oldest exposure of still-unpublished state.

This timestamp/age is durability-risk bookkeeping, not fictional chronology or gameplay state authority.

Exact field/storage representation is implementation detail and may remain host-local while the dirty state itself is host-local.

## 11.4 Partitioning

Architecture should support exposure by native durability/writable scope rather than require one campaign-global timer.

A singleplayer implementation may conservatively aggregate all current dirty campaign state into one exposure bucket if that does not lose correctness or create pathological unnecessary writes.

It must not use an unrelated commit to reset an old dirty scope.

## 11.5 Threshold semantics

The architectural rule is:

```text
established unpublished state exists
AND intended exposure limit for its applicable policy is exceeded
AND runtime has an authoritative enforcement opportunity
    -> create MUST_BE_DURABLE_BEFORE(NEXT_ORDINARY_GAMEPLAY_EXTENSION)
```

A stronger immediate obligation always wins earlier.

No numerical threshold is approved by this research.

## 11.6 No background callback

If the limit is crossed while no runtime execution occurs:

- no fictitious timed commit is promised;
- at the next authoritative interaction, evaluate before accepting/extending ordinary gameplay;
- if dirty state survived and the limit is exceeded, satisfy the durability obligation first;
- if dirty state was destroyed with the host, recover from actual durable state and do not invent it.

Thus the guarantee is **bounded intended exposure during available runtime opportunities**, not hard wall-clock RPO.

## 11.7 No heartbeat

If no established state is dirty, exposure does not exist and elapsed time creates no publication.

---

# 12. Advisory host-capacity risk

Three candidate policies:

## H-A — advisory signal itself creates mandatory flush

Rejected as default recommendation.

A false-positive heuristic could create unnecessary expensive HARD boundaries. More importantly, it would make an unreliable predictor part of the normal durability classifier despite Step 5.4 explicitly refusing that authority.

## H-B — advisory signal warns/offers handoff only — RECOMMENDED correctness contract

Step 5.4 warning remains OOC assistance.

If player accepts transfer/handoff, the reliable semantic trigger is explicit handoff intent, which activates BARRIER-NATIVE durability.

If player continues, ordinary SOFT exposure policy remains in force.

## H-C — optional opportunistic safe-point flush

A host/product profile may later choose to publish existing SOFT at a safe available point when advisory risk is high, provided:

- it is framed as an optimization/risk-reduction policy;
- false positives are harmless except extra I/O;
- it does not block a current action merely because the heuristic fired unless a separate real durability obligation exists;
- no correctness guarantee depends on the heuristic.

Research recommendation: canonicalize H-B as the correctness baseline and permit H-C only as future policy optimization. Do not make advisory capacity a HARD reason.

---

# 13. Existing runtime forced-boundary inventory — disposition

The current guard list should be interpreted under the new obligation model rather than retained as permanent state classes.

| Current reason | Research disposition |
|---|---|
| PROVISIONAL_IDENTITY | durability obligation at onboarding recovery edge; exact rule retained/reviewed during realization |
| stable READY_PC crossing another turn | obligation before guard-defined next-turn/readiness edge |
| PLAY_READY | obligation before first true live play |
| focal-location/card change | likely narrow obligation; challenge whether card projection itself should block and exactly which edge |
| lifecycle transition | obligation before transition acknowledgement/effectiveness |
| explicit save/session | explicit save uses broad save roots; session/lifecycle reasons should remain distinct |
| catastrophic continuity | reason-specific obligation; avoid vague “importance” classifier |
| verified destructive context loss | controlled handoff obligation from 5.4 |
| one-hour ceiling | replace with configured/owned SOFT exposure policy; numerical one hour not inherited |
| multiplayer/live/access | stronger domain-specific barrier edge, exact rules later 5.8 |

“Meaningful action,” dirty count, ordinary quest/NPC/item/resource changes and generic scene completion remain non-reasons by themselves.

---

# 14. Closure scope examples

## E1 — ordinary item acquisition in singleplayer

Item ownership change becomes ESTABLISHED + VOLATILE_DIRTY + MAY_DEFER => SOFT.

No Git transaction solely for the acquisition.

## E2 — later focal-location boundary references the new item only incidentally

If recovery of location boundary does not depend on the item's unpublished state and native records/scopes are independent, item may remain SOFT under obligation-rooted closure.

If the same owner record/scene snapshot co-owns the item state or the new location state directly references the item's changed placement, the item joins closure.

## E3 — new NPC ID referenced by durable thread

Thread cannot publish a durable reference while NPC owner/index remain volatile. NPC record/index joins closure.

## E4 — active Continuation at explicit save

Save roots include current operational state; Continuation, Resolution/Command/Procedure dependencies, fixed RNG and interpretation context required for recovery join closure.

Save does not force the mechanic to resolve.

## E5 — old dirty scene A; independent narrow access boundary in scene B

If A and B are genuinely independent writable/recovery scopes, B may satisfy its obligation without flushing A.

Explicit campaign save would include both if both belong to selected save scope.

## E6 — exposure ceiling for scene A

A's elapsed dirty exposure creates obligation before next ordinary extension of A/applicable singleplayer scope. An unrelated fresh scope B publication cannot reset A's age.

## E7 — save with lagging Story projection

If canonical gameplay state/recovery is complete and Story is merely lagging noncanonical projection, save may succeed. Step 5.10 later catches Story up.

## E8 — save with irreducible accepted player wording

If an accepted Interaction's exact message content is still required to preserve unmaterialized meaning, save cannot claim recovery completeness unless that evidence is recoverable or typed meaning is materialized first.

---

# 15. Alternatives for the top-level model

## Alternative 1 — KEEP CURRENT STATIC EPHEMERAL/SOFT/HARD LABELS

Treat each fact/commitment as one class.

### Advantages

Minimal terminology change; current runtime prose mostly survives.

### Problems

- HARD examples are actually different barrier reasons;
- the same ordinary fact is SOFT until a later boundary needs it;
- unclear whether HARD blocks narration, next turn, handoff, authority or only save acknowledgement;
- encourages per-fact classification rather than dependency closure;
- mixes semantic importance with storage timing.

Assessment: **not recommended**.

## Alternative 2 — THREE AXES + HARD AS EDGE OBLIGATION — RECOMMENDED

Separate semantic survival, current durability status and outstanding durability obligation.

Retain SOFT/HARD as convenient shorthand, not primary ontology.

### Advantages

- matches actual runtime behavior;
- supports reason-specific blocking;
- cleanly composes with 5.4 and 5.8;
- preserves sparse singleplayer;
- avoids permanent arbitrary fact classes;
- makes failure semantics explicit.

### Cost

Requires runtime documentation/tests to update terminology and guard reasoning.

## Alternative 3 — REMOVE SOFT/HARD TERMS ENTIRELY

Use only `EPHEMERAL/ESTABLISHED`, `DURABLE/VOLATILE`, `MAY_DEFER/MUST_DURABLE_BEFORE(edge)`.

### Advantages

Most semantically precise; no legacy ambiguity.

### Problems

SOFT/HARD are useful compact operational vocabulary already widespread in docs/tests and understood by the project. Removing them provides little additional correctness if their meanings are sharply narrowed.

Assessment: **technically clean but unnecessary churn**.

Recommendation: Alternative 2.

---

# 16. Strongest counterarguments to the recommendation

## Counterargument A — selective closure is too complex; just flush everything

In pure singleplayer the extra Git transaction size may be acceptable and global flush is easier to reason about.

Response:

Step 5.2 already requires partitionability for multiplayer/live/recovery owners. Making ordinary HARD globally flush all dirty state would silently create cross-scope coupling that later 5.8 must undo. The dependency planner is required anyway to prove reference/recovery completeness. Singleplayer implementation may conservatively broaden a selected closure, but architecture should not require global coupling.

## Counterargument B — explicit save should be identical to handoff

Both aim to make state recoverable.

Response:

They share closure mechanics but not necessarily root selection. A handoff promises the affected handoff scope; save intentionally asks to persist all established dirty state in the selected save scope. In ordinary singleplayer these frequently coincide, but making them definitionally identical constrains multiplayer/partitioned future semantics unnecessarily.

## Counterargument C — failed save should always block gameplay

This is safer and avoids silently increasing unsaved exposure.

Response:

It is a defensible product policy, but it can turn a transient Git outage into a singleplayer gameplay lock although the current host still owns coherent HOT state. The engine can preserve honesty by refusing `saved`, maintaining the dirty state and requiring explicit user cancellation/continuation acknowledgement. This remains a human product decision.

## Counterargument D — one global dirty_since is enough

Singleplayer normally has one campaign branch and one runtime.

Response:

A conservative global bucket may be a valid implementation profile, but architecture must not let unrelated publication reset dirty state it did not include. Native ownership is already partitioned by 5.2 and live mode. Per-scope semantics avoid later contradiction while allowing a simpler aggregate implementation where safe.

---

# 17. Preliminary recommendation

Recommend the following Step-5.5 direction:

> **EDGE-OBLIGATION / RECOVERY-CLOSURE DURABILITY**

Core form:

```text
EPHEMERAL vs ESTABLISHED          semantic survival axis
DURABLE vs VOLATILE_DIRTY         current storage/recovery status axis
MAY_DEFER vs MUST_DURABLE_BEFORE  durability-obligation axis

SOFT = ESTABLISHED + VOLATILE_DIRTY + MAY_DEFER
HARD = outstanding MUST_DURABLE_BEFORE(edge) obligation

ordinary HARD closure
    = obligation roots
      + transitive required recovery/reference/ownership dependencies

explicit SAVE closure
    = all established dirty roots in selected save scope
      + transitive required dependencies

SOFT exposure
    = age of actual unpublished established state
      not age of arbitrary last commit
```

Advisory host capacity remains non-HARD by itself.

No numeric exposure threshold is selected by this research.

---

# 18. Questions that still require analytical challenge

Before a decision brief, explicitly challenge:

1. whether retaining `SOFT/HARD` shorthand adds more ambiguity than value;
2. whether obligation-rooted closure can leave an unrelated dirty fact volatile without making the resulting durable user experience surprising;
3. whether explicit save root scope is sufficiently well-defined in singleplayer and future multiplayer;
4. whether plain `save` must block acceptance of the next gameplay input while in flight, or only `SAVE_SUCCESS` acknowledgement;
5. whether failed explicit save may be explicitly abandoned while preserving HOT state;
6. whether a SOFT exposure ceiling is itself non-abandonable once fired;
7. whether exposure should be per native writable scope or per causal dirty closure;
8. whether a conservative singleplayer aggregate exposure bucket is semantically safe;
9. whether any current guard reason genuinely requires narration blocking outside live/shared commit-before-reveal;
10. whether advisory capacity should be permitted to trigger opportunistic publication even when no true HARD obligation exists;
11. whether current focal-location/card forced boundary still belongs in the future architecture or is legacy product policy that should be revisited later during realization;
12. whether explicit save should guarantee canonical gameplay only or also current noncanonical Story/read-model freshness.

---

# 19. Expected later-slice requirements

## Step 5.6 — Campaign publication & crash consistency

Must accept a frozen semantic durability closure and make the authoritative outcome decidable across tree/commit/ref/acknowledgement failure windows.

It must preserve closure identity/completeness across retry without treating an attempted write as durable.

## Step 5.7 — Checkpoint/recovery protocol

Must hydrate/select compatible native sources satisfying required closure without equating save with checkpoint.

## Step 5.8 — Multiplayer/live ownership

Must map shared/live publication reasons onto barrier edges and define save/handoff scope under current live ownership. It may impose stricter before-reveal/visibility obligations.

## Step 5.10 — Story projection durability

Must allow noncanonical Story to lag/catch up without blocking canonical save unless a specific retained source dependency requires it.

## Step 5.11 — Transcript retention

Must retain literal wording only when still required as irreducible evidence; save cannot depend on generic chat memory.

## Step 5.12 — Host delivery

Must define emission/acknowledgement for narration/warnings separately. Step 5.5 only identifies durability barrier edges such as before shared reveal or before save-success acknowledgement.

---

# 20. Runtime/machine realization debt already visible

If the recommended direction is later approved, integrated implementation must revisit at minimum:

- `GAME/CORE/RUNTIME.md` — redefine HARD as an obligation/barrier, not a permanent state class;
- `GAME/CORE/DURABILITY_GUARD.md` — replace one-hour/durable-frontier formula with approved exposure semantics and reason-specific barrier behavior;
- `GAME/CORE/SAVE_CONTRACT.md` — align `SAVE_ALL_DIRTY` with all established dirty roots + recovery closure, including operational owners;
- `GAME/CORE/STORAGE.md` / `SESSION.md` / `PERSISTENCE.md` — remove global durable-frontier-time assumptions and duplicate timer policy;
- `DEV/TESTS/test_hourly_durability_contract.py` — replace literal one-hour formula assertions;
- `DEV/TESTS/DURABILITY_BOUNDARY_CASES.md` — reconcile D20 fixed-timer prohibition with bounded exposure policy;
- `DEV/TESTS/EXPLICIT_SAVE_CASES.md` — add operational/Continuation/RNG/recovery-closure cases;
- `DEV/TESTS/PERSISTENCE_TRANSACTION_CASES.md` — express HARD completeness as frozen recovery closure rather than just multi-record coherence;
- tests for unrelated dirty scopes, partial publication, exposure reset, no-background opportunity, failed save cancellation and advisory host-capacity cases.

No runtime/machine changes are made by this research.

---

# 21. Research self-review

Self-review status: **READY FOR ANALYTICAL CHALLENGE**.

The recommendation preserves explicit user save semantics, sparse singleplayer performance and closed Step-5.2–5.4 recovery laws without introducing a snapshot, generic dirty ledger, global save frontier or background scheduler.

The main unresolved owner-level issue is not mechanical completeness. It is product behavior after an explicit save fails while coherent HOT state still survives: whether ordinary play may resume only after explicit cancellation/acknowledgement of unsaved risk, or whether save failure remains a hard gameplay block until durability succeeds.