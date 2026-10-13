# SP03 original-input / common-turn bridges — Step1 framing and Stop1

Status: **STEP1 ACCEPTED / INDEPENDENT SENIOR STOP1 GO; STEP2 NEXT**
Source basis: `afca759c38480f0e4a5629236b08c9d401ecd10d`
Scoping agent: `ses_ec94c1ab6ffef3CBfyUt6EWwTh`
Independent Senior: `ses_ec97befd4ffeCwmiiZnavkhK4O`
Date: 2026-10-13

This records two separately dispositioned technical briefs and their independent
framing review. No representation, implementation, positive original-author or
common-turn permission, full SP03 readiness or production activation is accepted.
Their affected System-Impact edges remain ARCHITECTURE_REVIEW_REQUIRED during
design. NEEDS_PO: NONE presently established. VERSION_IMPACT: NONE.

## Brief A — original accepted input authorization

Problem: native command/Interaction/IntentPlan/clause/Player strings establish
links, not the authenticated external account that originated accepted input.
Current publisher, actor_id, verified DTO flags and authorize(gameplay) alone
cannot substitute. Preserve the historical accepted basis and compose applicable
current authorization without replaying settled work.

Scope/exit: one finite original-input chain and actual trusted acceptance issuer;
recoverable campaign/session/input/invocation/account basis; current unique active
Player/control and separate creator-history singleplayer; exact relational and
currentness checks; retry/continuation/offer/recovery, dependency protection,
discharge and unavailable outcomes. No presupposed new port/store/record or
unallocated ordinary-path model/network work. Security, bounded reads, privacy,
idempotency and deterministic recovery are required quality attributes.

Accepted constraints:
- Interaction owns invocation/message/authenticated context; exact transport retry
  reuses accepted identity, later intentional identical prose is new input.
- Command/Interaction/plan/clause links are reciprocal and exact, with a unique
  matching clause; clause.command_id, when populated, must equal the command ID.
  Campaign/session/input identities and Player envelope/state equality are checked.
- Multiplayer uses the current bounded complete account route and exact reload
  for unique active Player plus intentional controlled PC. Loading only the
  Interaction-named Player does not prove uniqueness or original authorization.
- Original provenance remains historical; current mutable control must be
  reacquired. Revocation neither rewrites old accepted actions nor preserves
  permission for new protected work.
- Creator singleplayer without Player remains separate: native first campaign
  initialization history plus current authenticated creator login. Stable account
  ID is not creator authority; accepted login-rename failure stays read-only.
- Trusted composition may supply an adapter; domain/model data cannot select it.
  An arbitrary-Python pseudo-token/registry does not prove external input origin.

Required cases: valid original multiplayer author; foreign campaign/session/input/
invocation; mismatched plan, duplicate/missing clause, wrong command; inactive/
duplicate/rebound Player and removed/transferred PC; strings/flags/current publisher
as false substitutes; exact retry vs later identical intent/edit/branch; cold
durable resume after handle loss/control change; no-Player creator and rename hold.
Separate new intentional input, exact retry/duplicate recognition, cold inspection,
continuation with further protected mutation, fresh Choice/Reaction response, and
controller change during open work. Do not require every current executor to equal
the old author or permit any current publisher to continue any command.

## Brief B — shared caster gate and Procedure occurrence

Problem: concrete Procedure phase/index/budget and Actor progress shape do not
prove current-turn occurrence, common immutable gate definition, initialization/
reset or accepted slot-spend cause.

Scope/exit: exact common definition/key/subject, Procedure-owned occurrence issuer
or owner-proven derivation and bounded recoverable evidence; native Actor progress;
lawful first-use/reset/consume branches; later atomic producer/recovery obligations
separate from read-only SP03 proof. One native state authority, deterministic retry,
bounded enrollment and no fabricated occurrence are required.

Accepted constraints:
- One caster gate across sources; another creature's turn stays that actual turn.
- Slotless/ritual/countered/interrupted-without-slot do not consume. Long casts
  consume only at the actual accepted slot boundary, not preparation/start alone.
- Immutable definition fixes native owner/subject and transitions. Gate state is
  Actor-native progress, not relocated generic Procedure state or cast-history truth.
- Procedure owns turn/initiative/budgets; boundary producer establishes occurrence.
  Same timing value, unrelated revision/restart/save/absorption is not new occurrence.
  A derived key is allowed only with lifecycle-proven uniqueness and causal linkage.
- Native cause, resource expenditure and gate mutation share lawful later segment
  closure. Read-only evaluator never initializes/resets/spends or issues receipts.
- Missing definition/progress/occurrence is a hold, never inferred consumed=false
  or an unused gate. Required causal
  dependencies remain boundedly reconstructible while consumers need them.

Required cases: exact active combat subtype; generic/malformed permutation/budget/
index/phase or wrong participant; caster reaction on another creature's turn;
second slot through another source; every no-slot/long-cast branch; missing/forged/
wrong producer/scope/cause; retry vs distinct Procedure/equal round/index vs actual
next turn; crash around reset/spend; termination/provider movement; cold recovery
or LIVE movement after old details compact. Ordinary subject witness does not
equate split principal/body/source/payer or create a second gate.

## Primary manifest and current evidence limitations

All locators below refer to inspected afca759c bytes; later source-only/cursor
commits do not refresh or broaden these claims. `S/` abbreviates
`DEV/docs/superpowers/specs/`, `D/` abbreviates `DEV/docs/superpowers/design/`.
Status/index/map are routing, not semantic authority. Reads support only framing;
candidate-sensitive closure remains Step2 work.

| Role | Primary inspected route / scope |
|---|---|
| Process | AGENTS/runtime overlays, SKILL_SCOPE; DEV/DESIGN_PROCESS §§3–6,10–19; HDM adapter; execution process200–264 |
| Allocation | Stable Wave05 SP03; D/2026-10-08-sp03-capability-cast-source-allocation-ruling.md |
| Execution | S/2026-10-04-local-spell-execution-contracts.md; S/2026-08-19-step-3-execution-boundary-canonical-spec.md, full |
| Lifecycle | S/2026-10-04-local-spell-lifecycle-contracts.md §§1–8 |
| Security | DEV/ARCHITECTURE/ACCESS_CONTROL.md; S/2026-09-03-r2-7-WP-16-multiplayer-access-control-live-state-canonical-spec.md; S/2026-09-06-hdm-creator-login-continuity-owner-decision.md |
| Host | D/2026-09-21-w04-runtime-host-ordering-route-owner-decision.md; stable Wave04 host route |
| Recovery | S/2026-08-20-step-5-4-host-lifecycle-session-handoff-canonical-spec.md; S/2026-08-20-step-5-7-checkpoint-recovery-protocol-canonical-spec.md §§1–7 |
| Retention | S/2026-08-21-step-5-11-transcript-history-retention-compaction-canonical-spec.md §§1–20; S/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md448–498 |
| Temporal | S/2026-08-20-step-5-3-temporal-pending-continuity-canonical-spec.md §§1–14; Step5.3/5.9 amendment; Step5.9 chronology spec; S/2026-09-03-r2-7-WP-15-temporal-owners-processes-chronology-canonical-spec.md §§1–15 |
| Input schemas | runtime-command, runtime-interaction, runtime-intent-plan, intent-clause, world-player, runtime-message state schemas |
| Turn schemas | combat-minimal-procedure, generic runtime-procedure, boundary-occurrence, temporal-binding, world-actor state; native-profile progress values |
| Runtime reads/issuer | runtime_host55–149,1675–1966,2483–2733; activity_contracts560–685; spell_cast184–254; current_owner192–336; native_storage14–159; runtime_execution78–90,1045–1208 |
| Access/history | access_control88–146,344–623; history1334–1513 |
| Actual turn consumers | temporal498–518; actor_continuity359–391; DEV validate_domain_rules_coverage198–275 |
| Version/intent | Release version policy; detailed September5 owner §§1–3; applicable active PO ledger and accepted PO-013 |
| Inspected tests | runtime_host_composition1204–1358; rd09 access329–418; rd08 temporal162–225; no positive bridge/deployment claim |

Current root rejects Procedure in both host/contracts and enforces its exact read
set. Expanded source membership enforces that set plus covered Effects/Assets.
New infrastructure reads must not become unchecked extras or selector/write role
permission. Concrete DEV Procedure uses envelope `.state`, schema2 capacity/spent;
generic Procedure is a different shape. DEV state_changed event is not a turn issuer.
Optional Interaction auth strings, publication identity, structural VerifiedPrincipal
and existing gameplay authorization do not supply original-input proof.

OpenCode local tools provide source/Git evidence, not an attested deployed
participant-input/invocation feed. Trusted fixtures can prove deterministic TCB
contracts, not real supported-host authentication. Local unavailability does not
prove supported deployment impossible; missing indispensable deployment proof
holds the affected positive claim. No behavior/deployment test PASS is claimed.

## Independent Stop1 ruling and binding research additions

Senior Stop1 **GO for both briefs**: Step2 research/draft followed by the complete
eight-step process. Author's distinct framing critic was self-performed and is
not relabeled independent; Senior additionally challenged actual neighboring
recovery/retention/collaboration/host consumers. No blocking framing defect remains.

Retention: disposable handles can be reconstructed, but sufficient accepted
native provenance/causal basis must survive while protected consumers need it.
Neither a new standalone history family nor persistent BoundaryOccurrence is
mandated. Existing runtime.message remains a lawful evidence owner. No universal
per-message immediate publication or permanent verbatim retention follows; unresolved
pre-command recovery depends on actual applicable durability/handoff promises.
Hash equality alone does not authenticate or reconstruct missing content.

Step2 must additionally inspect:
- Step5.2 resumable closure laws2–13/§§4–6; WP14 recovery laws6–11,20–26;
- Step5.5/5.6, WP13 durability/publication and Step5.8/WP16 LIVE boundaries;
- Step5.14 cross-source protection laws2,5 with Step5.11/5.13;
- WP17 agency laws16–22,27,32–40 and material source-basis retention;
- R2.6 host-assurance spec, September21 host composition, WP16 law1 and actual
  supported adapter evidence; current official capability evidence only for the
  exact unresolved input/principal/invocation capability;
- WP11 physical identity/routing and WP12 HOT; actual recovery, recovery_roots,
  durability, publication, hot_store, live_state and implicated schemas/tests;
- input/message/Intent/command/Continuation/Choice/Reaction, runtime_execution,
  collaboration/history/context/turn/access/host; emission if message shape changes;
- full applicable version/clean-slate/WP20 law, and WP25/native failure owners;
- domain coverage, concrete Procedure transition/state and DEV conformance producer.

Specific mandatory challenges: recovery_roots568–603 requires Player and uses
input_message_id as Interaction root identity; reconcile no-Player and exact
message/Interaction roots coherently. recovery858–897 does not already prove the
new closures. Protection must precede or accompany dependency acceptance (or
equivalent admitted fence/self-containment), not eventual registration. Test
compaction/retirement racing acceptance/movement. Do not presuppose eager reset
of every Actor; exact finite owner-enrolled sets are lawful alternatives.

Before Step3, ledger each required primary source as inspected/applicable/
superseded/held, expand for any changed producer/consumer/protection/recovery field,
and map every case to requirement/source/carrier/producer/reader/recovery/proof.
Challenge opposing case, simplest viable representation, assumptions, races,
global impact and disconfirming evidence. Step3 Decision Brief then recorded
Step4: human decision YES/NO. Mechanically derived NO proceeds without artificial
PO pause; human owns actual agency/trust/deployment/security/compatibility or
material latency/availability/privacy trade-offs, not technical proofreading.

Independent fresh-context whole-project Step6 critic, Step7 propagation, Step8
canonical owner synchronization/verification/publication/read-back and independent
Senior Stop2 remain. Then reconcile stable implementation Envelope/plan and its
Senior GO. Neither Stop1 nor this record permits bridge implementation.

Independent read-only Procedure/budget and native command/Interaction/plan/Player
linkage conformance may proceed under the separate existing-owner allocation;
positive author authorization/common-slot permission stay held. Full SP03 output
is NOT_PRODUCED; SP04 is not pulled forward. No new PO question established.
