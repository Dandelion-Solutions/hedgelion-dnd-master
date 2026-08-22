# HDM Private Hosted Inference Economics — Research Snapshot

**Status:** RESEARCH INPUT — NON-NORMATIVE / NOT CANONICAL  
**Date:** 2026-08-22  
**Purpose:** record whether a private owner-operated HDM server using direct model APIs or self-hosted inference could be economically viable for a small trusted group without changing the public/no-marginal-cost product baseline.

This document is deliberately narrow. It does **not** select an LLM provider, model, fine-tuning strategy, hosting vendor, licensing model or repository-distribution policy.

---

# 1. Two economic profiles must remain separate

The research now distinguishes two different product/deployment questions.

## 1.1 Public / ordinary-player baseline

The existing baseline constraint remains unchanged:

- ordinary players should be able to use HDM with an individual consumer AI subscription in the approximate `$20/month` class;
- normal gameplay should not impose a separately metered per-turn charge;
- Business / Enterprise / `$100–200+` premium tiers, purchased agent credits, API bills and pay-as-you-go overflow are not baseline requirements.

This is the portability/public-access target.

## 1.2 Private owner-operated profile

A separate profile is now explicitly allowed for research:

```text
small trusted group
      |
      v
private HDM service
├── authoritative database
├── deterministic core
├── Context Assembler
├── multiplayer / identity
├── role scheduler
└── controlled model inference
```

For this profile the owner is willing to consider a **bounded total inference budget on the order of `$10–20/month`** for personal play with a small number of friends.

This changes the feasibility question from:

> Can API inference be completely free?

to:

> Can measured HDM gameplay fit inside a deliberately capped private operating budget without making the server publicly available to unlimited users?

The private profile is not permission to make paid inference a hidden requirement of the public HDM baseline.

---

# 2. Point-in-time API list prices

The following prices are current first-party list prices observed on 2026-08-22. They are **research evidence, not a provider recommendation**, and may change.

| Model | Input / 1M tokens | Output / 1M tokens | Notes |
|---|---:|---:|---|
| OpenAI GPT-5.6 Sol | `$5.00` | `$30.00` | frontier tier |
| OpenAI GPT-5.6 Terra | `$2.00` | `$12.00` | balanced tier |
| OpenAI GPT-5.6 Luna | `$0.20` | `$1.20` | cost-sensitive tier |
| Anthropic Claude Sonnet 4.6 | `$3.00` | `$15.00` | standard global list price |
| Anthropic Claude Haiku 4.5 | `$1.00` | `$5.00` | cheaper Claude tier |
| Google Gemini 2.5 Flash | `$0.30` | `$2.50` | standard paid tier |

Important pricing properties:

- input and output are billed separately;
- reasoning/thinking tokens may contribute to billed output/usage depending on provider/model;
- tool-specific features may add their own fees;
- prompt/context caching can materially reduce repeated stable-prefix input cost where supported;
- batch pricing can be lower, but batch is not a natural fit for latency-sensitive player turns;
- list price alone does not prove quality, latency or suitability for an HDM role.

---

# 3. Illustrative per-turn cost envelope

A measured HDM workload does not yet exist, so the following is only a **calculation envelope**.

Assume an intentionally conservative simple topology:

```text
3 model calls per player-visible turn
10,000 input tokens per call
1,000 output tokens per call
---------------------------------
30,000 input + 3,000 output tokens / turn
```

This is not a claim that HDM will need this many tokens. The purpose is to expose order of magnitude.

| Model used for all 3 calls | Approx. cost / turn | 100 turns | 300 turns | 1,000 turns |
|---|---:|---:|---:|---:|
| GPT-5.6 Sol | `$0.2400` | `$24.00` | `$72.00` | `$240.00` |
| GPT-5.6 Terra | `$0.0960` | `$9.60` | `$28.80` | `$96.00` |
| GPT-5.6 Luna | `$0.0096` | `$0.96` | `$2.88` | `$9.60` |
| Claude Sonnet 4.6 | `$0.1350` | `$13.50` | `$40.50` | `$135.00` |
| Claude Haiku 4.5 | `$0.0450` | `$4.50` | `$13.50` | `$45.00` |
| Gemini 2.5 Flash | `$0.0165` | `$1.65` | `$4.95` | `$16.50` |

This immediately shows why `one frontier model for every logical role on every turn` is a poor default, but **direct API inference itself is not automatically unaffordable**.

---

# 4. Mixed-model routing can change the economics by an order of magnitude

The six logical roles do not imply six frontier calls. HDM can potentially route physically compatible or lower-risk work to cheaper models and reserve a stronger model for the one role where quality materially benefits.

Illustrative mixed routing only:

```text
internal/structured work on a cheap model:
    16k input + 1.2k output total

player-facing strong call:
    10k input + 1k output
```

Using GPT-5.6 Luna for the cheap work and GPT-5.6 Terra for the stronger call at current list prices gives approximately:

```text
cheap work:    ~$0.00464 / turn
strong call:   ~$0.03200 / turn
--------------------------------
total:         ~$0.03664 / turn
```

Illustrative monthly totals:

- 300 turns: about `$11.00`;
- 500 turns: about `$18.32`.

Again, this is not a forecast. It demonstrates that the owner's target `$10–20/month` range is **plausible enough to justify measurement**, provided the real architecture keeps context bounded and does not run an expensive frontier model indiscriminately.

The opposite scenario is also clear: if every role receives a large context and uses a frontier model, the budget is easily exceeded.

---

# 5. What must be measured before treating API cost as acceptable

The research should not choose a provider from list prices. First build a realistic HDM call graph and instrument it.

Required measurements:

1. physical calls per ordinary turn;
2. physical calls per unusual/high-complexity turn;
3. average and p95 input tokens per role;
4. average and p95 output/reasoning tokens per role;
5. percentage of turns that need secret-bearing Actor/Dramaturg work;
6. cacheable stable-prefix size;
7. cache-hit rate under real campaigns;
8. latency per call and total wall-clock turn latency;
9. retries/failures and their token cost;
10. background Chronicler/enrichment cost;
11. multiplayer scaling: whether costs grow per player input, per resolved shared event, or both;
12. model quality per role, not only blended benchmark quality.

A private deployment should have:

- hard provider-side monthly spend cap where available;
- server-side per-campaign and global usage counters;
- alerts before budget exhaustion;
- no automatic cost escalation to a more expensive model;
- bounded retry policy;
- safe degradation when the private monthly budget is exhausted.

---

# 6. Private server access changes the abuse model

The owner-operated profile is feasible partly because it does **not** need unlimited public access.

A reasonable private research posture can use:

- explicit allow-list / invitation;
- small fixed user count;
- authenticated users;
- per-user/campaign rate limits;
- server-owned provider credentials never exposed to players;
- global monthly inference budget;
- hard concurrency ceilings.

Opening the same service to arbitrary public users would create a qualitatively different economic and abuse problem. That could require quotas, user-supplied billing, sponsorship, donations or commercial terms. None of those are current project requirements.

---

# 7. Self-hosted / open-weight cloud inference is a separate future path

Instead of paying per token to a commercial model API, HDM could eventually rent GPU capacity and run an open/self-hosted model.

This is **not** currently selected and should remain abstract until API-based role/cost measurements exist.

## 7.1 Current cloud-GPU order of magnitude

Current published on-demand rates show examples such as:

| Example GPU | VRAM | Approx. on-demand rate |
|---|---:|---:|
| RTX A5000 | 24 GB | `$0.27/hour` |
| A40 | 48 GB | `$0.44/hour` |
| RTX A6000 | 48 GB | `$0.53/hour` |
| L40S | 48 GB | `$0.99/hour` |
| A100 PCIe | 80 GB | `$1.39/hour` |

Illustrative compute-only monthly cost if the GPU exists only during play:

| GPU | 20 h/month | 40 h/month |
|---|---:|---:|
| RTX A5000 | `$5.40` | `$10.80` |
| A40 | `$8.80` | `$17.60` |
| RTX A6000 | `$10.60` | `$21.20` |
| L40S | `$19.80` | `$39.60` |
| A100 PCIe | `$27.80` | `$55.60` |

By contrast, a continuously running 24/7 GPU is generally far outside the `$10–20/month` personal target.

Therefore the interesting self-hosted shape is likely **ephemeral/session-scoped inference**, not a permanently allocated high-end GPU.

Storage, cold-start/model-load time, data transfer, availability and serverless premiums must be added to the compute-only figures.

## 7.2 The real blocker is quality, not merely hosting cost

A GPU cheap enough to rent does not establish that a suitable model fits it or produces acceptable HDM behavior.

Future evaluation must cover at least:

- narrative quality and style control;
- instruction following;
- long-context reliability;
- structured output/tool calling;
- role isolation/context obedience;
- reasoning quality for interpretation and NPC decisions;
- hallucination/fabrication behavior;
- Russian and English quality if both matter to deployment;
- latency/tokens-per-second;
- VRAM requirements under required context length;
- quantization quality loss;
- concurrent-player throughput;
- stability across long campaigns.

## 7.3 Fine-tuning is deliberately deferred

Do **not** begin by assuming HDM needs to train or fine-tune a model.

A later research sequence should be:

```text
select plausible base/open models
        ->
build HDM role-specific evaluation suite
        ->
measure failures against project goals
        ->
only then decide whether prompting/RAG/tools are enough
        ->
if not, identify the exact behavior that requires tuning
        ->
evaluate LoRA/SFT/preference tuning or other methods
```

This avoids paying the cost and complexity of training before the project knows what deficiency it is trying to correct.

---

# 8. Repository visibility is a separate decision

Operating a private paid-inference server does **not technically require** the main source repository to become private.

Regardless of repository visibility:

- provider API keys must never be committed;
- database credentials and production secrets stay in secret/config infrastructure;
- server access policy must not depend on source secrecy;
- authentication/authorization must assume the implementation can be inspected.

Making the main repository private may still become desirable for unrelated reasons:

- restricting distribution while the hosted service is experimental;
- preserving future licensing/commercial options;
- avoiding support expectations for unfinished server infrastructure;
- separating public runtime/client code from private hosted operations.

Those are **product/licensing/distribution choices**, not an immediate technical consequence of API billing. No decision is made here.

A future split-repository arrangement is also possible:

```text
public HDM engine/client/contracts
private deployment/infrastructure repository
```

but this is only a policy option and is outside current architecture selection.

---

# 9. Updated interpretation of infrastructure Option 4

`Fully Controlled HDM Service + Direct Model Inference` should now be evaluated in two different ways:

## Public baseline

Still economically ineligible if HDM itself pays unbounded commercial inference for arbitrary users.

## Private owner-operated profile

No longer dismissed on economics alone.

It becomes a serious research option if measured real gameplay can stay inside the owner's chosen `$10–20/month` total inference budget for the intended small trusted group.

This profile would provide the cleanest technical ownership of:

- role calls;
- exact context isolation;
- model routing;
- deterministic server state;
- validation/staging;
- background work;
- observability;
- multiplayer concurrency.

Its main unresolved questions become **actual token economics and model quality**, not architectural controllability.

---

# 10. Research decision posture

Current research posture:

1. Keep the public/no-marginal-cost baseline as the general product target.
2. Add a distinct private owner-operated API profile rather than treating all metered inference as automatically disqualified.
3. Measure real HDM token/call behavior before deciding whether `$10–20/month` is realistic.
4. Treat cheap models + role-based routing + bounded context as the primary economic hypothesis.
5. Treat self-hosted/open-weight inference as a future alternative worth preserving, not a problem to solve now.
6. Do not begin fine-tuning work before a role-specific HDM evaluation suite identifies concrete model deficiencies.
7. Keep repository-publicity/licensing decisions separate from credential security and infrastructure feasibility.

---

# 11. Primary current pricing sources

Observed 2026-08-22:

- OpenAI model comparison/pricing: https://developers.openai.com/api/docs/models/compare
- Anthropic list prices (2026-05-27): https://www-cdn.anthropic.com/files/4zrzovbb/website/3684c2faafb97418665782cea0001f439f74b1d2.pdf
- Gemini Developer API pricing: https://ai.google.dev/gemini-api/docs/pricing
- Runpod GPU pricing: https://www.runpod.io/pricing
- Lambda GPU instance pricing: https://lambda.ai/instances
