# Step 5.7 — Checkpoint / Recovery Protocol — Adversarial Review

Status: **ADVERSARIAL REVIEW — CANDIDATE CHALLENGED**

Date: 2026-08-20

Candidate under review:

`2026-08-20-step-5-7-checkpoint-recovery-protocol-candidate-spec.md`

Candidate direction:

> **CURRENT-AUTHORITY-FIRST / CHECKPOINT-OPTIONAL NATIVE-ROUTED BOUNDED RECOVERY**

## 1. Review standard

This review attempts to falsify the candidate by constructing cases where it could:

- release a stale or split recovery composition as current;
- convert checkpoint convenience metadata into hidden state authority;
- lose or duplicate active operational work;
- confuse source movement with corruption;
- make historical evidence silently override current authority;
- create an impossible race-free guarantee without an owning fence;
- over-constrain Step 5.8 live ownership;
- create unnecessary checkpoint churn;
- require broad scans or universal frontiers;
- weaken Step-5.6 publication/crash semantics;
- invent recovery from evidence that was never durably promised.

Findings are classified:

```text
BLOCKER
SIGNIFICANT
MINOR
NO ISSUE
```

A candidate may canonicalize only after all BLOCKER/SIGNIFICANT findings are resolved or explicitly deferred to the correct later owner without leaving a semantic hole.

---

# 2. Finding A — final currentness check cannot make a recovered basis permanently current

Severity: **SIGNIFICANT**

## Attack

Candidate LAW 5.7-24/27 says writable/current resume release requires currentness validation. But any mutable ref can move immediately after the final check:

```text
check campaign/live/current routing
    -> all unchanged
    -> return READY
    -> another writer advances source
    -> recovered host mutates based on now-stale basis
```

Without a lock/fence, no finite read-based validation can guarantee that the basis remains current after the check.

If candidate implicitly claims `READY` confers mutation authority, it is unsound.

## Resolution

Refine `READY` semantics:

> `READY` means the runtime proved a coherent recoverable basis at the recovery gate. It does not bypass the normal optimistic-concurrency/current-ownership preconditions of the next operation.

Consequences:

- every subsequent campaign mutation still uses Step-5.6 pinned-parent/non-force CAS;
- every subsequent live mutation still uses the Step-5.8 owning CAS/fencing contract;
- ordinary runtime refresh/currentness rules continue after recovery;
- if authority moves after the recovery gate but before a mutation, the mutation fails/revalidates rather than writing stale state;
- 5.7 does not promise a magical post-recovery global lease.

For player-visible narration/read decisions, the host should use the recovered validated basis under the normal currentness/ownership freshness contract for that scope; Step 5.8 owns stronger shared-live semantics.

**Required canonical refinement:** define `READY` as validated recovery basis, not perpetual currentness or mutation lease.

---

# 3. Finding B — root routing can move after owner hydration

Severity: **SIGNIFICANT**

## Attack

Recovery may:

1. load root-routing set R containing Procedure P;
2. hydrate P;
3. another valid transaction terminates P and removes it from routing;
4. recovery validates only source refs, not root-routing membership generation;
5. old P is resumed as active.

Inverse case:

1. R lacks new Command C;
2. another transaction establishes C and enrolls it;
3. recovery releases without seeing C;
4. mandatory work is omitted.

## Existing protection

Step 5.2 already requires root enrollment change to join the owning lifecycle durability closure and requires routing to be partitionable by native scope.

## Resolution

Canonical 5.7 must state explicitly:

- recovery pins/observes the routing/lifecycle basis for each participating native partition;
- final validation proves that the root-membership basis used to enumerate recovery roots is still valid for the recovered attempt;
- owner lifecycle and root enrollment are validated together;
- route/lifecycle inconsistency is not resolved by trusting checkpoint;
- legitimate movement => RETRY;
- persisted mismatch at one pinned current source => integrity suspicion for affected scope.

No new global routing generation is required. Exact representation is machine-realization detail owned by Step-5.2 implementation.

**Required canonical refinement:** root-membership basis is part of the final recovery validation footprint.

---

# 4. Finding C — active Procedure machine schema cannot currently prove lifecycle

Severity: **SIGNIFICANT IMPLEMENTATION DEBT, NOT ARCHITECTURE BLOCKER**

## Attack

Step 5.2 says active Procedure may independently require root discoverability, but current `runtime-procedure-state.schema.json` owns resources/world context only. There is no explicit lifecycle/status field sufficient for recovery to determine active/closed membership from the Procedure payload itself.

A candidate that says “validate owner lifecycle” without machine support is not implemented.

## Resolution

Architecture is already clear: lifecycle/root-membership contract must exist in native machine realization; checkpoint must not become substitute lifecycle authority.

Record implementation obligation:

- add/derive explicit deterministic Procedure lifecycle evidence sufficient for root enrollment validation;
- atomically couple Procedure activation/termination with routing enrollment/removal under its native transaction boundary;
- regress active Procedure with no Command and terminated Procedure stale-routing cases.

No owner-level semantic choice is required here.

---

# 5. Finding D — campaign ref movement after pin could be disjoint

Severity: **MINOR / PERFORMANCE**

## Attack

Candidate conservatively retries if campaign ref H changes before READY even when H2 changes only unrelated Story or another independent scope. This may increase cold-start contention.

## Resolution

Keep conservative default. Cold recovery is relatively infrequent and correctness dominates. Step-5.6 already has dependency-overlap machinery that can inspire a later optimization.

Canonical language should permit but not require proven-disjoint reuse:

```text
if campaign anchor moved:
    default -> repin/re-resolve
    optional optimization -> retain unaffected hydrated data only when bounded proof shows its authority/dependency basis remains valid
```

Do not introduce a second overlap engine just for 5.7.

No blocker.

---

# 6. Finding E — active live source movement can make recovery retry forever

Severity: **SIGNIFICANT BUT CORRECTLY DEFERRED**

## Attack

A busy live scene may advance continuously. Exact-pin + recheck may repeatedly return RETRY.

## Resolution

5.7 cannot solve live stabilization without owning Step-5.8 semantics. It should require only:

- no stale release when current live owning contract says basis is invalid;
- bounded retries;
- typed coordination/stabilization requirement after retry exhaustion;
- no corruption classification solely due to movement.

Step 5.8 must provide the live-specific adopt/fence/epoch protocol that makes recovery practical under active concurrency.

**Carry-forward to 5.8:** explicitly test cold host adoption while another live writer is active.

No 5.7 blocker if this dependency is explicit.

---

# 7. Finding F — checkpoint-first repair temptation can become silent rollback

Severity: **SIGNIFICANT**

## Attack

Suppose current campaign routing is malformed. A checkpoint K from five commits ago names a coherent scene/source composition. An implementation may be tempted to “recover” by loading K and proceeding.

This creates hidden rollback and violates current authority.

## Resolution

Canonical distinction must be hard:

```text
ordinary recovery:
    current authority defect -> BLOCKED + integrity workflow

bounded repair:
    checkpoint/history may be evidence
    -> diagnose
    -> human/authorized deterministic repair decision where required
    -> forward corrective publication
    -> ordinary recovery again
```

Checkpoint evidence may bootstrap *diagnosis*, not silently bootstrap current gameplay authority.

No direct state adoption from checkpoint without explicit historical maintenance/repair semantics.

**Required canonical refinement:** repair evidence does not constitute fallback current source.

---

# 8. Finding G — optional checkpoint corruption can still be a dangling MANIFEST reference

Severity: **SIGNIFICANT CLARIFICATION**

## Attack

Candidate says malformed/missing optional checkpoint does not block gameplay if RRC is independently valid. But MANIFEST may contain `last_checkpoint_id` pointing to nothing. Existing integrity rules normally flag required dangling references.

Could this make the whole campaign `CANON_SUSPECT`, thereby indirectly blocking play?

## Resolution

Scope the reference semantics.

If `last_checkpoint_id` is retained as optional checkpoint-facility metadata, its target requirement belongs to that metadata facility. A dangling pointer yields:

```text
checkpoint metadata scope = CANON_SUSPECT
operations that require that checkpoint = BLOCKED
current gameplay scopes = may remain CANON_OK / recovery READY
```

Do not make `last_checkpoint_id` a globally required gameplay reference.

Machine schema/docs must encode optionality clearly enough that generic integrity tooling does not treat it as current-state dependency.

**Required canonical refinement:** pointer integrity is facility-scoped.

---

# 9. Finding H — checkpoint creation on clean state could become repository churn

Severity: **SIGNIFICANT POLICY BOUNDARY**

## Attack

LAW 5.7-39 allows metadata-only checkpoint publication on already durable state. A policy could then create one every session/hour/turn, effectively reintroducing heartbeat/no-op garbage under another name.

## Resolution

Require an independent **semantic/operational checkpoint reason**, not mere freshness:

Valid classes may include:

- explicit support/export/historical landmark request;
- complex suspension or controlled handoff where descriptor provides measurable recovery value;
- migration/repair boundary;
- a future configured event-driven checkpoint policy tied to meaningful recovery structure change.

Invalid sole reasons:

- elapsed time;
- checkpoint age;
- “keep latest pointer fresh”;
- session count;
- empty save;
- heartbeat/capacity bookkeeping with no changed recovery evidence.

Architecture need not enumerate every future valid reason, but must forbid age/freshness-only creation.

If implementation cannot articulate what new durable recovery evidence the descriptor adds, skip the write.

**Required canonical refinement:** metadata-only checkpoint must carry independently justified new recovery/maintenance evidence/value.

---

# 10. Finding I — `last_checkpoint_id` update can select a descriptor with no incremental value

Severity: **MINOR after Finding H**

## Attack

Even if a descriptor exists, pointer movement alone could churn.

## Resolution

No pointer-only freshness update. Pointer changes only in a real campaign transaction selecting a materially new checkpoint descriptor or correcting checkpoint metadata under explicit repair.

Checkpoint file and selection pointer are same campaign transaction when created together.

---

# 11. Finding J — retiring `expected_commit_sha` loses exact creation provenance

Severity: **MINOR / ACCEPTED TRADE-OFF**

## Attack

Historical support might want to know which commit first introduced K.

## Resolution

Ordinary recovery does not need this information. Historical/repair tooling can obtain it from bounded path history when necessary.

Alternatives to self-reference include:

- repository object context where K is currently read;
- introduction-commit lookup by path/history;
- non-self-referential observed source revisions stored in K.

Creating a follow-up commit solely to backfill K's containing SHA is worse: it adds noise, destroys single-transaction simplicity and immediately changes containing SHA again.

Retirement stands.

---

# 12. Finding K — checkpoint observed source SHAs might themselves become a universal recovery cut

Severity: **SIGNIFICANT**

## Attack

Candidate allows “observed domain-typed source hints.” If implementation records campaign H + every live source + every runtime partition revision, checkpoint effectively becomes a serialized RecoveryCut even if called a hint.

## Resolution

Do not require complete source enumeration.

Checkpoint fields must be justified individually by recovery/diagnostic value. A checkpoint SHALL NOT claim that its source-hint set is complete for RRC unless a future specifically typed maintenance contract defines such a historical descriptor and accepts retention costs.

Ordinary checkpoint semantics:

- zero or more hints;
- each hint domain typed;
- hint-set incompleteness allowed;
- current native routing remains membership authority;
- no cross-domain “valid through” claim.

**Required canonical refinement:** source-hint collection is explicitly non-exhaustive by default.

---

# 13. Finding L — source compatibility proof can become a hidden universal predicate

Severity: **SIGNIFICANT CLARIFICATION**

## Attack

“Compatible composition” can tempt implementation to invent one global `is_compatible(campaign, live, runtime, chronology...)` predicate or scalar recovery generation.

## Resolution

RRC compatibility is the conjunction of owning contracts needed by the particular closure:

```text
campaign routing relation
live ownership/source relation
execution accepted interpretation compatibility
reference/revision validity
root/lifecycle consistency
other explicit owner-specific dependencies
```

No universal cross-domain comparison primitive or global compatibility frontier is introduced.

Recovery engine may orchestrate these checks but does not own their semantics.

**Required canonical refinement:** compatibility checks remain owner/domain-native predicates composed by recovery.

---

# 14. Finding M — checkpoint “engine” provenance could override open execution context

Severity: **SIGNIFICANT but candidate already mostly handles it**

## Attack

Campaign has current runtime R2. Checkpoint K says R1. Suspended Resolution was accepted under compatible R1 context and must resume under pinned interpretation. An implementation might either downgrade whole campaign to R1 because of K or reinterpret Resolution under R2.

## Resolution

Three separate facts:

1. current campaign accepted runtime identity at current campaign authority;
2. checkpoint observed runtime provenance — advisory only;
3. open execution's accepted interpretation context — native execution dependency and correctness-critical.

Recovery validates the open execution's accepted context through Step-3/5.2 contracts. Checkpoint cannot choose it.

No issue after canonical emphasis.

---

# 15. Finding N — exact accepted text may be removed by transcript compaction later

Severity: **SIGNIFICANT CROSS-SLICE CONSTRAINT**

## Attack

5.11 might delete exact transcript text that remains irreducible accepted recovery evidence for unresolved Interaction/IntentPlan. Then 5.7 cannot recover.

## Resolution

Carry forward binding constraint to 5.11:

> exact wording/evidence that is still a required Step-5.2 recovery dependency is not eligible for transcript deletion merely because general transcript retention expires.

It may be replaced only when an owning typed state/evidence artifact renders it no longer semantically required.

Checkpoint summary cannot substitute.

No 5.7 blocker.

---

# 16. Finding O — duplicate temporal root plus reachability from Command may double execute

Severity: **SIGNIFICANT VALIDATION CASE**

## Attack

Step 5.2 deliberately roots every armed independently-due temporal owner even if another active root also reaches it. Recovery could hydrate it twice and arm two agenda entries/firings.

## Resolution

Routing duplication is identity/reference duplication only.

Recovery and derived Temporal Agenda rebuild must deduplicate by native owner/binding/occurrence identities according to Step 5.2/5.3. Multiple discovery paths cannot create multiple owners or occurrences.

Candidate failure matrix already mentions deduplication, but canonical spec should make this explicit.

**Required canonical refinement:** discovery-path multiplicity never multiplies semantic owner/obligation identity.

---

# 17. Finding P — current root routing itself may be incomplete but internally well-formed

Severity: **SIGNIFICANT INTEGRITY LIMIT**

## Attack

Suppose an active Procedure exists durably, but due to a prior bug it was never enrolled in routing. Routing itself is syntactically valid and no pointer is dangling. Cold recovery cannot discover P, so RRC falsely appears complete.

## Resolution

This is why Step 5.2 makes owner lifecycle ↔ root enrollment a correctness invariant, not mere routing syntax.

Recovery final validation must include bounded lifecycle-membership consistency for the native scope, using whatever native indexes/lifecycle evidence machine realization provides.

It cannot discover arbitrary omitted owners by campaign-wide scan on every cold start. Therefore:

- implementation must ensure lifecycle transaction makes omission impossible in healthy writes;
- targeted integrity/audit tests detect representative omissions;
- if independent evidence later exposes omitted P, scope becomes suspect and repair is required;
- no checkpoint can guarantee against arbitrary latent omitted roots unless it duplicates all authority, which is rejected.

This is an unavoidable trust boundary of the native persistence invariants, analogous to index consistency elsewhere.

**Required machine realization:** atomic owner lifecycle + routing updates and integrity regressions.

---

# 18. Finding Q — checkpoint optionality may make checkpoint product surface pointless

Severity: **MINOR / YAGNI REVIEW**

## Attack

If healthy ordinary recovery never needs checkpoint, why retain CHECKPOINTS at all?

## Resolution

The architecture intentionally leaves checkpoint optional because existing support/maintenance/migration/suspension use cases may still justify it. But it does not protect the feature from deletion for legacy reasons.

Canonical recommendation should include explicit revisit trigger:

> If implementation/evaluation shows no material diagnostic, maintenance, historical or bounded-recovery benefit, remove checkpoint from ordinary product surface rather than expanding its schema.

No correctness dependency prevents future removal.

---

# 19. Finding R — checkpoint creation during controlled handoff can be mistaken for handoff success evidence

Severity: **SIGNIFICANT**

## Attack

Host creates checkpoint K but another required source is not durable. If UI sees K, it may acknowledge safe handoff.

## Resolution

Step 5.4/5.5 remain controlling:

- checkpoint existence never proves handoff RRC;
- controlled handoff acknowledges only after complete promised native durable closure is actually durable/compatible;
- K is auxiliary evidence only.

Canonical 5.7 should state checkpoint publication cannot promote a failed/incomplete handoff to success.

---

# 20. Finding S — partial multi-domain publication and current routing may temporarily disagree

Severity: **SIGNIFICANT, OWNED AT 5.8 WHERE LIVE TRANSFER INVOLVED**

## Attack

Domain A publishes, B fails. Campaign route may say one owner while another domain contains newer state. Which is current?

## Resolution

5.7 cannot use “newer data exists” to select authority. It follows owning-scope routing/transfer semantics.

Step 5.5 says successful A publication remains real; Step 5.8 must define transition states so authority is never ambiguous/split during campaign/live transfer.

5.7 behavior:

- inspect actual current routing/owners;
- if owning contract yields a valid source, pin it;
- if transfer state is incomplete/indeterminate under owning contract, BLOCKED/RETRY rather than guess;
- never choose by checkpoint age or commit time.

**Carry-forward to 5.8:** exact partial compaction/route-update crash windows must make source selection decidable.

---

# 21. Finding T — authorization can change during recovery

Severity: **SIGNIFICANT**

## Attack

User is authorized when campaign is selected but loses membership/write authority before READY. Recovery may expose or mutate state improperly.

## Resolution

Separate repository read capability from gameplay/application authorization, consistent with 5.6.

Recovery must validate required authorization at the relevant stage:

- read/disclosure eligibility for loaded material;
- writable/adoption permission before enabling writes;
- subsequent mutation still checks normal current authorization/CAS.

Authorization movement may produce BLOCKED/RETRY without canon corruption.

Exact multiplayer membership semantics belong 5.8/access-control owners.

**Required canonical refinement:** authorization is part of recovery release prerequisites where relevant, but repository credentials are not gameplay authority.

---

# 22. Finding U — optional checkpoint can leak secrets if support/export uses broad payload

Severity: **MINOR / SECURITY BOUNDARY**

## Attack

Checkpoint diagnostic notes/source hints could include secret world information and be surfaced to a player/support export outside disclosure eligibility.

## Resolution

Checkpoint storage/access follows campaign repository authorization; human-visible export additionally follows existing disclosure/access policy. Recovery metadata does not bypass Step-4 knowledge/disclosure boundaries.

Do not store raw hidden LLM reasoning/prompt context in checkpoint.

No new security owner needed.

---

# 23. Finding V — `READY` for read-only observer and `READY` for writable host differ

Severity: **SIGNIFICANT CLARIFICATION**

## Attack

Observer may be able to hydrate a coherent view but lacks mutation authority. One `READY` status could imply write readiness.

## Resolution

Recovery readiness should be parameterized by requested capability/operation scope, or report validated basis plus authorized capabilities.

Simplest architecture:

```text
READY
    = requested recovery/read basis is valid

write enablement
    = separate authorization + owning mutation contract
```

Do not overload recovery disposition with role permissions.

For host resumption that requires mutation, authorization is an additional release prerequisite.

Canonical spec should avoid saying `READY` means “writable lease”.

---

# 24. Finding W — checkpoint path/history retention may be lost after GC

Severity: **NO ISSUE if guarantee stays conditional**

Historical checkpoint support is explicitly conditional on retained exact dependencies. Step 5.13 owns physical deletion; a product guarantee for rewind would need retention policy. Current candidate correctly avoids such promise.

---

# 25. Finding X — malformed checkpoint pointer can trigger repeated startup warnings forever

Severity: **MINOR UX/REPAIR**

If ordinary recovery ignores checkpoint but flags metadata suspect each startup, users may see repetitive warning noise.

Resolution belongs to later UX/repair policy. Architecture only requires:

- suspicion remains truthful;
- dependent checkpoint operation blocked;
- independent gameplay may proceed;
- repair can clear pointer/metadata through forward publication.

No blocker.

---

# 26. Finding Y — checkpoint schema minimum may be even smaller than candidate suggests

Severity: **MINOR / YAGNI**

Minimum immutable descriptor could be only:

```text
schema version
checkpoint identity
campaign identity
created metadata/reason
optional typed evidence
```

No state block is necessarily required.

Resolution: canonical spec should define semantics, not prematurely freeze a replacement schema. Machine planning can decide whether legacy `state:` nesting survives.

---

# 27. Finding Z — recovery result evidence itself could become persisted authority

Severity: **SIGNIFICANT CLARIFICATION**

`selected_source_evidence` in an in-memory result could later be serialized and treated as new recovery cut.

Resolution:

- RecoveryResult is operational result/diagnostic evidence, not authority;
- no persistence required by 5.7;
- if diagnostics are logged, native source identities remain references to authorities, not a new current-state owner;
- no future read may prefer old RecoveryResult over current routing.

Canonicalize this explicitly.

---

# 28. Finding AA — exact source read can fail transiently after pin

Severity: **NO ISSUE with typed retry/block semantics**

Repository/network unavailable after pin is operational unavailability, not canon corruption absent evidence of missing persisted object. Recovery can retry/block. If an exact object that current authoritative ref necessarily references is confirmed missing/corrupt, integrity escalates.

---

# 29. Finding AB — current campaign ref itself may be inaccessible or deleted

Severity: **SIGNIFICANT BOUNDARY**

If selected campaign branch/ref is missing, ordinary recovery has no current campaign anchor.

Do not silently choose a checkpoint/historical branch. Classify as BLOCKED / current source unavailable or integrity/storage defect depending evidence. Bounded repair/discovery may use campaign card/history/checkpoints only under explicit repair semantics.

No invented “most recent commit”.

---

# 30. Finding AC — bootstrap might read checkpoint before runtime identity for optimization

Severity: **MINOR**

Reading checkpoint bytes early is not itself authority violation, but parsing/version semantics may require runtime/schema compatibility.

Safer default remains current campaign identity/runtime/routing first. Implementations may fetch immutable checkpoint concurrently/early only if they do not trust/interpret it before required schema/identity validation.

No architecture need for speculative parallelism.

---

# 31. Finding AD — no-checkpoint recovery can increase GitHub calls under current slow connector

Severity: **PERFORMANCE, NOT ARCHITECTURE BLOCKER**

Current ChatGPT connector latency makes additional reads expensive. This is real but cannot justify unsafe checkpoint authority.

Possible later optimizations:

- compact native routing manifests;
- Python RepositoryPort batched reads;
- verified checkpoint hints after measurement;
- external deterministic bridge.

Step-6 RepositoryPort feasibility owns physical transport; 5.7 keeps bounded semantic reads.

---

# 32. Finding AE — checkpoint selected in same commit cannot know its own containing commit, but pointer can

Severity: **NO ISSUE**

The pointer and checkpoint exist atomically in resulting tree. Repository read of current H establishes that K exists at H. K need not embed H.

Historical creation provenance can be looked up separately.

---

# 33. Finding AF — source hint can refer to a commit that later becomes unreachable

Severity: **NO ISSUE**

Hints are non-authoritative. If explicit historical maintenance needs that exact source and it is unavailable, maintenance fails. Ordinary current recovery ignores stale/unresolvable hint.

---

# 34. Finding AG — checkpoint notes may contain unverifiable free text

Severity: **MINOR**

`recovery_notes` are diagnostic text only. They never establish state/routing/compatibility. Machine recovery decisions use typed evidence/native sources.

---

# 35. Finding AH — current campaign HEAD plus routing may be coherent but accepted open execution belongs to older source revision

Severity: **SIGNIFICANT and already inherited from 5.2**

Open execution may retain dependency refs/accepted catalog context pinned to an earlier compatible basis. Recovery must distinguish:

- current owner/source selection for mutable current state;
- exact historical/accepted inputs that the execution owner legitimately retains as causal evidence.

Owning execution contract decides whether those refs are still valid/recoverable. Do not overwrite them with current ambient values merely because campaign HEAD advanced.

Canonical 5.7 should emphasize that “current-authority-first” does not mean “replace every accepted historical execution input with current values.”

---

# 36. Finding AI — recovery of settled Command records may be unnecessary

Severity: **NO ISSUE**

Step 5.2 routes non-settled Commands only unless another active dependency requires settled evidence. Transitive closure can load settled receipts/events when explicitly needed. No scan of all historical Commands.

---

# 37. Finding AJ — checkpoint could be used as a trusted negative (“no active roots”)

Severity: **SIGNIFICANT**

An empty checkpoint root list could cause runtime to skip native routing checks.

Resolution:

- checkpoint hint absence is never proof of absence;
- negative/current membership claims come only from current native routing/lifecycle under owning contract;
- checkpoint may suggest positive candidates but cannot prove no additional roots unless a future specifically versioned domain-native completeness contract exists, at which point that contract—not generic checkpoint—owns the proof.

**Required canonical refinement:** checkpoint has no default negative/completeness authority.

---

# 38. Finding AK — root routing corruption and no checkpoint may make recovery impossible

Severity: **ACCEPTED**

No persistence design can guarantee automatic recovery from every corruption without duplicating all state. Architecture chooses single authority + repair evidence over duplicated snapshots.

Git history/checkpoints/events can support bounded repair, but automatic ordinary recovery must fail safely rather than invent.

---

# 39. Finding AL — `created_at` checkpoint metadata could accidentally order checkpoints across domains

Severity: **MINOR**

Created time is diagnostic only. `last_checkpoint_id` selection is campaign-domain publication state, not “max created_at”. No cross-domain comparison follows from timestamp.

---

# 40. Finding AM — historical rollback with forward corrective publication may create semantic discontinuity

Severity: **OWNER-LEVEL IF PRODUCT FEATURE EXISTS, CURRENTLY NOT BLOCKING**

A true player-facing rewind would need explicit semantics for:

- what later events are superseded;
- multiplayer disclosure/knowledge consequences;
- chronology/history retention;
- whether rewound facts remain known to players;
- Story/transcript handling.

This confirms why guaranteed rewind is not a small checkpoint mechanism and must not be silently promised by 5.7.

Current maintenance proposal does not establish a product rewind feature. Therefore no blocker, but any future rewind request requires separate architecture across 5.9–5.12/Step 6.

---

# 41. Required canonical refinements

The candidate direction survives, with these changes required before canonicalization:

1. Define `READY` as a validated recovery basis at the gate, **not** a perpetual currentness guarantee, lock, lease or bypass of next-operation CAS/authorization.
2. Include native root-routing/lifecycle basis in recovery final validation footprint.
3. Explicitly carry Procedure lifecycle/root-enrollment machine debt.
4. Make checkpoint ordinary acceleration optional even as an implementation choice; no read required.
5. Scope checkpoint-pointer integrity defects to checkpoint facility unless another operation depends on them.
6. Require independently justified new recovery/maintenance evidence/value for metadata-only checkpoint creation; freshness/age/time alone forbidden.
7. Make checkpoint source/root hints non-exhaustive by default; no implicit RecoveryCut or negative completeness claim.
8. State compatibility semantics are owner/domain-native predicates orchestrated by recovery, not one universal comparison authority.
9. State duplicate discovery paths deduplicate semantic owners/temporal obligations by stable identity.
10. Make authorization/read/write capability validation explicit without treating repository credential as gameplay authority.
11. Clarify current-authority-first does not overwrite legitimately pinned accepted historical execution inputs.
12. RecoveryResult/evidence remains operational/non-authoritative and does not become persisted recovery cut.
13. Checkpoint publication never proves save/handoff success by itself.
14. Current source missing/route corrupt never silently falls back to checkpoint; checkpoint can assist repair only.
15. Carry to 5.8: live host adoption/stabilization under concurrent writer and partial campaign/live transfer crash windows.
16. Carry to 5.11: irreducible exact accepted evidence is retention-protected while it remains a recovery dependency.

---

# 42. Adversarial verdict

**No architecture blocker remains after the above refinements.**

No new owner decision is required for Step 5.7.

The strongest remaining would-be owner choice—guaranteed player-visible historical rewind—is confirmed to be a separate, materially cross-cutting product feature rather than an implicit checkpoint property. It is not currently promised by canonical gameplay architecture and therefore is not introduced here.

Recommended canonical direction remains:

> **CURRENT-AUTHORITY-FIRST / CHECKPOINT-OPTIONAL NATIVE-ROUTED BOUNDED RECOVERY**

with `READY` explicitly treated as a validated recovery basis and all future mutations still subject to their owning CAS/fencing/authorization contracts.