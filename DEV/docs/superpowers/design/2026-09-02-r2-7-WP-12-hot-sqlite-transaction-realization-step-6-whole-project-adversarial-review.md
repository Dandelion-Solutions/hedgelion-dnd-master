# R2.7 WP-12 — Step 6 Whole-Project Adversarial Review

Status: **COMPLETE — BLOCKING/SIGNIFICANT FINDINGS REQUIRE MECHANICAL REPAIR**

## 1. Independent dependency reconstruction

The critic restarted from current `DEV/PROJECT_MAP.md` rather than trusting the
Step-1 manifest or Step-5 candidate. It followed the persistence/HOT route into:

- Step-3 deterministic execution and embedded ExecutionSegment;
- Step-5.2 native-owner recovery and interpretability closure;
- Step-5.5 scoped durability;
- Step-5.6 publication/currentness/dirty-generation law;
- Step-5.7 recovery/checkpoint law;
- Step-5.8 live claims/CAS;
- Step-5.14 integrated recovery/concurrency clarifications;
- R2.3/WP-09 Context Runtime and information-eligibility boundary;
- WP-10 record-family allocation and WP-11 route/index law;
- `ACCESS_CONTROL.md`, `BRANCH_MODEL.md`, Actor/Asset/catalog/
  `MECHANICAL_CONTEXT.md` owners;
- GAME Storage/Persistence/Save/Integrity/Multiplayer/Live/Randomness consumers;
- current campaign/current/live/checkpoint/storage schemas and runtime-owner
  machine contracts;
- current maintenance-audit implementation.

The review asks whether a convenient SQLite implementation could create new
authority, drop an accepted qualifier, lose an owner generation, leak inaccessible
information, reinterpret accepted execution, or turn a local transaction into a
cross-source transaction.

## 2. Findings

| ID | Attack / failure mechanism | Severity | Required resolution |
|---|---|---|---|
| F01 | Candidate LAW WP12-4 correctly says source selection is metadata for one native owner, but §12's baseline expectation says the owner surface is keyed by `native family + owner identity and current source basis`. If source basis participates in the current-owner uniqueness key, campaign and live versions of the same semantic owner can coexist as independently current/writable rows. | BLOCKING | Current-owner semantic key must be native campaign/context + family + complete native identity. Source/currentness basis is metadata, never part of semantic-owner uniqueness. Historical/source evidence belongs in explicitly non-current support storage. |
| F02 | LAW WP12-18 says a live prospective result is not shared established state before CAS, but allows it to be “committed/staged” locally. An implementation could overwrite the accepted current owner row before CAS, and another local consumer/narration path could observe it as current despite the remote write later failing. | BLOCKING | Pre-CAS live mutation must remain an **ephemeral prospective overlay/frozen transition**, not the accepted current owner row. Confirmed compatible live CAS is followed by one local adoption transaction. Failed/stale/closed CAS discards/rebases only the prospective transition under Step-5.8 rules. |
| F03 | LAW WP12-12 says source movement invalidates affected owner/helper state. Applied literally, a disjoint campaign HEAD movement could invalidate already-established local SOFT owner generation and force semantic replay, contradicting Step-5.6 transport-only rebuild and Step-5.5 ESTABLISHED≠DURABLE. | SIGNIFICANT | Distinguish source-derived clean assumptions from established local owner generations. Disjoint external movement preserves accepted local semantics/IDs/RNG and only rebases source/publication basis; overlapping dependency movement triggers owner-specific revalidation/re-resolution. |
| F04 | The candidate states Context Runtime helpers are non-authoritative but does not state that physical presence of owner payloads in HOT never grants role eligibility, read authority or write authority. A generic local query path could bypass R2.3 information eligibility or `ACCESS_CONTROL.md` simply because the bytes are already in SQLite. | SIGNIFICANT | Add a hard access/eligibility law: local possession is not permission. Semantic reads presented to an HDM role and all mutations must pass the existing role-context/information/access-control boundaries; helper/query APIs cannot launder hidden/private state into an ineligible role. |
| F05 | LAW WP12-16 freezes owner generations/dependencies/source basis but omits the exact acting principal/authorization basis required by Step-5.6 and `ACCESS_CONTROL.md`. A prepared publication could outlive a membership/authority change and be sent under stale authorization. | SIGNIFICANT | Frozen publication state must carry the exact authorization/principal basis required by the native write contract, and the owning publication/access protocol must revalidate any mutable authorization dependency at its required pre-mutation boundary. Local cached creator/player evidence remains derived evidence, not authority. |
| F06 | LAW WP12-2 requires current owner-schema validation, but the candidate does not explicitly protect Step-5.2 interpretability closure for open execution. A later ambient catalog/rules/schema context could be used to reinterpret an old accepted Command/Resolution/Continuation during local adoption/hydration. | SIGNIFICANT | Runtime owner rows must retain/reference the accepted catalog/rules/invocation/dependency context required by their native contracts. Structural migration/validation may evolve representation, but open accepted work is never silently rebound to arbitrary newer ambient mechanics. |
| F07 | The candidate does not explicitly scope every current-owner operation to the selected campaign/runtime authority context. A future shared SQLite file or pooled process could accidentally satisfy an owner lookup from another campaign/session namespace with the same family/native ID. | SIGNIFICANT | Add logical isolation: every owner/currentness/query/mutation operation is explicitly scoped to the selected campaign/authority context. Physical one-file-per-campaign is an implementation option, not architecture law; any co-hosting must provide hard namespace isolation and cannot permit cross-campaign currentness or access inference. |
| F08 | LAW WP12-20 permits reuse of surviving local bytes as a “validated cache” but does not state the validation ceiling precisely. An implementation could treat unpublished dirty HOT bytes that survived a process crash as recoverable current state, weakening Step-5.2 LAW 5.2-7. | SIGNIFICANT | Cold recovery may reuse local bytes only after proving them equal to/derivable from the currently selected compatible native source as non-authoritative cache. Unpublished local owner generations are not recovered as established canon merely because a SQLite file survived. |
| F09 | `DEV/ARCHITECTURE/BRANCH_MODEL.md` still describes storage marker v2/`baseline_version`, while current shipped `GAME/SCHEMA/dnd_storage.schema.yaml` and `GAME/CORE/STORAGE.md` use storage v3 structured baseline provenance. This is a current documentation/topology inconsistency discovered through the storage route, but it does not change WP-12's only relevant law: storage baseline is not existing-campaign runtime authority. | MINOR | Preserve as documentation-consistency forward work for WP-26/current storage owner reconciliation. Do not reopen WP-12 or treat either marker shape as HOT semantic authority. |

## 3. Attacks that did not produce new findings

The critic also attempted and rejected these failure paths because the candidate
already blocks them:

- SQL rowid/AUTOINCREMENT/order as native identity or fictional chronology;
- generic `pending_work`, scheduler, publication journal or RecoveryCut owner;
- standalone semantic `runtime.execution_segment` introduced for SQL convenience;
- campaign-wide SQL scan as ordinary known-ID hydration;
- checkpoint/current_state/index/cache becoming current authority;
- global durability timer/frontier reintroduced through dirty metadata;
- SQLite transaction held across GitHub/network/player dialogue;
- campaign + live distributed transaction;
- storage baseline overriding an existing campaign runtime;
- MechanicalContext/DAG/context bundle persistence as recovery authority;
- live campaign-base fallback while the selected live source owns the mutable
  claim;
- rollback/replay of accepted RNG merely because transport/currentness changed.

## 4. Severity and decision gate

All BLOCKING/SIGNIFICANT findings are specification-precision defects with a
single owner-conforming repair. None creates a credible competing product semantic,
canonical ownership transfer, compatibility policy or material risk choice.

**Human decision required: NO.**

Step 7 must repair F01–F08, preserve F09 as scoped forward consistency work, and
run the mandatory finding-propagation sweep before Step 8.
