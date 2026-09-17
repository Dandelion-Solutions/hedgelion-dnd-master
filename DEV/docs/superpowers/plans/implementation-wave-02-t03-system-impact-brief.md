# W02.T03 System-Impact Brief

TRIGGER: W02.T03 requires a trusted exact campaign publication/history policy resolver, but the current repository exposes only `DEV/TOOLS/validate_house_rules_mechanical_boundary.py`, a development conformance helper whose input contains caller-supplied authority/applicability booleans and source paths. Using that input at runtime creates a second policy/currentness authority.

LAST_SAFE_SHA: `f8a5166b3371e565e3d252fab5bbdd890f5f33d1`
CURRENT_TASK: W02.T03 - Exact accepted adjudication basis

APPROVED SPEC / PLAN EXPECTATION:
- `HOUSE_RULES_MECHANICAL_BOUNDARY.md` requires the existing campaign publication/history resolver to prove exact policy revision, normative/sidecar pairing, adoption authority, and applicability before command acceptance.
- W02.T03 must freeze the exact basis, enforce the two parameter plus seven fact consumer edges, and reject untrusted/missing/stale/inconsistent sources before mechanics.

DISCOVERED IMPLEMENTATION PRESSURE:
- No current GAME/runtime campaign publication/history resolver was found.
- The W02.T03 worker's raw `policy_sources`, `current_campaign_revision`, `authority_validated`, `applicable`, and source-path inputs admitted forged policy evidence and an unregistered active fact edge.
- Reusing the DEV conformance helper at runtime would change its trust boundary and create policy/currentness authority not admitted by the approved envelope.

AFFECTED OWNERS / CONSUMERS:
- W02.T03 `GAME/TOOLS/runtime_execution.py` acceptance boundary;
- campaign publication/history and House-Rules adoption/currentness owners;
- `HOUSE_RULES_MECHANICAL_BOUNDARY.md`, active consumer ledger, adjudicated parameter/fact contracts, and future T05/T06 publication/recovery consumers.

PROTECTED INVARIANTS AT RISK:
- no second policy/currentness/execution authority;
- exact historical policy basis, not caller booleans or latest policy;
- exact two-parameter plus seven-fact active consumer surface;
- retry/recovery never rebinds accepted adjudication input.

WHAT CAN PROCEED WITHOUT THE CHANGE:
- W02.T04 and W02.T07 may proceed only after their own fresh owner/write-set checks confirm they do not consume the unresolved accepted-adjudication basis.
- W02.T05 and W02.T06 remain blocked by their explicit dependency on W02.T03/T05 outputs.

SAFE OPTIONS:
1. Return to the applicable architecture/design owner to identify or authorize the native campaign publication/history resolver and its runtime boundary.
2. Authorize a bounded architecture amendment that states the resolver's authority, inputs, persistence/currentness route, and consumers before T03 implementation resumes.

RECOMMENDATION: resolve the native campaign publication/history resolver through the System-Impact/design route before resuming W02.T03. Do not normalize the DEV validator or raw caller evidence into runtime authority.

COST / RISK IF RECOMMENDATION IS WRONG: accepting forged or current-latest policy evidence can change mechanically accepted input on retry/recovery and establishes an unauthorized policy/currentness authority.

UNPUBLISHED_WORK: detached `/tmp/opencode/w02-t03` commit `29ded20` is unsafe T03 implementation evidence only; it is not integrated or published.

## Senior / Product-Owner-approved resolution — ACCEPTED 2026-09-18

Selected disposition: **bounded runtime trust-boundary realization; no new policy authority**.

The canonical House-Rules mechanical boundary now defines a production `PolicyBasisResolver` as a verifier/adapter over:

- exact pinned campaign revision H;
- RepositoryPort-equivalent exact commit/tree/path reads at H;
- the existing House-Rules sidecar + normative source owners;
- trustworthy acting-principal plus current creator/PLAYER policy-adoption evidence when required;
- the already selected compatible `BoundCatalogContext` for material `realization_refs`.

The result is ephemeral verified evidence. Only accepted `policy_id@H` refs plus the accepted parameter/fact values participate in RuntimeCommand identity. No persisted policy-proof registry, policy epoch, second ACL/currentness owner or policy engine is authorized.

Raw caller authority/applicability booleans, caller-selected source paths/revisions and `DEV/TOOLS/validate_house_rules_mechanical_boundary.py` are explicitly rejected as runtime authority.

Recovery reuses the frozen historical basis and does not rebind accepted work to current/latest policy or later grant state.

The detached prototype `29ded20` remains non-authoritative failed implementation evidence and must not be cherry-picked/integrated as-is. W02.T03 is unblocked for fresh implementation under the repaired stable plan.
