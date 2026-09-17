# W02.T04 System-Impact Brief

TRIGGER: W02.T04 needs owner-issued, lifecycle-validated operational-root enrollment/removal evidence. The current public `OperationalRoot`/`OperationalRootRouting` carriers are freely constructible, so caller-built before/after routes can forge membership or removal. Securing the boundary requires a change to command/procedure/promised-input lifecycle owner interfaces or a newly authorized owner-issued evidence boundary.

LAST_SAFE_SHA: `dcb39ddb697aea122a04f985780eeac01d29636a`
CURRENT_TASK: W02.T04 - Operational-root enrollment and routing contract

APPROVED SPEC / PLAN EXPECTATION:
- T04 requires typed, idempotent, campaign-scoped eligibility/enrollment/removal derived from active native work.
- T05 exclusively owns terminal-publication removal; T04 cannot create a journal, durability frontier, global queue, or second lifecycle authority.

DISCOVERED IMPLEMENTATION PRESSURE:
- Public carriers can be constructed with arbitrary roots or empty partitions and diffed into an apparent removal without any native lifecycle proof.
- Rejecting an ad-hoc mapping does not prove that the typed carrier came from an owner.
- The current Python/schema routes also disagree on same-kind/different-owner ID matching; this local drift is not repaired separately while the primary authority boundary is unresolved.

AFFECTED OWNERS / CONSUMERS:
- command, procedure, promised-input, publication and recovery lifecycle owners;
- T04 operational-root routing consumer;
- T05 terminal publication/removal and T06 recovery hydration consumers.

PROTECTED INVARIANTS AT RISK:
- no second lifecycle/recovery/currentness authority;
- no forged enrollment/removal or disappearance before T05 terminal-publication evidence;
- exact native owner identity rather than a cache/index/checkpoint/delta-derived authority;
- active-only bounded root routing with no global queue/journal/frontier.

WHAT CAN PROCEED WITHOUT THE CHANGE:
- W02.T07 may proceed only after its own fresh owner/write-set check confirms no dependency on operational-root routing or the blocked adjudication basis.
- W02.T05 and W02.T06 remain blocked by their explicit T03/T04 dependencies.

SAFE OPTIONS:
1. Return to the architecture/design owner to identify the native lifecycle proof interface that T04 may consume.
2. Authorize a bounded architecture amendment defining the lifecycle owner, proof shape, publication-removal handoff and recovery consumer semantics before T04 resumes.

RECOMMENDATION: resolve the native lifecycle proof authority through the System-Impact/design route. Do not use publicly constructible routing carriers as a substitute.

COST / RISK IF RECOMMENDATION IS WRONG: forged root removal can hide active accepted work from later recovery; a new ad-hoc proof carrier can silently become a duplicate lifecycle/currentness authority.

UNPUBLISHED_WORK: detached `/tmp/opencode/w02-t04` commits `0244a7b` and `14b061b` are unsafe T04 implementation evidence only; they are not integrated or published.

## Senior / Product-Owner-approved resolution — ACCEPTED 2026-09-18

Selected disposition: **materialize the already-accepted native lifecycle contract; no new lifecycle authority**.

Step 5.2 now constrains the W02.T04 realization:

- `runtime.procedure` exposes explicit owner-native `ACTIVE|TERMINAL` lifecycle semantics;
- only an accepted Procedure-opening transition creates ACTIVE and only an explicit typed Procedure close/reset/terminal transition creates TERMINAL;
- absence of open commands, Encounter/Scene status, routing membership or caller assertion cannot establish terminality;
- RuntimeCommand eligibility continues to derive from native accepted/settled disposition plus unfinished mandatory closure;
- operational-root deltas derive from exact validated native owner kind+identity+state; publicly constructible Python carriers are not authority;
- W02.T04 prepares derivative enrollment/removal evidence; W02.T05 owns the publication closure applying native terminal transition plus required root-membership mutation;
- unresolved Interaction/IntentPlan routing is admitted only when the durability/handoff owner supplies an accepted promise. T04 defines the eligibility/derivation contract and does not invent that promise.

The detached prototypes `0244a7b` and `14b061b` remain non-authoritative failed implementation evidence and must not be cherry-picked/integrated as-is. W02.T04 is unblocked for fresh implementation under the repaired stable plan.
