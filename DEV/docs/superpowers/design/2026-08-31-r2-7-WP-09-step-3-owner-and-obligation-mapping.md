# R2.7 WP-09 Step 3 — Owner and Obligation Mapping

Status: **STEP 3 COMPLETE — REVIEW CANDIDATE NEXT**

## Decision record

Step 2 exposes no new product, authority, compatibility, risk-acceptance or scope
choice. The decision is therefore a disciplined allocation: retain the accepted
R2.3/R2.4/R2.6 logical law; make a narrow implementation-facing realization
mapping only if it adds non-duplicative enforceable allocation; defer physical
choices to their named owners.

## Finding-to-owner mapping

| Finding | Canonical semantic owner | Current supporting consumer | Required future realization / verification | Boundary |
|---|---|---|---|---|
| F01 — CORE cache differs from campaign working set | R2.3 context projection; R2.6 host constraint | `GAME/CORE/PLAY_POLICY.md`, `RUNTIME.md`, `STORAGE.md` | Keep full engine instruction cache separate from request/profile-scoped campaign packet. Test that scene/module activation never authorizes campaign preload. | No new cache/store; WP-12 physical derived-cache detail. |
| F02 — compact routing is not authority | R2.3 discovery/currentness/eligibility; Step 5.14 source basis | CURRENT/scene/location/index schemas | Discover by compact hints, then resolve routed current native owner and role eligibility before semantic use. Test an omitted/stale hint and a mobile entity/current-owner route. | WP-10 roots; WP-11 topology/partitioning. |
| F03 — profile floors/outcomes lack behavioural proof | R2.3 allocation/outcomes; R2.4 finite caller path; R2.6 estimator | `core-catalog.json` vocabulary only | Future behavioral acceptance evidence must show that runtime-local registered profiles produce required closure before optional material; a central conservative estimator chooses only legal representations; caller handles terminal `UNSATISFIABLE` by registered finite path. This selects no module, schema, catalog, storage design or implementation plan. | No durable control schema/catalog change in WP-09; no provider policy. |
| F04 — normal path must not scan campaign/history | R2.3 bounded discovery/history; R2.6 bounded operation | PLAY_POLICY/RUNTIME/STORAGE and existing latency cases | Preserve decision-scoped targeted reads; history escalation names typed dependency/source family/finite bound. Test no broad directory/history scan on an ordinary turn. | WP-24 measured scale, not a numeric target here. |
| F05 — mechanical/S6D context is a false substitute | R2.3 plus closed WP-08 role-context allocation | MechanicalContext schemas/tests | Keep mechanical invocation facts, continuation and resolution trace out of role-context authority and role-private continuity/control constrained by closed WP-08. Test/contract boundary is negative, not a data bridge. | Do not reopen WP-08; S6D remains independent. |
| F06 — DEV/package/CI are development machinery | R2.6 host/package assumptions; branch/package owners | install/bootstrap, BRANCH_MODEL, closure/audit/CI | Runtime reads only selected package/campaign scope. Tests/audits execute on development route, never as ordinary retrieval. | No DEV path becomes runtime source. |

## Representation and authority disposition

| Surface | Classification | Prohibited promotion |
|---|---|---|
| RoleContextRequest / ContextNeedProfile / RoleContextBundle / ContextTrace / ContextBudgetEnvelope | Existing runtime-local control contracts (closed WP-08 + R2.3) | durable campaign schema, generic cache, mechanical continuation, prompt-memory authority |
| CORE cache and loaded working set | ephemeral operational support | campaign/source basis or closed-world evidence |
| CURRENT / SCENE / LOCATION / INDEX | compact routing / current-scene support | semantic completeness, universal currentness or role eligibility |
| DEV catalog registrations | machine vocabulary | proof of behavioral implementation or runtime authority |
| MechanicalContext, continuation and resolution trace | deterministic mechanics state/derived trace | role source eligibility, role-private continuity/control or broad retrieval context |
| SQLite/HOT | existing physical/operational concern | format-implied authority or WP-09 physical choice |

## Verification allocation

The future implementation/release cycle must add behavior-level evidence, not merely
schema or catalog presence, for:

1. a registered consumer can request bounded required closure through legal
   discovery channels;
2. stale/index-only or role-ineligible evidence cannot enter the semantic bundle;
3. required legal floors survive pressure before optional ranking occurs;
4. only legal downgrade produces `ASSEMBLED_DEGRADED`;
5. an infeasible required packet produces terminal `UNSATISFIABLE` and one
   registered finite caller response, with no loop/guess;
6. operation proceeds without exact provider remaining-token telemetry;
7. normal path reads only decision-relevant routed sources and bounded history;
8. cache, index, trace, Context Runtime and MechanicalContext retain their
   distinct authority classifications.

These are obligations under existing accepted law. Their exact runtime module,
durable record family, sharding, HOT/SQLite mechanics and numeric evaluation
targets remain unselected here.

## Cross-domain routing

| Owner | Forward obligation |
|---|---|
| WP-10 | Decide only any necessary durable record/template roots after a concrete realization needs them. |
| WP-11 | Evaluate partition/shard topology only on its own scale/host evidence; no R2.3 trigger is present. |
| WP-12 | Realize any derived cache/HOT/SQLite mechanics without changing semantic authority. |
| WP-18 | Supply Story/Dramaturg consumers as registered role profiles without broad continuity preload. |
| WP-24 | Set numeric scale/latency evidence and measurement policy. |
| WP-25 | Integrate `UNSATISFIABLE` with wider failure taxonomy without changing R2.4 finite caller law. |

## Next logical step

Prepare a reviewable candidate mapping that can be challenged for false authority,
scope bleed, hidden telemetry and cache/index conflation. No human decision is
required before that review.
