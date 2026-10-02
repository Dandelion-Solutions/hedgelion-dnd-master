# W05.T06-A1 — Step 6 Whole-Project Adversarial Review

Status: COMPLETE
Stance: assume the candidate is subtly wrong.

The dependency graph was reconstructed from PROJECT_MAP and the actual currentness, Context, History, information, Story, RuntimeHost, bootstrap and readiness owners rather than from the candidate alone.

## Findings

### H06-01 — SIGNIFICANT — durable EVENT_INDEX alone misses accepted unpublished history

Mechanism:

WP12 permits accepted unpublished HOT/SOFT SemanticEvent state. A retrospective immediately after such an event could return an older durable history result if discovery consults only EVENT_INDEX at pinned Git.

Impact: wrong current/past-game answer before SAVE.

Resolution required: event establishment must update a non-authoritative HOT discovery helper atomically, and query composition must include accepted HOT rows under the same operation snapshot.

### H06-02 — SIGNIFICANT — selected LIVE cannot fall back to campaign discovery

Mechanism:

A current LIVE-owned event/history scope may differ from campaign durable history. Reusing campaign EVENT_INDEX as current discovery when LIVE lacks equivalent metadata silently violates LIVE currentness.

Impact: stale or contradictory retrospective.

Resolution required: selected LIVE supplies its own bounded discovery metadata/current event evidence or returns typed inability. Campaign history remains durable past evidence, not current LIVE fallback.

### H06-03 — SIGNIFICANT — per-record HOT reads can mix operation state

Mechanism:

The candidate names CurrentOwnerView but does not yet require a coherent HOT read snapshot. Multiple owner reads could observe different accepted local generations during concurrent mutation.

Impact: readiness or eligibility assembled from a state combination that never coexisted.

Resolution required: bind an operation-scoped SQLite read snapshot or equivalent validation token. This is operational consistency only, not a global semantic frontier.

### H06-04 — SIGNIFICANT — discovery metadata/raw event access can become a secret leak

Mechanism:

A deterministic service can physically read private event bodies or protected identifiers. If these are returned in tool/context payloads before Narrator filtering, logical eligibility is already compromised in a single-context host.

Impact: private historical material enters the model context.

Resolution required:

- durable index copies only existing index-safe refs;
- raw EVENT_INDEX/HOT helper and raw private event payload remain inside deterministic runtime;
- Context receives only a sealed evidence carrier;
- final role bundle contains only independently eligible projections;
- missing eligibility metadata excludes the material rather than exposing it.

### H06-05 — SIGNIFICANT — caller can otherwise turn retrospective flag into evidence injection

Mechanism:

Current ContextService accepts request/candidate mappings. Merely changing retrospective=True from unconditional UNSATISFIABLE to normal candidate assembly would let a caller nominate runtime.semantic_event or protected payload without a service-issued proof route.

Impact: authority bypass.

Resolution required: runtime.semantic_event historical material is admitted only through a RuntimeHost-issued unforgeable/sealed evidence path tied to the operation basis. The ordinary public candidate mapping cannot carry raw historical payload authority.

### H06-06 — MINOR — event template already disagrees with current History enrollment contract

Current History adapter expects complete and upper_ordinal semantics while the blank EVENT_INDEX template is minimal. T06 History discovery will touch the same surface.

Resolution: include template/writer/schema alignment in the implementation prerequisite and Version Impact Gate. Do not treat the current blank file as proof of a different semantic contract.

### H06-07 — MINOR — Story revisit must not silently become implementation scope

The candidate defers Story but does not explicitly classify the item as dormant.

Resolution: canonical result records exact revisit triggers and no current implementation task.

## Whole-project conflict check

No accepted owner requires Story for ordinary Master baseline.

No accepted owner permits repository-only readiness.

No accepted owner grants Context direct authority to search History.

No accepted owner conflicts with an operation-scoped internal current-owner view as long as source selection remains delegated to campaign/HOT/LIVE owners.

No Product Owner trade-off is exposed by these findings; all significant findings have owner-determined repairs.

BLOCKING: 0
SIGNIFICANT: 5
MINOR: 2
PRODUCT_OWNER_DECISION_REQUIRED: NO
STEP_7_REQUIRED: YES
