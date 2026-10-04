# Spell execution architecture - independent Step 6 review

Status: FINAL STEP-6 REVIEW - DECISION-READY PROPOSAL. Significant technical findings SC-02, SC-03 and SC-06 and minor findings SC-04 and SC-05 are CLOSED at candidate-design scope. SC-01 is WITHDRAWN. The sole residual human judgment is SP-14 Wish Roll Redo, recorded NEEDS_PO. This record grants no canonical architecture, implementation, production, Step 8 or Review Stop 2 acceptance.

Date: 2026-10-04. Independent whole-project candidate critic. Source baseline: `Dandelion-Solutions/hedgelion-dnd-master` at `05576261665280c3f424d791c19d8c4080343c6a`. Connector `git/ref/heads/v1/engine-rearchitecture` independently returned that exact SHA at bootstrap and again after the final READY signal; recursive remote tree was complete (`truncated=false`, 1,650 entries). No remote write, gameplay/bootstrap, release ZIP, executable GAME test or target latency measurement occurred. Read-only design-data integrity assertions were executed. Only this scratch review is written by this critic.

## Review boundary and independent discovery

The review tests a design proposal for faithful local support of the complete SRD spell corpus. It does not treat catalog names, conformance fixtures, source scans, architecture routing or prior-wave PASS as proof of a composed production cast. Genuine Wish Roll Redo `NEEDS_PO` remains blocking for dependent accepted architecture; a proposal may be ready for that concrete judgment without pretending the judgment was supplied.

Independent discovery followed current AGENTS/runtime/process/Project Map/current progress and the actual remote tree. It found native `world.connection`, location, zone, Actor, Effect and information carriers; selected native schemas; actual command/catalog/durability/publication producer-consumer seams; and current PO-004 meaning beyond the candidate's stated label. Source-specific exceptions, current scheduling and accepted boundaries take precedence over candidate wording.

| Owner / evidence route | Actual inspected scope and review use |
|---|---|
| `AGENTS.md`; `DEV/AGENT_RUNTIMES/CHATGPT_WORK.md`; `SKILL_SCOPE.md`; `DEV/DESIGN_PROCESS.md`; `DEV/ARCHITECTURE/DESIGN_PROCESS.md` | Bootstrap, authority, independent whole-project critic, evidence, Step 6/7/8 and exact two Senior stops; bounded subagent inheritance and no duplicate PO gate |
| `DEV/PROJECT_MAP.md`; recursive pinned tree; `DEV/CURRENT_PROGRESS.md` | Independent ownership/dependency routing, global header/cursor and preserved P0/S1/S2/P1A/P2/P3/Story gates. Map is derivative; current progress is scheduling authority |
| `DEV/ARCHITECTURE/PRODUCT_OWNER_INPUT_PROCESS.md`; `DEV/PRODUCT_OWNER_INPUT.md` applicable entries | Verbatim/routing preservation, cross-stage intent, clean-slate policy, historical decision-basis cost, public provenance, failure/durability, sizing and response/perspective boundaries |
| `ACTOR_MODEL.md`; `ASSET_MODEL.md`; `HEALTH_EFFECTS_RECOVERY.md`; `ENTITY_STRUCTURES.md` | Full Actor/Health owner bodies; material Asset handling/identity/consumption and entity ownership tables/invariants. One writable HP/location owner; stable identities; singular target-local Effects; support DAG; physical location vs micro-position; native connection/portal route |
| `ACTIVITY_MODEL.md`; `MECHANICAL_CONTEXT.md`; `ACTIVITY_PRIMITIVE_CONTRACTS.md` | Full Activity/Context owner bodies; primitive core/execution/activation laws. Finite typed recipes; exact consumer permission; no arbitrary query/patch; no dormant activation; fixed causal inputs and disposable prospective context |
| Step-3 final execution spec | Interaction/IntentPlan/command/binder/Procedure/Resolution/segment sections and recovery/choice laws relevant to the review; immutable accepted events/RNG, native atomicity and mandatory descendant closure |
| Step-4 truth/knowledge spec; R2.4 single-context spec | Truth/proposition identity, knowledge subject and PC agency, monotonic exact human exposure; full R2.4 role/context/handoff/visible-output and failure boundary |
| Step-5.9 chronology spec | Forward-extensible capability boundary, immutable anchor/event meaning, mutable-past enforcement and supported rate/stasis scenarios. Roll Redo is a real new-consumer insufficiency requiring an explicit exception |
| WP-16 spec | Actual claim grammar, lifecycle, source-native identity, cross-source freeze, no distributed transaction, no accepted rollback, native durability-edge granularity, information/agency and currentness |
| WP-24 spec and current sizing amendment | Actual ordinary-path, physical-call, evidence-class, cache/currentness, direct routing and semantic-preservation laws; read-only content is not subject to mutable artifact hard caps |
| Selected `DEV/SCHEMAS/world-{actor,effect,zone,location,connection}-state.schema.json` | Actual native carriers and open structural fields. Structural objects do not supply an executable mutation profile or decide missing body/soul factoring |
| Actual GAME `catalog_runtime`, `runtime_execution`, `mechanics`, `runtime_host`, `durability`, `publication`, `temporal`, `information`, `native_storage` | Function/source-shape inspection. Independently corroborated nested catalog carrier vs flattened join-generation check and absent command execution join in composed publication route; source evidence, not executed failures |
| `GAME/CORE/AI_REASONING.md`, `PLAY_POLICY.md`, `MAGIC.md`; House Rules and portable-value owners | Actual interpretation/local fallback wording and accepted role/adjudication boundaries. Supported deterministic rules gaps need the proposed CORE qualification; genuine fictional judgment is retained |
| Current local candidate package and supplied spell extraction | Final candidate re-read after READY; Decision Brief, system impact, product routing, source-obligation resolution and repair propagation inspected with existing production/performance/capability evidence. Direct full bodies for Astral Projection, Magic Jar, Clone, Creation, Demiplane, Fabricate, Gate, Magnificent Mansion, Teleport, Prismatic Spray and Reincarnate independently checked for identity, physical, information, stochastic and cross-source consequences |
| Final `requirement-matrix.json`; `source-pass-{0-2,3-5,6-9}.json`; `source-body-witnesses.json`; `build_requirements.py` | Independent name/level/group/route/hash/reference checks over every row; all 339 per-entry mode/exception summaries inspected and full-body reviewers' common obligations/findings/source limitations reconciled. Generator source audited. Those independent source passes supply the whole-corpus full-body reading evidence; this critic does not claim a fourth complete primary-body pass or executable recipe proof |

Clean Architecture is applied as a dependency/authority lens under the HDM override. No textbook score is used to reopen accepted owners; the meaningful checks are whether definitions depend on exact inner semantic contracts, adapters preserve native establishment, and caches/projections never become authority.

## Historical actionable findings and final repair disposition

The original defect descriptions below are retained so closure does not erase the review evidence. CLOSED means that the final candidate has selected and stated a sufficient repair, not that machine contracts or GAME production now implement it.

### SC-02 - SIGNIFICANT - body/soul/astral factoring left for later design

Candidate SP-10 requires exact linked-body state, but capability-closure section 5.2 says exact representation factoring remains a candidate design decision. Decision Brief says only SP-14 remains as a material residual judgment. A complete candidate cannot leave the identity/health/location/knowledge boundary of required Magic Jar, Clone and Astral Projection modes undefined.

Owner constraint: Actor Model sections 5/8 owns one Actor hp and physical location; Step-4 knowledge uses a subject identity. Astral Projection supplies independently affected body/form and replicated possessions; Magic Jar transfers a controller/mental statistics while the original bodies remain independently real. A same-Actor live stat projection alone cannot represent these consequences.

Required repair: choose concrete existing native carriers and narrowly typed episode links. Specify principal vs body/proxy identity, each sole HP/location/resource/knowledge owner, legitimate possession replicas, PLAYER control versus in-fiction controller, death/return/container-destruction ordering, atomic closure and cold/LIVE recovery. Do not introduce a universal soul service. Handle a mechanically derivable owner-conforming factoring without a new PO gate; surface a judgment only if a genuinely material authority choice remains after analysis.

Disposition: CLOSED after independent final re-read. Candidate section 12.1/SP-22 selects stable principal Actors, separately native physical/proxy Actors, native container/original/replica Assets and one typed spell-root Effect relation. Atomic split removes competing physical HP/location from the principal; each independent body owns current native health/location, and knowledge stays with the principal knower without host union. Current-state return, death/cord/container branches, replica teardown, explicit Effect subject bindings, Procedure/control authorization and cold/LIVE recovery are stated. Coordinated Actor/Health/Information amendment is a prerequisite to activation. Decision Brief, SI-25 and source-resolution L69-03 agree; capability-closure's old factoring-open sentence is explicitly historical and superseded. This is a sufficient selected technical design and leaves no second product judgment.

### SC-03 - SIGNIFICANT - all-or-nothing reality wording lacks exact multi-LIVE route

SP-14 stages complete reconciliation and forbids partial reality rewrite while merely saying native multi-owner/LIVE boundaries remain observed. WP16-42 forbids a distributed transaction; WP16-44 preserves a first accepted native edge when another source rejects. Two affected ACTIVE LIVE sources therefore make the unspecified route ambiguous.

Required repair: explicitly select the already accepted WP16-43 close/freeze route, prove exact finals, perform lawful absorption/routing and the owning forward campaign establishment, then optional successors. Partial close progress is technical state only. Specify stale/indeterminate/capacity behavior before the first reality-reconciliation edge, plus recovery after accepted establishment. Never restore an accepted native edge merely because another source fails. Use two-LIVE conflict/recovery witnesses. This is owner reconciliation, not an additional PO gate.

Disposition: CLOSED after independent final re-read. SP-14 selects exact WP16 freeze/close, final-proof and lawful absorption into one campaign owner before replacement fiction. A first successful close remains pending preparation if a later close fails; original fiction stays intact. Only the complete staged campaign replacement is established at the single native atomic edge, with exact owner-issued join/currentness proof and later LIVE successors. After acceptance, failure preserves the replacement and recovers forward. Decision Brief and SI-07 preserve this qualification. The candidate no longer promises cross-LIVE distributed atomicity or rollback. SP-14's underlying mutable-past exception remains NEEDS_PO independently of this now-closed technical finding.

### SC-04 - MINOR - wrong PO-004 provenance label

`system-impact.md` calls PO-004 voluntary PC control. Current `DEV/PRODUCT_OWNER_INPUT.md` PO-004 is the v1.0 clean-slate compatibility baseline. Agency is owned by Actor Model 7.5, Step-4 5.4 and WP16-51.

Required repair: correct the pointer and retain clean-slate/no v0.8 migration meaning. No decision or accepted-law change is required.

Disposition: CLOSED after independent final re-read. The system-impact product route identifies PO-004 as clean-slate compatibility and points agency to Actor Model 7.5, Step-4 5.4 and WP16-51. Original Product Owner quotations remain unchanged.

### SC-05 - MINOR - unregistered MAPPER role wording

Candidate section 2 calls interpretation the existing Master/MAPPER logical role. The accepted Step-4/R2.4 phase is Interpreter; current AI_REASONING supplies no MAPPER role.

Required repair: use existing Interpreter phase terminology. Preserve one-chat and zero-extra-call laws; no new role or authority follows.

Disposition: CLOSED after independent final re-read. Candidate section 2 uses Interpreter. It preserves one chat, existing logical eligibility and zero intermediate/dedicated spell-model-call requirements. No new GAME role is activated.

### SC-06 - SIGNIFICANT - Prismatic Spray repeat wording can reject legal duplicate rays

New SP-21 says Prismatic Spray rejects a duplicate two-ray result. Direct supplied body inspection establishes that secondary ray draws reject table result 8 only; two equal results from 1-7 remain legal. Deduplicating rays would change the damage distribution.

Required repair: state the exact rejection predicate and allow identical non-8 rays. Future fixed-RNG witnesses must include `[8,1,1]` (two Red rays) and `[8,8,1,2]` (secondary 8 rejected, Red plus Orange). No new decision is required.

Disposition: CLOSED after independent final re-read. SP-21 rejects only secondary result 8, allows identical non-8 rays and states both required fixed-sequence fixtures. Source-pass L69-01 and source-obligation resolution agree. The resumable exact stochastic profiles cover Teleport, Prismatic Spray and Reincarnate without a semantic attempt cap or changed probability distribution. These fixtures are future conformance obligations, not tests executed in this review.

## Closed false positive

SC-01 is WITHDRAWN. Initial Cyrillic/control-character rendering looked corrupt even through explicit UTF-8 PowerShell output. ASCII-only `.NET ReadAllText(UTF8)` codepoint evidence proves product-input has zero U+FFFD and zero disallowed controls, and the original block starts U+043C U+0435 U+043D U+044F. This is a terminal display issue. No immutable text rewrite is requested or authorized by that observation.

## Final challenge outcomes

- Shared finite Activity/native owner extension is justified; thirteen research groups need no thirteen executors, runtime subagents or model fan-out.
- Casting null-target outcomes preserve costs and secrecy; malformed binding remains a distinct preacceptance error. Counterspell needs its exact current slot/action commitment profile.
- Form HP/temp-HP/gear, generic concentration, periodic work and Conditions are correctly qualified as exact extensions, not already active production mechanics.
- Rule package identity and cache identity remain distinct; no loader/cache proposal may weaken current changed-source negatives. Cold validation is not a per-turn catalog prompt.
- Actual producer/consumer contradictions require real-producer composition repair and native end-to-end evidence; they do not automatically invalidate prior bounded Wave acceptance.
- Genuine fictional adjudication is required for open effects; model arithmetic, arbitrary patches and internet rules lookup do not provide a supported deterministic fallback.
- Wish Roll Redo `NEEDS_PO` is justified by current chronology/accepted-event laws. Proposal readiness and accepted architecture remain separate verdicts.
- The final source-specific additions close the current common one-slot-per-turn, prepared ritual and long-casting consumers; Fire Storm's each-cube-neighbor predicate without inventing global connectivity; enduring consequences of instantaneous spells; exact conditional release rather than automatic decade expiry; lawful successors/permanent native state; sparse indexed counters; prospective interception and source-specific reaction payer; and death-time knowledge/nonleaking disclosure. They are explicit exact-consumer extensions with admission and production proof still required.
- Form/summon dependencies cover complete eligible lawful domains and their actual actions, not example lists. Wish feat replacement similarly closes eligible feats/prerequisites. Unseen Servant's selected sparse force Actor carrier does not silently confer creature targeting or private cognition; source-ambiguous eligibility remains a bounded pre-outcome fact/policy consumer.
- Source reconstruction, Telekinesis's licensed continuation, displaced supporting blocks, foreign tails, seed metadata/provenance and the extra Thunderclap entry remain explicit content-admission obligations. They do not leave an unresolved engine owner or require a repeated product-scope decision. Valid Unicode signs are preserved.

## Independent final corpus integrity evidence

The following checks ran read-only against the exact final files after READY. All assertions completed successfully. They verify routing/evidence integrity, not source interpretation by hash, machine admission, executable recipes or runtime behavior.

| Check | Independently observed result |
|---|---|
| Source/pass/witness/matrix name sets | Exactly 339 unique names, no omitted or duplicate pass row; disjoint 141 + 114 + 84 source-pass slices exhaust the supplied extraction |
| Levels | 0:27, 1:57, 2:57, 3:42, 4:34, 5:38, 6:31, 7:20, 8:17, 9:16; matrix/witness/extraction agree |
| Extracted body identity | All 339 SHA-256 values recomputed from exact supplied body strings equal witness, linked independent pass and matrix values; witness level/page/header-line fields also equal extraction |
| Detailed evidence preservation | Each matrix row resolves to its exact named independent row; every independent SP route survives; all routes are SP-01..SP-24. Every row retains nonempty mode/exception and qualification evidence in its hashed source artifact |
| Research identity | LF-normalized UTF-8 inventory SHA-256 `cd894d28ef8693352c2a80c01e062a058358ef3734ff6f813e42c934fb84e4c3`; all matrix names, levels, pages and groups equal that inventory. Raw CRLF file-byte hash `1154f9b1770fd918cf8ccf4fbcc6ad2212ac12f1300088eebf5ef6b34e06e68f` differs only by the declared newline basis, not semantic promotion |
| Matrix | 412,991 bytes; LF UTF-8 SHA-256 `254bde30639bc0071fd944d738407f4e01987065ef6b6448a82b11eae2438372` |
| Pass/witness manifest | All three source-pass hashes and the frozen-witness hash equal the matrix's exact manifest references |
| Admission/proof qualifiers | Every row says recipe proof NOT_PERFORMED_BY_DESIGN_ROUTING, machine admission UNCHANGED_EXACT_BASELINE_ONLY and production NOT_ESTABLISHED_BY_THIS_DESIGN. Only Wish has NEEDS_PO_SP14_FOR_ROLL_REDO |
| Encoding | Final candidate/evidence/control package text has zero U+FFFD and zero disallowed controls; no corruption inference from Cyrillic terminal rendering |

The producer code validates the pinned normalized inventory, all body witnesses, exact reviewed roster and qualified manifests before deriving routes. Original-extraction versus frozen-witness reproduction was reported by the coordinator; this critic independently checked the resulting hashes and producer source, and did not execute that writing producer. Frozen spans intentionally include their recorded layout/contamination/tail basis. A matching body hash is not primary visual verification or permission to import that span as a recipe.

Final candidate snapshot: LF UTF-8 SHA-256 `33116b918af862371eb3b54f393bfe31233d0194dac71dc2e221364704520b75`. Decision Brief: `421920a6cd5730278f2f02623ffa824968a669a0353636a26f38eb944e32b718`. The resolution ledger's earlier "final re-read pending" rows describe pre-verdict repair state; the coordinator must synchronize those dispositions and actual global routing with this final review during authorized publication.

## Final verdict and remaining action

**DECISION-READY PROPOSAL.** The significant technical repairs are sufficient at architecture-candidate scope. No open technical finding and no genuine additional residual product/architecture judgment was found in this bounded whole-project review. The proposal can be published as a reviewable candidate with the concrete Decision Brief and NEEDS_PO route. It cannot be represented as accepted canonical architecture or full339 production support.

| Remaining item | Actual owners | Required action and boundary |
|---|---|---|
| SP-14 Wish Roll Redo - NEEDS_PO | Step-5.9 chronology/reconciliation; Step-3 accepted execution/RNG; Information; native durability/WP16 and affected owner closure | Human accepts the narrowly scoped published-rule reality exception and its consequence-closure risk, or explicitly accepts omission/scope concession. Original evidence stays immutable; one coherent replacement current reality, exact recent-round frontier and selected WP16 route remain required. Until that judgment, dependent canonicalization/implementation and complete339 support claim remain held |
| Candidate/control publication and review disposition | Owning HDM design process; PRODUCT_OWNER_INPUT_PROCESS; CURRENT_PROGRESS; project routing and existing plan/cursor owners | Coordinator synchronizes this verdict, repair ledger and concrete PO route; preserves prior accepted work and independently eligible lanes; fresh-reads/verifies authorized remote publication. This critic has not verified proposed global control edits or the coordinator's control tests |
| Later acceptance/materialization | Exact affected semantic owners, consumer/admission/package owners and existing stable implementation-plan process | After the real SP-14 decision, formalize selected owner amendments, complete Step 8 with required propagation/verification/publication/read-back, obtain independent Senior Review Stop 2, then reconcile the existing stable plan. Per-mode source/dependency/admission equality, real producer/native end-to-end and recovery proof, and actual WP24 measurements remain mandatory; none is discharged by this verdict |

There is no new PO gate for principal/body factoring, stochastic repetition, source reconstruction, exact casting costs, indexed counters, reaction payer or routine technical owner materialization. Current GAME law and accepted wave outcomes remain unchanged by this design review.
