# HDM Platform Feasibility — Economic Profile Amendment

**Status:** RESEARCH INPUT — NON-NORMATIVE / NOT CANONICAL  
**Date:** 2026-08-22  
**Applies to:** `2026-08-22-platform-feasibility-comparative-research.md` and `2026-08-22-infrastructure-topology-options.md`

This amendment records a new distinction discovered after the initial consumer-host feasibility pass. It does not replace either owning research snapshot and does not change accepted HDM architecture.

---

# 1. Public baseline remains unchanged

The general HDM product target remains:

- ordinary individual AI subscription around the `$20/month` class;
- no Business/Enterprise dependency;
- no mandatory purchased agent credits;
- no separately metered inference requirement for ordinary public users;
- no hidden per-turn charge required for baseline correctness.

Consumer-host feasibility should continue to be judged against that target.

---

# 2. Add a distinct private owner-operated profile

The project owner has access to general-purpose hosting capable of running an HDM service, database and APIs. A separate private deployment profile is therefore allowed for research:

```text
small trusted group
       |
       v
private HDM server
├── authoritative database
├── deterministic mechanics
├── Context Assembler
├── role scheduler
├── memory / retrieval
├── multiplayer / identity
├── observability / budgets
└── direct model inference
```

For this profile, a deliberately bounded inference spend on the order of **`$10–20/month total`** is acceptable for personal play with a small number of friends.

The server is not assumed to be available to unlimited public users.

This is a different economics envelope from the public baseline and must not be used to weaken the baseline affordability requirement.

---

# 3. Infrastructure consequence

For hosted profiles with an HDM-owned authoritative database, GitHub is **not required as shared campaign state**.

Possible remaining GitHub roles are optional:

- export;
- backup;
- human-readable version history;
- portability;
- development/release source control.

The hosted service may use normal transactional database semantics for live state, concurrency, identity and recovery.

---

# 4. Direct commercial API inference is no longer rejected for the private profile

The original infrastructure research correctly rejected separately metered API inference as a **public baseline** dependency.

That conclusion should not be generalized to the new private owner-operated profile.

Current list-price reconnaissance shows that API cost varies by more than an order of magnitude between model tiers. A private campaign may plausibly fit the owner's `$10–20/month` target if HDM uses:

- bounded role-specific context;
- the minimum physical call graph compatible with isolation;
- cheaper models for structured/internal work;
- stronger models only where quality materially matters;
- prompt caching where measurable and reliable;
- bounded retries;
- hard monthly spend limits.

The exact feasibility claim remains **REQUIRES MEASUREMENT**. No model/provider is selected by this amendment.

Detailed calculations and current list prices are recorded in `2026-08-22-private-hosted-inference-economics.md`.

---

# 5. Self-hosted/open-weight inference becomes a preserved future branch

Cloud GPU rental makes another private profile technically plausible:

```text
HDM Server
   |
   +-- ordinary DB/core services
   |
   `-- ephemeral GPU inference worker
          `-- open/self-hosted model
```

The interesting economic shape is likely session-scoped/ephemeral GPU allocation rather than a 24/7 dedicated accelerator.

This path is **not ready for architecture selection**. Its dominant unknown is model suitability, not merely compute price.

Future work must evaluate:

- role-specific quality;
- narrative quality;
- structured/tool behavior;
- context reliability;
- latency and throughput;
- VRAM/model-size requirements;
- quantization trade-offs;
- concurrency;
- operational burden;
- whether any candidate base model already meets HDM needs.

Fine-tuning strategy is explicitly deferred. Do not assume training is needed before measuring concrete failures of plausible base models with an HDM-specific evaluation suite.

---

# 6. Repository privacy is not implied by private inference

Paying for inference on a private server does **not technically require** the source repository to become private.

Secrets must remain outside source control regardless of repository visibility.

Repository visibility is a separate future decision involving:

- distribution policy;
- licensing;
- possible commercialization;
- support expectations;
- whether public engine/client code and private deployment infrastructure should be split.

Possible future shapes include:

```text
A. public engine + private hosted deployment repository
B. fully private development repository
C. public source + privately operated service
```

No choice is made here.

---

# 7. Updated research priority

The feasibility program should now maintain three independent economics questions:

1. **Public baseline:** can ordinary users play without marginal inference charges beyond their consumer subscription?
2. **Private API profile:** can measured real HDM gameplay for a small trusted group stay within a hard owner-funded `$10–20/month` inference budget?
3. **Private self-hosted profile:** can an ephemeral open-model GPU deployment meet both that budget and the required HDM quality bar?

These questions should not be collapsed into one `cost` score.

The next meaningful evidence for questions 2 and 3 is a measured HDM role/call workload and role-specific model evaluation, not more abstract price comparison alone.
