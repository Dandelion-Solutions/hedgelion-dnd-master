# R2.7 WP-07 — Step 6 Whole-Project Adversarial Review

Status: **PASS — RECOVERY REVIEW COMPLETE — 0 NEW BLOCKING / 0 NEW SIGNIFICANT FINDINGS**

## Recovery purpose and source route

This corrective Step-6 record replaces the former thematic conclusion with an
independent attack record for every WP-07 finding and for N02. It rechecks the
task-specific route required by `DEV/PROJECT_MAP.md` and the WP-07 Task-Brief
Critic:

```text
Step-4 semantic owners and single-context amendment
    -> R2.3 Context Runtime / R2.4 execution / R2.6 assurance consumers
    -> Step-5.10--5.13 Story, retention, disclosure and cleanup owners
    -> catalog exact-ID and field contracts
    -> installed GAME schema/template/instruction consumers
    -> interaction binding and focused conformance evidence
```

The review tests whether a current surface can wrongly acquire authority, bypass
eligibility/disclosure gates, widen retrieval, weaken recovery/retention, or turn
an accepted realization gap into a new architecture decision. It does not claim
that the currently unimplemented machine routes already provide end-to-end
runtime proof.

## Item-level attack records

### F01 — legacy lore `status` can collapse truth and lifecycle

**Abuse mechanism.** Treat `GAME/SCHEMA/lore.schema.yaml` as a current semantic
owner and use its single `status: enum[canonical, superseded,
disputed_in_world]` axis to decide both objective truth and record lifecycle.
That would either revive an objective `disputed` truth state or make
supersession a truth claim.

**Owners, consumers and dependency route.** Step-4 sections 4.1--4.4 own the
separate truth/lifecycle model; its `world.lore_fact` catalog contract requires
`statement`, `truth_status`, and `record_status`. The installed lore schema is a
machine representation consumer, not a semantic owner. The focused catalog
conformance test checks the separate `truth_statuses`, `lore_record_statuses`,
and required lore fields.

**Concrete evidence.** The installed schema still requires `status` and lists
`canonical`, `superseded`, and `disputed_in_world`, even though its prose
invariant says in-world dispute belongs to knowledge. Step-4 says truth and
lifecycle are separate, and `DEV/CATALOG/entity-structures.json` requires the
two distinct fields. No inspected consumer establishes the legacy enum as an
override of those owners.

**Process classification.** `STALE_DEBT`.

**Why no new owner/spec/human decision is required.** The accepted owner already
fixes the required semantic split; the unresolved work is a narrow later schema
repair. This review neither chooses a migration nor invents a new lore path.

### F02 — stale `world.knowledge` prose can overwrite the exact field contract

**Abuse mechanism.** Treat the `ENTITY_STRUCTURES.md` row using `status` and
`learned_from_id` as the current machine shape, thereby restoring a stale
knowledge vocabulary or creating a second event/provenance representation.

**Owners, consumers and dependency route.** Step-4 section 5 owns the sole
current subject-to-proposition relation keyed by `(knower_id, fact_id)`;
`CATALOG_CONTRACTS.md` assigns exact machine field/identifier authority to the
catalog JSON. `ENTITY_STRUCTURES.md` is an owning-prose companion, while
`entity-structures.json`, `identifier-policies.json`, and
`test_r2_7_wp03_catalog_conformance.py` are current machine-contract consumers.

**Concrete evidence.** The prose row lists `status` / `learned_from_id`; the
current catalog requires `knower_id`, `fact_id`, `stance` and permits bounded
`supporting_source_refs` / `last_changed_event_id`. The focused test asserts
that exact current field contract and composite identity. Step-4 keeps full
history in SemanticEvents, so neither stale prose nor a future physical record
authorizes a second epistemic event log.

**Process classification.** `STALE_DEBT`.

**Why no new owner/spec/human decision is required.** The canonical owner and
exact catalog already resolve the disagreement. A later narrow prose and ledger
citation repair is traceability work, not a new knowledge semantic, record
owner, physical path, or compatibility decision.

### F03 — absent Story root can be misread as Story authority or a mandate to invent one

**Abuse mechanism.** Infer that the absence of `story_root` from the installed
manifest makes Story unavailable as a noncanonical projection, or compensate by
placing mutable Story progress in `MANIFEST`, `CURRENT`, or recovery state.

**Owners, consumers and dependency route.** Step-5.10 owns Story projection
durability and says Story is durable but noncanonical. The campaign manifest
schema/template are installed routing consumers. Step-5.10 permits a future
static `story_root` established by scaffold/migration, while forbidding ordinary
Story catch-up from mutating `MANIFEST` merely to advance projection progress.

**Concrete evidence.** `campaign_manifest.schema.yaml` and
`GAME/CAMPAIGN/MANIFEST.yaml` route only `STATE`, `INDEX`, `WORLD`, `LOG`, and
`CHECKPOINTS`; no Story root exists. Step-5.10 expressly records a possible
later static Story route and independently prohibits Story records, coverage,
and generated prose from becoming gameplay authority.

**Process classification.** `IMPLEMENTATION_OBLIGATION`.

**Why no new owner/spec/human decision is required.** The absence is the named
deferred machine-realization gap under the existing Story owner. Selecting a
physical root, scaffold, schema, or migration now would exceed WP-07 evidence
work without resolving an architecture ambiguity.

### F04 — catalog admission can be mistaken for installed durable realization

**Abuse mechanism.** Treat admitted IDs for `world.knowledge`,
`runtime.disclosure`, and `runtime.message` as proof that the installed GAME
tree already has durable records, then either use interaction IDs as substitute
authority or invent arbitrary roots and schemas.

**Owners, consumers and dependency route.** Step-4 and Steps 5.11--5.12 own
the semantics. `CATALOG_CONTRACTS.md` and catalog JSON own exact IDs, field
shape, and identity policy; `CATALOG_ADMISSION.md` owns admission/realization
trace interpretation. Installed schemas/templates and
`runtime-interaction-state.schema.json` are machine consumers.

**Concrete evidence.** Catalog contracts identify the four owners and composite
keys for knowledge/disclosure; the interaction-state schema binds campaign,
session, authenticated player, input message, and optional response message IDs.
It does not define dedicated durable owner records. `CATALOG_CONTRACTS.md`
section 12 explicitly routes truth/knowledge/disclosure/message schemas, roots,
HOT/SQLite, and recovery details to later R2.7 work; admission rules prohibit
the ledger from overriding a domain owner or serving as a runtime package.

**Process classification.** `IMPLEMENTATION_OBLIGATION`.

**Why no new owner/spec/human decision is required.** Admission and realization
are intentionally separate evidence axes. The existing owners define the later
realization cluster, and WP-07 does not have authority to select physical paths
or claim that the legacy scaffold is complete.

### F05 — PC/live fields can become parallel knowledge or disclosure authority

**Abuse mechanism.** Use embedded PC knowledge arrays or live-epoch perception
fields as a globally writable current knowledge/disclosure store, or equate a
PC's fictional observation with human recipient disclosure.

**Owners, consumers and dependency route.** Step-4 owns `world.knowledge`;
Step-5.12 owns recipient-scoped `runtime.disclosure`; PC and live-scene schemas
plus `CORE/LIVE_SCENE.md` are bounded projection/epoch consumers. The
campaign-absorption path is the only lawful route out of a closed live epoch.

**Concrete evidence.** `pc.schema.yaml` calls legacy `knowledge` a
non-authoritative projection/input surface that does not replace
`world.knowledge`. `live_scene.schema.yaml` labels objective truth and per-PC
knowledge/disclosure distinct, records `known_by_pc_ids` and
`perceived_by_pc_ids` only within an epoch, and requires durable absorption
after closure. `LIVE_SCENE.md` requires a closed epoch's routing/absorption
check and forbids automatic disclosure to PCs lacking a perception or knowledge
channel.

**Process classification.** `VERIFICATION_OBLIGATION`.

**Why no new owner/spec/human decision is required.** No inspected field grants
parallel global authority, but executable normalization, recipient isolation,
and no-second-live-disclosure-owner proof are still absent. That is a later
machine verification obligation under existing owners, not grounds to define a
new record or change the semantic boundary.

### F06 — generic CORE containment prose can be falsely accepted as the R2.6 instruction realization

**Abuse mechanism.** Treat generic distinctions among truth, fictional
knowledge, player disclosure, and bounded retrieval as fulfillment of the
explicit active-role/`RoleContextBundle`/lawful-typed-handoff instruction, or
misread shared physical context as permission for raw-role inheritance.

**Owners, consumers and dependency route.** R2.6 section 3 owns the explicit
shipped instruction requirement; the Step-4 amendment, R2.3, and R2.4 own the
eligibility, bounded assembly, rebinding, and typed-handoff laws. The installed
`PROJECT_INSTRUCTIONS.txt` and CORE corpus are shipped instruction consumers.

**Concrete evidence.** R2.6 requires the exact behavior equivalent: use only
information eligible to the active role under the current `RoleContextBundle`
and lawful typed handoffs; physical presence does not confer eligibility; lawful
later eligibility restores normal use. The inspected project instructions and
CORE modules include generic authority, knowledge-compartmentalization, and
smallest-working-set guidance, but contain no explicit active-role,
`RoleContextBundle`, or lawful typed-handoff equivalent. The amendment and R2.4
independently forbid physical-presence eligibility and raw private handoffs.

**Process classification.** `IMPLEMENTATION_OBLIGATION`.

**Why no new owner/spec/human decision is required.** R2.6 already assigns the
exact wording, module activation, and tests to R2.7 and implementation/TDD. The
absence cannot satisfy the rule, but it also exposes no unresolved authority,
product, compatibility, or risk-acceptance choice.

### N02 — cross-owner attacks on eligibility, disclosure, retrieval, and recovery

**Abuse mechanism.** Combine otherwise lawful surfaces to create a bypass:
promote Story/Transcript/trace/host context to authority; use an unbounded
history scan after failed assembly; disclose material through an auxiliary
surface; or delete/compact message evidence before owner and survivor
obligations are discharged.

**Owners, consumers and dependency route.** Step-4 and its amendment own the
five-way information boundary and logical eligibility. R2.3 owns bounded
discovery, terminal `UNSATISFIABLE`, and non-authoritative `ContextTrace`; R2.4
owns rebinding and minimal typed handoffs; R2.6 owns observable behavioral
containment. Steps 5.10--5.13 own noncanonical Story, message retention,
`EMISSION_COMMIT`, disclosure closure, and cleanup. Installed CORE instructions,
interaction binding, and schema/template surfaces are consumers only.

**Concrete evidence.** R2.3 forbids ordinary whole-history/global-campaign
fallback and makes `UNSATISFIABLE` terminal for an attempt. R2.4 requires a
fresh role bind and prohibits raw private handoffs; R2.6 defines behavioral,
not physical/cognitive, containment. Step-5.12 requires eligible-content,
material-disclosure-ref, and recipient validation before `EMISSION_COMMIT`,
prohibits auxiliary secret-delivery surfaces, and preserves the accepted
post-commit interruption limitation. Step-5.11 preserves message identity and
semantic meaning across lawful payload compaction; Step-5.13 leaves liveness and
survivor decisions with native owners and rejects universal cleanup authority.
No inspected GAME consumer contradicts these boundaries or promotes host context,
Story, Transcript, trace, cache, index, or prose to current semantic authority.

**Process classification.** `SATISFIED` as an adversarial coverage requirement;
existing F01--F06 realization/debt classifications remain unchanged.

**Why no new owner/spec/human decision is required.** The attack paths terminate
in already accepted owners and explicit constraints. Behavioral containment is
not misrepresented as physical isolation, and the `EMISSION_COMMIT`
over-confirmation limitation is retained rather than silently repaired with a
new delivery subsystem.

## Result

Every F01--F06 and N02 attack has a concrete owner/consumer route, evidence,
process classification, and non-escalation rationale. The corrective review
found no new `BLOCKING` or `SIGNIFICANT` finding, no material candidate
correction, and no residual human decision. Step 7 may now determine whether
these unchanged, owner-routed dispositions permit canonicalization.
