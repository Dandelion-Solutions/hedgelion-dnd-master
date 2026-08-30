# ChatGPT Plus Host Evidence — Extracted R2.6 Research Evidence

Status: **RESEARCH EVIDENCE — NON-NORMATIVE**

SPLIT_FROM: `DEV/docs/superpowers/research/2026-08-24-r2-6-chatgpt-plus-assurance-evidence-ledger.md`

SEMANTIC_SOURCE_RANGE: `# 3. Current first-party ChatGPT evidence` — H1 through H8, ending before section 4.

CURRENT_AUTHORITY: NONE — EVIDENCE ONLY

This extraction preserves the point-in-time host evidence and its qualifications. Implementation-facing R2.6 law remains in the current canonical owners.

---

# 3. Current first-party ChatGPT evidence

## H1 — Projects provide stable project instructions and source files

Current first-party Projects documentation establishes that Projects are available on Plus, support project instructions, files and connected apps, and that project instructions apply inside the project and override global custom instructions.

Current Plus file limit is documented as 25 files per Project, with at most 10 uploaded at once.

R2.6 interpretation:

- current runtime-package-as-ZIP source shape is compatible with the documented Project file envelope;
- HDM must not turn the Project file limit into a campaign-data architecture constant because campaign canon remains in the campaign repository and runtime extraction/cache is local;
- project instructions remain instruction-layer input, not campaign authority.

Evidence class: **DOCUMENTED / current first-party**.

## H2 — Project memory can inject prior-chat context

Current Projects documentation establishes that Plus/Pro project chats may reference previous chats within the same project and prioritize project chats/files. Project-only memory can exclude outside-project memories/chats while still allowing context from chats in the same project.

R2.6 interpretation:

> Project memory is an ambient physical-context source and MUST NOT become campaign authority, currentness evidence, Actor knowledge, disclosure evidence or a substitute for repository retrieval.

This is not a contradiction of the single-context amendment: physical availability does not make content logically eligible. It does create a production-like contamination channel that Protocols 1-3 did not explicitly label as Project-memory-originated evidence.

Required new assurance probe: stale/foreign-project-chat style facts physically available through project history must lose to current routed repository owners and role eligibility.

Evidence class: **DOCUMENTED host behavior + ASSURANCE REQUIRED**.

## H3 — Plus exposes High reasoning but exact serving identity is not stable enough for campaign semantics

Current GPT-5.6 documentation establishes for Plus:

- Medium and High reasoning are available with GPT-5.6 Sol;
- Extra High and Pro are not Plus baseline options;
- if a GPT-5.6 reasoning allowance is reached, ChatGPT may continue with another available reasoning model;
- model availability and limits are product/plan dependent and can change.

R2.6 interpretation:

- owner-selected High remains a valid **recommended working profile** when available;
- campaign semantics/persistence SHALL NOT require exact model identity or identical reasoning selection across multiplayer participants;
- a shared campaign-level model identity would become stale/false under documented fallback behavior;
- S53 should be resolved as a minimum supported behavioral/capability envelope plus a recommended profile, not exact serving equality.

Evidence class: **DOCUMENTED / current first-party + Protocol-3 supporting evidence**.

## H4 — Consumer ChatGPT does not expose a stable remaining-context telemetry contract

Current first-party ChatGPT documentation reviewed for R2.6 does not establish a stable consumer API for exact remaining context/token capacity available to the conversation at each turn.

The public API model context-window value is not a consumer ChatGPT contract and SHALL NOT be copied into HDM as a runtime constant.

R2.6 interpretation:

- R2.3 central budget estimation remains necessarily conservative/approximate;
- correctness must use representation floors, `ASSEMBLED_DEGRADED` and `UNSATISFIABLE`, not assumed exact spare tokens;
- assurance should measure failure behavior under pressure rather than certify one permanent quota.

Evidence class: **NEGATIVE DOCUMENTARY FINDING / limitation**.

## H5 — App permissions can introduce user-confirmation latency, but repeated approval can often be reduced

Current first-party Apps documentation establishes that app permissions can require approval before reads/changes/important actions. Depending on the account/action, approval choices may include one-time approval, lower-risk auto-approval and `Always allow`; a `Never ask` policy may also be available in some configurations.

R2.6 interpretation for the **fixed Connector path only**:

- approval behavior is host configuration, not gameplay authority;
- a required approval can pause a persistence boundary but cannot change fictional order, replay mechanics or authorize force publication;
- ordinary low-latency gameplay may recommend the least-interruptive owner-accepted permission available for the installed Connector, but correctness cannot assume confirmation is absent;
- R2.6 does not compare another Git transport to avoid approval latency.

Evidence class: **DOCUMENTED / current first-party**.

## H6 — Retry/regeneration and chat branching exist, but no machine-readable ancestry contract is established for HDM

Current product documentation exposes response retry/regeneration and chat branching user features. The reviewed ordinary-chat documentation does not establish a stable machine-readable Retry/Edit/branch ancestry primitive that HDM can use as campaign authority.

This matches Step-5.12:

- Retry/Edit/branch is not campaign rewind;
- accepted mechanics/world state are not replayed merely because host history changes;
- absence of cheap exact ancestry remains tolerated.

D15 trigger status: **NOT FIRED** by documentary evidence alone.

Evidence class: **DOCUMENTED feature existence + NEGATIVE contract finding**.

## H7 — No first-party ordinary-Chat contract establishes byte-exact pre-render interception of the final assistant message

The reviewed first-party consumer documentation does not expose a programmable ordinary-Chat hook equivalent to:

```text
generate final assistant bytes
-> deterministic external validator edits/rejects those exact bytes
-> only then make those exact bytes visible
```

The current host can execute tools before a final assistant response, and R2.4 supplies logical role rebinding and typed gates, but this is not the same claim as a documented byte-exact post-generation renderer/outbox hook.

R2.6 consequence:

- do not claim stronger physical staging than evidence supports;
- test whether the accepted single-context topology plus pre-emission eligibility/disclosure gating and Narrator behavioral containment provides an **equivalent safe material-output boundary** for the supported profile;
- if production-like probes demonstrate a material disclosure failure that cannot be fenced without a stronger host primitive, this becomes a deployment blocker / explicit architecture reopen under Step-5.14, not a reason to silently weaken disclosure law.

Evidence class: **NEGATIVE DOCUMENTARY FINDING / potentially blocking assurance question**.

## H8 — The configured GitHub Connector surface currently supplies the fixed operations HDM needs

Current connected-tool capability in this development environment exposes authenticated repository read/search/permission functions and Git-data/ref mutation primitives including the fixed campaign path's `create_tree`, `create_commit` and non-force `update_ref` operations.

Current development work on the active branch has also successfully used authenticated Connector writes.

Prior HDM feasibility experiments established:

- deterministic Python can cheaply freeze/hash exact publication payload identity;
- Connector Git-data operations can preserve coherent tree/commit/ref semantics;
- non-force ref transition acts as the final optimistic-concurrency guard;
- the Connector is not a transparent push of a locally created commit/object database.

R2.6 consequence:

> repository transport selection is closed. Assurance asks whether this exact fixed path remains usable under final R2.1-R2.5 failures/races, not what else could write GitHub.

Evidence class: **CURRENT EMPIRICAL CAPABILITY + retained HDM experiment evidence**.
