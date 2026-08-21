# Step 5.2 — Resumable Runtime Closure — Adversarial Review

Status: **ADVERSARIAL REVIEW COMPLETE — SIGNIFICANT FINDINGS RESOLVED**

Date: 2026-08-20

Reviewed candidate:

- `2026-08-20-step-5-2-resumable-runtime-closure-candidate-spec.md`

Review objective:

Attempt to break the candidate under crash, stale-read, multiplayer, cross-domain dependency, temporal-obligation, identity and pending-input scenarios without reopening already accepted owner boundaries unnecessarily.

---

# 1. Verdict

The candidate architecture survives adversarial review.

No finding requires:

- a new semantic recovery authority;
- a first-class `runtime.recovery_closure` record;
- serialized Temporal Agenda;
- changing Procedure/Resolution/Continuation ownership;
- a global recovery frontier;
- a new product-semantic decision from the owner.

The review found **six significant specification refinements** and several minor clarifications. All can be resolved mechanically inside the candidate architecture.

```text
BLOCKING / owner decision required: 0
SIGNIFICANT resolved:               6
MINOR resolved:                     4
```

---

# 2. Significant finding S1 — Hydration can observe mixed native revisions

## Attack

A recovery operation does:

1. read campaign scene pointer at campaign HEAD C;
2. read live branch by relative branch name;
3. live branch advances before dependent runtime owner is loaded;
4. read another live/root file from newer head L2.

The runtime has now assembled one recovered view from incompatible native revisions even though all individual records were valid.

This recreates exactly the mixed-read problem Step 5.1 prohibited.

## Resolution

Add a **PINNED NATIVE SOURCE law**:

> One recovery/hydration attempt SHALL resolve every participating mutable source to an exact native revision before consuming dependent state from that source. Reads for that attempt are pinned to those resolved revisions. If compatibility validation or a required source refresh changes the selected revisions, invalidate/restart the affected hydration selection rather than mixing versions.

This does not create a common frontier or order among source revisions.

Examples:

```text
campaign branch -> exact commit C
live scene A    -> exact live head LA
live scene B    -> exact live head LB
```

LA and LB remain incomparable unless another owner contract relates them.

Exact read/retry protocol remains 5.7/5.8.

Status: **RESOLVED**.

---

# 3. Significant finding S2 — Cross-domain dependency could silently fall back to wrong owner scope

## Attack

A recoverable Procedure/Continuation references entity X.

Campaign branch contains old X state at C, but scene/live routing says X is currently live-owned in epoch L.

A naïve recovery loader resolves ID X from ordinary campaign WORLD and obtains valid but stale state.

No file is missing, so ordinary integrity checks might not detect the semantic ownership violation.

## Resolution

Add **OWNING-SCOPE RESOLUTION law**:

> Required recovery dependencies SHALL resolve through the current native ownership/routing contract for that identity/scope. The presence of an older durable representation in another domain does not authorize fallback when another native owner currently owns mutable truth for that scope.

For live-owned entity/scene state:

```text
campaign representation = base/reference
live epoch              = current operational owner
```

If the routed live owner is unavailable/incompatible, recovery blocks/suspects that scope rather than silently using campaign fallback.

Status: **RESOLVED**.

---

# 4. Significant finding S3 — Root projection can omit an owner with no local evidence of omission

## Attack

A Procedure becomes active but transaction bug fails to enroll it in recovery routing. Cold recovery reads the index, sees nothing, and has no reason to suspect an omitted owner.

“Owner wins over index” is useless if the owner is never discovered.

## Resolution

This cannot be solved by cold-read semantics alone. It requires a **publication completeness invariant**:

> Any durability/publication operation that makes an independently recovery-relevant owner active, changes its recovery-root eligibility, or makes it terminal SHALL include the corresponding routing membership mutation in the same semantic durability closure.

Further:

- owner-kind tests/validators must define root-enrollment obligations;
- 5.6/5.7 publication validation must assert relevant root membership against the dirty owner set before acknowledgement;
- exceptional maintenance audit may perform broader structural checks to detect latent historical drift;
- normal cold recovery still trusts the current routing projection under this invariant.

This is analogous to maintaining a correctness-critical secondary index transactionally.

Status: **RESOLVED**.

---

# 5. Significant finding S4 — Procedure lifetime is accepted, but current machine state has no lifecycle/status

## Attack

Candidate says active Procedure must remain rooted independently. Current DEV Procedure schema stores IDs/resources/context but no explicit active/terminal state.

A routing index therefore risks becoming the de facto Procedure lifecycle authority: “listed means active”.

## Resolution

Clarify machine-realization obligation:

> Procedure lifecycle/activity MUST be derivable unambiguously from Procedure-owned state or an accepted Procedure lifecycle contract. Recovery-routing membership SHALL NOT be the sole semantic evidence that a Procedure is active.

Step 5.2 does not decide the final lifecycle field/state machine, but later implementation cannot rely on index presence alone as Procedure semantic lifecycle.

This is a concrete implementation obligation carried into integrated Step-3 realization.

Status: **RESOLVED**.

---

# 6. Significant finding S5 — Temporal-owner routing can accidentally become scheduler state

## Attack

To optimize cold recovery, implementation stores:

```text
owner_id
deadline
next_due
priority
selected_trigger
```

in the temporal-source index.

A later runtime sees an index deadline differing from Effect TemporalBinding and must choose one. Agenda authority has reappeared through the index.

## Resolution

Strengthen recovery-routing field exclusion:

Temporal-source routing MAY contain only data needed to locate/validate the native source, such as:

```text
owner kind
owner ID/reference
owning scope/path/index partition reference if required
```

It SHALL NOT own or be trusted for:

```text
deadline
next_due
priority
due/not-due result
selected trigger
firing generation
chronology ordering
```

If later optimization duplicates such values, that optimization must be explicitly disposable/validated against owner state and cannot participate as required recovery semantics.

Status: **RESOLVED**.

---

# 7. Significant finding S6 — Runtime package/catalog needed by suspended execution may be unavailable

## Attack

Continuation durably stores accepted catalog-context fingerprint and Activity identity. Campaign MANIFEST points to required runtime package identity. New environment lacks that exact compatible runtime/catalog package.

All campaign/runtime owner records are present, but deterministic resume cannot interpret them safely.

## Resolution

Add **INTERPRETABILITY CLOSURE law**:

> A promised recoverable operational owner is resumable only when its accepted rules/catalog/runtime interpretation context is resolvable according to the campaign engine/package compatibility contract. Missing runtime bytes/context are a recovery prerequisite failure, not permission to bind the suspended execution to arbitrary newer ambient rules.

This does not require campaign storage to contain engine bytes.

Existing engine mismatch/update recovery mechanisms provide the package-resolution boundary. Step 6 owns broader migration/catalog-gap closure; Step 5.7 owns hydration validation.

If compatible migration/adoption is required, it must be explicit and cannot silently change an already accepted open Resolution meaning.

Status: **RESOLVED**.

---

# 8. Minor finding M1 — “All active temporal owners” is too broad without due-capable qualification

Some owner-local temporal metadata may be descriptive or only evaluated within an already-rooted Procedure/scene.

Resolution:

Use:

> otherwise-unreachable **armed due-capable temporal source owner**

rather than indexing every record containing any temporal field.

If another guaranteed root already reaches the owner and cold rebuild traverses it boundedly, redundant temporal root membership is unnecessary.

Status: **RESOLVED**.

---

# 9. Minor finding M2 — Resolution may be root-worthy in a future execution path not owned by a Command

Current Step-3 model permits child Resolution causal invocation without an initiating Command field, while root-command/casual closure still exists in accepted execution semantics.

The candidate should not encode a forever-closed root-class list that prevents later justified runtime owners from becoming independent roots.

Resolution:

The current minimum root classes remain, but canonical admission rule is generic:

> Any native operational owner with independently active recoverable lifetime that is not guaranteed reachable from another admitted root must itself become a typed recovery root.

Adding a newly admitted root kind follows normal architecture/catalog evolution; it is not an untyped generic bucket.

Status: **RESOLVED**.

---

# 10. Minor finding M3 — Root routing itself may be corrupted

If root index/file cannot be parsed, normal recovery has no roots.

Resolution:

- malformed required routing evidence blocks normal recovery for its scope;
- enter targeted recovery/integrity mode;
- exceptional repair may reconstruct routing from broader native owner storage/history if evidence permits;
- reconstructed index is a repair projection, never permission to invent missing owner state.

Exact repair tooling belongs to 5.7/maintenance.

Status: **RESOLVED**.

---

# 11. Minor finding M4 — Exact prior player wording vs semantic pending clarification

If pending Interaction semantics are too weakly materialized, regenerated clarification can change meaning.

Resolution:

Step 5.2 requires **sufficient semantic pending-input payload**, not necessarily verbatim transcript.

If exact wording is the only evidence that disambiguates the accepted intent, then that message evidence is temporarily irreducible until interpretation is sufficiently materialized. The runtime may retain `runtime.message`/Interaction evidence for that reason.

This does not make complete transcript universally authoritative.

Status: **RESOLVED**.

---

# 12. Crash-window attacks

## 12.1 Owner created, root not yet published

If neither is acknowledged durable yet:

- crash rolls back to prior durable source set;
- valid under sparse durability.

If owner is published but required root membership is not:

- invalid durability publication under S3 invariant.

Later 5.6 must ensure transaction grouping.

---

## 12.2 Root published before owner

Forbidden by closure completeness.

A promised durable source set with dangling required root is invalid/recovery-blocked.

---

## 12.3 Owner terminal committed, root removal lost

Cold recovery may load a stale listed owner.

Native owner terminal state wins; routing is stale and can be repaired.

No mandatory work is replayed merely because index membership is stale.

This failure is safer than premature root removal.

Later publication should still keep membership coherent.

---

## 12.4 Root removed before mandatory descendants settle

Forbidden.

Command/root terminality or root removal cannot make required descendant closure unreachable.

---

# 13. Multiplayer attacks

## 13.1 Independent scenes both activate Procedures

A required single global root file would conflict.

Candidate partitionability permits independent routing partitions. Pass.

## 13.2 Same entity crosses live scopes

Existing live model forbids concurrent ownership by two epochs and requires freeze/compaction before crossing.

Recovery root movement must follow that same ownership transition; 5.8 owns mechanics. Pass.

## 13.3 Campaign HEAD moves while live recovery hydrates

Pinned-source rule S1 prevents mixed reads. If campaign changes invalidate live pointer/compatibility, recovery reselects/refreshes affected sources rather than mixing. Pass.

## 13.4 One live branch is closed-unabsorbed

Recovery source remains meaningful but ordinary gameplay is blocked for that scope until bounded compaction/recovery proceeds. Candidate permits this. Pass.

---

# 14. Temporal attacks

## 14.1 World time does not advance while chat is absent

Current runtime explicitly has no background execution. Rebuilding Agenda after restart does not by itself advance fictional/world time.

Due evaluation uses recovered chronology/context, not host wall clock unless a specific admitted mechanic explicitly owns such semantics.

Pass.

## 14.2 Effect due candidate selected before crash but child not committed

If selection was only Agenda-local/prospective and not accepted/committed under later 5.3 rules, recovery may rederive selection from owner state.

If selection crossed the committed materialization boundary, stable firing/pending-child identity must survive and Agenda must not select it anew.

5.3 must define exact boundary. Candidate compatible.

## 14.3 Effect terminated while stale temporal index still lists it

Load native Effect, see terminal lifecycle, do not fire; repair index. Pass.

---

# 15. RNG attacks

## 15.1 RNG value drawn, narrated, owner state not durably saved

If narration occurred while value/result remained only SOFT and no durability promise fired, total process loss may roll back to prior durable basis under existing policy. The engine must not pretend the narrated result survived cold recovery.

If a boundary promised that point, fixed RNG and dependent owner state must be durable before acknowledgement.

This exposes a user-experience/RPO issue for later 5.4/5.5, not a 5.2 ownership flaw.

## 15.2 Stale live write conflict after RNG

Existing live contract reuses raw random result if same random experiment still applies; obtains new randomness only if experiment no longer corresponds.

Recovered fixed RNG semantics remain compatible. Pass.

---

# 16. Interaction attacks

## 16.1 Player said ambiguous action, clarification sent, process lost

If no durability/handoff boundary promised this pending input, rollback may lose it under sparse policy.

If controlled handoff/save promised resume, Interaction/IntentPlan plus sufficient message evidence must be durable/rooted.

5.4/5.5 decide when promise applies. Pass.

## 16.2 Master generated multiple-choice options that were only suggestions

No durable Choice owner unless those options became a mechanically/semantically fixed bounded response contract.

Do not persist arbitrary generated UI as recovery authority. Pass.

---

# 17. Checkpoint attacks

## 17.1 Latest checkpoint references historical root set, current campaign moved on

Current recovery uses current durable routing/source selection. Historical checkpoint hydration uses the source/root evidence associated with that checkpoint under 5.7.

No conflict. Pass.

## 17.2 Checkpoint target commit exists but live branch has advanced

Historical checkpoint cannot silently adopt newer live state unless its recovery contract explicitly selects that native revision compatibly.

5.7 must pin native live source as part of historical recovery selection when applicable. S1/S2 constrain this.

Pass with later representation requirement.

---

# 18. YAGNI / abstraction attack

Question:

Can Step 5.2 remove the named concept `Resumable Runtime Closure` entirely and just say “save all active runtime state”?

Answer:

No. The named property captures several cross-system correctness constraints that are not equivalent to “save state”:

- current vs durable distinction;
- native ownership;
- transitive dependency lifetime closure;
- bounded root discovery;
- rebuildable caches;
- live/domain-native composition;
- no-lost pending obligations;
- semantic pending input;
- interpretability context.

However the concept does **not** justify a record/class.

The abstraction is useful as an invariant/property, not as a data model object.

---

# 19. Duplicate-authority attack

Potential duplicates reviewed:

```text
checkpoint snapshot vs owners       -> forbidden
CURRENT tactical blob vs Procedure  -> forbidden
Temporal Agenda vs TemporalBinding  -> forbidden
root index state vs owner state      -> forbidden
transcript vs Interaction semantics  -> transcript not universal owner
trace RNG vs Resolution RNG          -> Resolution/Continuation own continuity
campaign fallback vs live owner      -> owning-scope resolution required
```

No surviving duplicate-authority path is required by the candidate after refinements.

---

# 20. Revised laws required for canonicalization

Canonical spec must include the candidate laws plus:

## LAW 5.2-9 — PINNED NATIVE HYDRATION

One recovery attempt pins each participating mutable native source to an exact revision and reads dependent state from those pinned revisions. Revision changes require re-selection/revalidation, never mixed branch-relative hydration.

## LAW 5.2-10 — OWNING-SCOPE RESOLUTION

Recovery resolves required identities through their current native ownership/routing contract. Stale representations in another domain are not fallback authority.

## LAW 5.2-11 — ROOT MEMBERSHIP COHERENCE

A durability acknowledgement that creates/removes recovery-root eligibility must include coherent routing membership change. Root projection completeness is a publication correctness invariant.

## LAW 5.2-12 — INTERPRETABILITY CLOSURE

Recoverable execution must resolve the accepted compatible runtime/catalog/rules context needed to interpret its typed state. Missing compatible interpretation context blocks recovery; arbitrary ambient rebinding is forbidden.

---

# 21. Final adversarial verdict

After applying S1–S6 and M1–M4:

```text
native owner architecture preserved       YES
bounded cold recovery possible in design  YES
Agenda remains derived                    YES
multiplayer partitioning preserved        YES
B-NARROW preserved during hydration       YES
cross-domain fallback prevented            YES
new semantic authority required           NO
new first-class closure record required   NO
human decision required                   NO
```

Recommendation: proceed to Resolution Gate/canonical specification with the refinements above.
