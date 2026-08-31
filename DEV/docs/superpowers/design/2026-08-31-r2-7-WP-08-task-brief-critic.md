# R2.7 WP-08 — Task-Brief Critic

Status: **STEP-1 WHOLE-PROJECT CRITIC REPAIR PASS AFTER SENIOR HOLD — REPAIRS APPLIED**

## Mandate

This critic independently challenged the WP-08 Task Brief against current R2.7
scope, accepted role/context owners, current shipped instruction surfaces, machine
contracts and direct upstream/downstream dependencies. Its purpose is to expose an
incorrect boundary, duplicate authority or missing consumer before Step 2.

## Findings and repairs

| ID | Finding | Severity | Repair in final Task Brief |
|---|---|---|---|
| C01 | A role/context audit could silently assume a new physical multi-call, prompt framework or persistent role-state design. Those are rejected/non-goal architecture unless a current owner proves a required mapping. | SIGNIFICANT | Added explicit non-goals: no new physical topology, provider/API, prompt DSL, role bus, worker or default durable role/context records. |
| C02 | The Step-4 base specification contains older physical-isolation language. The later single-context amendment and R2.4/R2.6 ownership are required to interpret the current law correctly. | BLOCKING | Added the amendment, R2.4 and R2.6 as superseding/current canonical sources; the brief now states behavioral containment in one physical context, not a physical-isolation requirement. |
| C03 | Full preloaded CORE, semantic module activation and role-local eligible evidence are three different mechanisms. Treating them as one context would erase the central logical-eligibility boundary. | BLOCKING | Added `PLAY_POLICY.md`, `CORE_INDEX.md`, R2.3/R2.4 and explicit failure probes for cache/activation/bundle conflation. |
| C04 | R2.5 participant envelopes, catch-up and Dramaturg planning can inject cross-player/planning material into Narrator-adjacent paths without becoming evidence. Omitting R2.5 would make the critic module-local. | SIGNIFICANT | Added R2.5 as a direct canonical downstream constraint and added participant/recipient/generation-scoped handoffs to scope and failure probes. |
| C05 | R2.6 requires an explicit runtime instruction equivalent to the containment/lawful-later-uptake law, while WP-07/F06 records the same remaining implementation obligation. A brief restricted to abstract role diagrams would miss the current CORE/Project Instructions mapping. | SIGNIFICANT | Added the WP-07/F06 carry-in, `PROJECT_INSTRUCTIONS.txt`, current CORE surfaces and a required single-owner instruction mapping. |
| C06 | Chronicler and Narrator share the role/context domain but have different authority/output boundaries. Without Step-5.10 and Step-5.12, a later audit could treat Story drafts or delivery surfaces as ordinary role handoffs. | SIGNIFICANT | Added both canonical neighbors, `EMISSION_COMMIT`, Story non-authority and auxiliary-surface safety to the manifest and required proof. |
| C07 | The task-local audit cursor still names the pre-GO WP-07 checkpoint. Using it as a global authorization source would block or misroute WP-08. | MINOR | Recorded that current progress is the sole global authority. No WP-07 cursor/closure edit is warranted or made. |
| C08 | The canonical-owner manifest used bare filenames and therefore relied on an implied historical location. A Step-2 reader could open a noncanonical artifact or miss the primary owner entirely. | BLOCKING | Replaced canonical-owner filenames with exact current `DEV/docs/superpowers/specs/` paths and made other named Source Manifest surfaces explicit where a concrete file is cited. Each listed canonical primary source was opened on the published parent ref before repair. |
| C09 | R2.1 continuity/history and R2.2 Actor continuity/cognition were absent as direct WP-08 constraints. That omission leaves source escalation, hidden-reasoning exclusion, Actor purpose and the Actor-private versus `world.knowledge` boundary untested. | BLOCKING | Added R2.1/R2.2 exact canonical paths, Step-2 inspection scope, proof-record fields, exit criteria and adversarial probes for those boundaries. |

All BLOCKING and SIGNIFICANT framing defects are repaired in the final Task Brief.
No finding requires a semantic change to the accepted R2.3/R2.6 one-context model,
WP-07 closure, R2.5 collaboration model, or any compatibility policy.

## Whole-project dependency route checked

| Route | Critic disposition |
|---|---|
| R2.7 current progress, scope discovery, task brief, execution protocol and project map | retained as stage/process/routing authority |
| R2.1 continuity/history | retained as a direct source-escalation, eligibility and no-hidden-reasoning constraint; no continuity redesign admitted |
| R2.2 Actor continuity/cognition | retained as a direct Actor-purpose and source-Actor-private versus `world.knowledge` constraint; no cognition redesign admitted |
| Step-4 base owner, single-context amendment, R2.3, R2.4 and R2.6 | retained as the central semantic and assurance source chain |
| R2.5 collaboration/catch-up/planning | retained as direct recipient/role-context consumer; no R2.5 redesign admitted |
| Step-5.10 Story and Step-5.12 delivery/disclosure | retained as bounded neighboring owners for Chronicler and Narrator/output |
| WP-07 Step-8/F06 | retained as closed upstream implementation input; no re-opened information audit |
| Project Instructions, PLAY_POLICY, CORE_INDEX, RUNTIME, AI_REASONING and role-facing CORE modules | retained as current shipped instruction/runtime surfaces |
| current/session/player schemas and runtime/test/audit surfaces | retained as machine/test evidence only; no presumption that they must persist role control |
| unrelated domain mechanics, broad storage topology, migration, release and deployment detail | excluded except when a concrete role/context consumer edge is discovered; their owners remain later WP domains |

## Required Step-2 attacks

Step 2 must specifically test:

- whether the installed instruction surfaces express one consistent active-role,
  bundle and typed-handoff contract without duplicating authority;
- whether preloaded physical CORE can be separated operationally from role-local
  eligibility and from semantic module activation;
- whether any existing schema/session/cache/trace could become an accidental durable
  role-context, disclosure or currentness owner;
- whether Interpreter/Dramaturg/Actor/Chronicler/Narrator/Commentator transitions
  preserve minimum typed handoff and recipient/subject/generation bounds;
- whether `UNSATISFIABLE`, degraded assembly and protected Narrator output remain
  finite/non-leaking under the current instruction/runtime route;
- whether R2.6’s explicit containment/lawful-uptake instruction and WP-07/F06
  have one exact implementation destination and appropriate regression/MVP evaluation
  mapping;
- whether R2.1 continuity/history use keeps role/subject/recipient eligibility,
  performs proper-source escalation for material current/exact claims, and excludes
  hidden reasoning, prompts and unaccepted generations from continuity evidence;
- whether every Actor cognition use has an explicit R2.2 purpose and bounded eligible
  evidence/current state, preserves source-Actor-private continuity, and does not
  duplicate or mutate `world.knowledge` through the Actor path;
- whether Story, planning, trace and auxiliary output remain non-authoritative and
  do not leak into Narrator/player-visible output.

## Decision and gate

No product-semantics, authority-change, compatibility-policy, scope-change or
risk-acceptance decision is exposed by Step-1 framing.

**Critic verdict: PASS.** The repaired Task Brief is review-ready. Step 2 and all
later work remain blocked pending the mandatory Senior review.
