# R2.7 WP-10 Recovery Completion — Step 6 Independent Adversarial Critic

Status: **RECOVERY-COMPLETION STEP-6 COMPLETE — STEP-7 RESOLUTION REQUIRED**

## Independent dependency reconstruction

This critic did not rely on the candidate alone. It reconstructed the relevant
subgraph from PROJECT_MAP and the task Source Manifest: R2.1 continuity/history;
R2.2 Actor continuity; Step-3 execution boundary; Step-4 truth/knowledge;
Step-5.3 temporal, Step-5.9 chronology, Step-5.10 Story, Step-5.11 transcript,
Step-5.12 delivery; R2.5 multiplayer; WP-09 no-record controls; GAME schema,
storage, session and campaign-identity consumers; and DEV runtime/effect
contracts. Original and first-recovery critics remain historical evidence only.

Severity is the impact if the attack were admitted. “Candidate safe” means the
accepted Alternative-A allocation rejects the mechanism; it does not claim a
physical realization has been built.

| ID | Attack / failure mechanism | Affected owner / consumer | Primary evidence | Candidate result | Severity / classification | Human decision |
|---|---|---|---|---|---|---|
| A01 | Write a current epistemic stance into PC/NPC/faction knowledge fields and treat a named field as authority. | world.knowledge; PC/NPC/faction schema consumers. | Step-4 owner; R2.2-2; GAME PC/NPC schemas. | Rejected: one subject/fact knowledge relation; legacy fields are not a second writable owner. | BLOCKING / false-authority attack; candidate safe. | NO |
| A02 | Infer B-to-A relationship state when A-to-B changes, or store one symmetric edge for convenience. | Source Actor relationship views; Actor cognition consumer. | R2.2-3 and R2.2-8–11. | Rejected: each directed source/target view is independently owned; no reciprocal state/objective fact inference. | BLOCKING / symmetric-relationship attack; candidate safe. | NO |
| A03 | Use an Actor condition/effect list as the universal current effect/application record, then let the list stand in for an independently lifecycled application. | Natural effect/application; mechanical condition aggregation. | Activity/Asset/effect owners; DEV world-effect-state schema; DEV mechanical-surfaces derived condition aggregation. | Rejected: natural owner-local application remains authoritative; lists may be derived/projection only. | BLOCKING / effect-list-surrogate attack; candidate safe. | NO |
| A04 | Store Interaction, IntentPlan, Command, Procedure, Resolution or Continuation in SESSION/CHECKPOINT merely because it helps resume. | Step-3 lifecycle members; GAME Session/checkpoint consumers. | Step-3 canonical execution boundary; GAME CORE SESSION; checkpoint contract. | Rejected: member lifecycles remain separate; checkpoint is sparse recovery descriptor and Session is bounded coordination. | BLOCKING / lifecycle-collapse attack; candidate safe. | NO |
| A05 | Turn MechanicalEvent, receipt or ResolutionTrace into mutable current state, or conflate MechanicalEvent with the semantic event log. | Step-3 immutable evidence; event/log consumer. | Step-3 execution boundary; GAME event schema and LOG template. | Rejected: evidence members are immutable and distinct from current world state and semantic history. | BLOCKING / evidence-authority attack; candidate safe. | NO |
| A06 | Persist Agenda as the owner of TemporalBinding or give it a universal binding record. | Native temporal owner; Agenda consumer. | Step-5.3 temporal canonical spec and temporal-agenda amendment. | Rejected: binding remains natural-owner-local; Agenda is derived with no independent family. | BLOCKING / temporal-owner transfer; candidate safe. | NO |
| A07 | Treat Message as proof of disclosure/read receipt, or treat disclosure as objective truth/knowledge. | runtime.message; runtime.disclosure; delivery consumer. | Step-4 owner; Step-5.11 transcript; Step-5.12 delivery/disclosure. | Rejected: message, disclosure and knowledge retain distinct authority, mutation and retention contracts. | BLOCKING / delivery-authority collapse; candidate safe. | NO |
| A08 | Treat Story as current canon/recovery authority, or put runtime-local R2.3/WP-09 source basis into Story provenance. | Story projection; current owners; Context Runtime. | R2.1-1–13; Step-5.10; WP-09 canonical no-record. | Rejected: Story is optional, lagging, noncanonical and source-bound; runtime-local source basis has explicit no campaign record. | BLOCKING / projection-authority and persistence attack; candidate safe. | NO |
| A09 | Create collaboration or Dramaturg campaign roots for every campaign, including no active collaboration or single-player play. | R2.5 collaboration and planning projections; multiplayer consumer. | R2.5 canonical spec; Step-2 reclassification correction. | Rejected: collaboration is trigger-conditional; Dramaturg is dormant single-player and conditional multiplayer-only. | SIGNIFICANT / conditionality breach; candidate safe. | NO |
| A10 | Make the documentation namespace a central registry/service that owns member membership, mutation or recovery. | All Alternative-A members; runtime consumer. | Step-2 accepted decision brief; Step-3 decision; Step-4 candidate. | Rejected: namespace is traceability grouping only; each member remains primary-owner controlled. | BLOCKING / invented-subsystem attack; candidate safe. | NO |
| A11 | Pick a root, shard scheme, HOT store, schema, migration or bootstrap sequence from the logical matrix. | WP-11/12/19/20 downstream owners; storage/bootstrap consumers. | WP-10 Task Brief scope boundary; GAME STORAGE/PERSISTENCE. | Rejected: all physical realization remains downstream; candidate has no such selection. | SIGNIFICANT / scope-leak attack; candidate safe. | NO |
| A12 | Put any unmapped concern in MANIFEST, CONFIG, CURRENT, CARD, INDEX, LOG, SESSION or CHECKPOINT because an existing file is convenient. | Campaign metadata/current/checkpoint/index/log consumers. | WP-10 Task Brief mandatory probes; GAME STORAGE, SESSION, CAMPAIGN_IDENTITY. | Rejected: those surfaces retain their own narrow authority/projection roles; missing a named template is not allocation permission. | BLOCKING / convenience-surrogate attack; candidate safe. | NO |
| A13 | Treat template/schema omission as proof that a semantic owner is absent, or treat a DEV schema as shipped campaign persistence. | GAME scaffold and DEV schema consumers. | WP-10 Step-2 evidence and Task Brief Source Manifest. | Rejected: machine absence is coverage evidence only; owner law controls; DEV contracts are not shipped format. | SIGNIFICANT / machine-to-architecture inference attack; candidate safe. | NO |
| A14 | Conflate campaign branch canon, storage defaults, local template and runtime cache; then update the wrong surface. | STORAGE/BOOTSTRAP/PERSISTENCE consumers. | GAME STORAGE, PERSISTENCE, NEW_CAMPAIGN/Session route in Source Manifest. | Rejected: branch, storage metadata, template and cache have distinct lifecycles; matrix gives none new authority. | BLOCKING / lifecycle/location conflation; candidate safe. | NO |
| A15 | Persist R2.4 proposals, hidden reasoning or host/chat memory as a campaign record to make recovery feel complete. | R2.4/WP-09 controls; trace/evidence consumer. | R2.1-8; R2.2-12; Step-3 trace boundary; WP-09 no-record. | Rejected: hidden reasoning and unaccepted material are excluded; traces are bounded admitted diagnostics; host memory has no campaign authority. | BLOCKING / prohibited-persistence attack; candidate safe. | NO |
| A16 | Treat index/cache/card/discovery metadata as exhaustive negative proof or writable semantic owner. | R2.2 discovery; CURRENT/index/card consumers. | R2.2-22–25; WP-10 Task Brief; GAME index/card contracts. | Rejected: derived surfaces are locator/projection only unless their own contract proves current exhaustive scope. | SIGNIFICANT / derived-surface authority attack; candidate safe. | NO |
| A17 | Replace a stale-looking scaffold field without owner, supersession and consumer evidence. | Existing GAME campaign/schema consumer. | WP-10 Task Brief pre-release rule; GAME PERSISTENCE path-preservation barrier. | Rejected: clean-slate authorization is not automatic replacement authority. | SIGNIFICANT / unsupported-supersession attack; candidate safe. | NO |

## Critic conclusion

All pre-existing recovery probes are re-run as concrete attacks, including the
two formerly untested probes A02 and A03. No attack produced an unaddressed
semantic contradiction, compatibility policy choice, scope transfer or risk
acceptance. Step 7 must still record the explicit no-finding resolutions before
Step 8 can cite this critic as operative.
