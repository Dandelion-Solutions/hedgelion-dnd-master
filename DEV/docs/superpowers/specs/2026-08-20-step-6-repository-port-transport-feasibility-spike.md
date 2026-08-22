# Step 6 Carry-Forward — RepositoryPort Transport Feasibility Spike

Status: **PRELIMINARY FEASIBILITY SPIKE — NOT CANONICAL**

Date: 2026-08-20

Purpose: preserve current evidence for the Step-6 host/deployment feasibility work created by canonical Step 5.6. This document does not reopen Step 5.6 and does not start Step 6.

## 1. Question

Canonical Step 5.6 requires runtime repository publication to be owned by deterministic Python core through an authenticated `RepositoryPort`, while current built-in ChatGPT Data Analysis Python cannot itself make external web/API requests.

Investigate practical publication options, especially:

1. a deterministic bridge from Python/core to GitHub;
2. an alternative GitHub mutation that preserves single-commit/CAS semantics;
3. a hybrid in which Python prepares publication state and a ChatGPT/GitHub integration acts only as transport;
4. whether Python can create a local Git commit that the current GitHub connector simply pushes without resending file contents.

## 2. Current platform constraint

OpenAI currently documents that the Python environment used for ChatGPT data analysis cannot make external web requests or API calls.

Therefore the built-in sandbox, by itself, is not a GitHub client even when ChatGPT has a connected GitHub app.

This is a current deployment constraint, not a universal Python limitation. It MUST be rechecked during actual Step 6 because product capabilities can change.

## 3. Lab setup

Test repository:

`dkolyada/hedgelion-dnd-master-lab`

Isolated branch created for this spike:

`experiment/step-5-6-repository-port-001`

Base `main` commit at branch creation:

`84a9cefc25f6d0bf48ccdee05dcf0a7069969ea8`

No existing lab branches were modified.

## 4. Experiment A — Python can precompute Git blob identity

Python locally constructed the canonical Git blob object for:

```text
HDM repository-port spike
payload_version: 1
value: deterministic-blob
```

Predicted SHA-1:

`65f52727a6235e266eb808106eaa3905f2159984`

The GitHub connector `create_blob` call returned exactly:

`65f52727a6235e266eb808106eaa3905f2159984`

Result:

> Byte payload identity can be owned and proven by Python even when another layer performs remote transport.

The LLM does not need to be trusted as semantic content authority if Python retains the expected object hash.

## 5. Experiment B — Python can precompute resulting tree identity

A first root-tree test locally reconstructed Git tree serialization from exact base-tree entries and predicted the resulting tree after adding a root file.

Predicted resulting tree:

`09c181f769d05e6aecd6e55104fa04052b812c41`

GitHub `create_tree` returned exactly the same SHA.

A second nested-path test used the current connector's support for a tree element containing inline UTF-8 `content`, allowing GitHub to create the changed blob as part of `create_tree` rather than requiring a separate `create_blob` call.

Path:

`SPIKES/repository-port/direct-tree-content.txt`

Python predicted the content blob SHA:

`a8331d3f72bed14991d331c1a6f493f9ea73ac27`

Python recursively reconstructed the changed nested tree and predicted resulting root tree:

`b4e0c6a30cffbcdb7625169771a12478838575b8`

Connector `create_tree(base_tree=..., content=...)` returned exactly:

`b4e0c6a30cffbcdb7625169771a12478838575b8`

Result:

> For text campaign deltas, the current connector can carry all changed file contents in one `create_tree` request, while Python independently proves the exact resulting Git tree SHA before any commit/ref publication.

This means the current fallback need not use one `create_blob` call per changed text file.

Conceptual minimum current connector mutation sequence is therefore:

```text
Python freezes publication envelope
Python predicts expected resulting tree SHA
    -> connector create_tree(base tree, complete delta contents)
Python verifies returned tree SHA
    -> connector create_commit(parent = pinned H, tree = verified T)
    -> connector update_ref(force=false)
```

This is still a model/tool relay, but it can be made non-authoritative for payload correctness.

## 6. Experiment C — non-force ref update provides real race guard

Two sibling commit candidates were created from the same parent:

Candidate A:

`29e4db8f00c1fc82dd6ea67a8cc78813cbb15fe9`

Candidate B:

`9576868182c25c39ac58449a9c8201c5f2fea9b4`

The branch was advanced to A with `force=false`.

A subsequent attempt to move the same branch to sibling B with `force=false` failed with GitHub response:

`422 Update is not a fast forward`

The branch still contained candidate A's value (`race.txt = winner`).

Result:

> The final non-force ref transition is a real optimistic-concurrency guard. A prepared losing commit remains a non-authoritative Git object and cannot replace the winner through the ordinary path.

This validates the Step-5.6 CAS assumption against the actual connected GitHub transport.

## 7. Existing Experiment 002 evidence

The lab already contains `reports/experiment-002-python-checkpoint/RESULTS.md` from 2026-08-17.

Observed there:

- native Git was unavailable in the Python/container environment;
- Python prepared a readable checkpoint in approximately 2.234 ms;
- one GitHub connector mutation took approximately 961 ms;
- total save-turn processing reported by ChatGPT was approximately 1 minute 59 seconds;
- restore likewise needed connector retrieval because Python could not resolve GitHub.

That experiment already concluded that Python preparation is cheap while ChatGPT/connector orchestration dominates the user-visible path.

The new spike strengthens this by showing that connector publication can be reduced to a complete-tree transport plus commit/ref calls and can be hash-verified by Python.

## 8. Exact `local commit -> current connector push` finding

The user's proposed strong hybrid is:

```text
Python builds local working tree
Python creates local Git commit C
LLM/connector merely pushes already-created C
```

This exact form is **not supported by the current connected GitHub tool surface**.

The current connector exposes remote Git Database primitives such as:

- `create_blob`;
- `create_tree`;
- `create_commit`;
- `update_ref`.

It does not expose an operation equivalent to:

```text
upload this local Git pack/bundle/object database
or
git push this already-created local commit
```

Consequences:

- a local commit SHA alone is insufficient because GitHub must also possess its referenced blobs/tree/commit object;
- the current connector cannot consume an existing local pack/bundle;
- its `create_commit` wrapper creates a new remote commit object and does not expose author/committer metadata inputs;
- therefore it cannot be treated as a transparent push of an already-created local commit identity.

This does **not** mean exact local-commit push is impossible in general. A custom backend or a Python environment with authenticated Git network access can use normal Git smart transport or import a bundle/pack and push the exact object.

It means only that the current built-in ChatGPT GitHub connector is not such a transport.

## 9. Alternative GitHub backend primitive — GraphQL `createCommitOnBranch`

GitHub currently exposes GraphQL mutation `createCommitOnBranch`.

Important properties:

- branch is explicit;
- caller supplies `expectedHeadOid`;
- one mutation supplies the complete file additions/deletions;
- GitHub creates the commit whose parent is branch HEAD and updates the branch in the same mutation;
- mismatched expected HEAD prevents blindly committing against an unexpected frontier;
- additions contain full Base64 file contents;
- authorship belongs to the authenticated credential owner;
- GitHub can sign these commits when supported.

For a custom deterministic `RepositoryPort`, this is a strong candidate because it collapses the ordinary single-ref publication into one GitHub mutation rather than remote object preparation followed by a separate ref update.

The Base64 requirement is not architecturally problematic if encoding occurs inside deterministic bridge/backend code rather than in LLM reasoning/tool payload construction.

Whether GitHub GraphQL payload/file limits fit all HDM campaign batches must be measured before selection; do not assume unlimited payload size.

## 10. Alternative GitHub backend primitive — Git Database REST

GitHub Git Database REST remains suitable when exact object-level control is preferred.

A custom bridge can:

```text
create blob/tree objects
create commit with explicit author/committer/date when desired
perform non-force ref transition
```

GitHub's REST commit endpoint supports explicit `author` and `committer` including timestamps. The current connector wrapper does not expose all of those fields, but a custom RepositoryPort backend can.

This path costs more GitHub API operations than `createCommitOnBranch` but gives more control over object identity and preparation/recovery behavior.

## 11. Option A — custom deterministic RepositoryPort service — recommended target

Concept:

```text
Python core
    builds/finalizes publication envelope or bundle
    hashes exact contents and expected closure
        |
        v
host file/typed bridge
        |
        v
HDM RepositoryPort backend
    authenticates acting principal
    checks expected HEAD / authorization
    publishes via GitHub GraphQL or REST/Git
    returns exact structured result
        |
        v
Python validates result and adopts/clears frozen generations
```

Advantages:

- LLM is not repository transport authority;
- file contents need not be semantically reconstructed by the model;
- one backend call can own retries/ambiguous-ack handling;
- acting-principal/auth policy can be implemented deliberately;
- can use one-shot GraphQL commit when suitable;
- preserves Step-5.6 boundary cleanly.

Current limitation:

OpenAI currently documents full custom MCP write/modify support for ChatGPT Business and Enterprise/Edu. Pro users can currently connect custom MCPs only for read/fetch in developer mode. Custom MCP apps are currently web-only. This must be rechecked at Step 6 and makes this route unsuitable as a universal consumer ChatGPT deployment assumption today.

Promising transport detail to verify later:

OpenAI's MCP/App tooling has file-parameter mechanisms, and current OpenAI Codex source includes rewriting local paths into uploaded file references with temporary download URLs. Community reports describe the same `_meta["openai/fileParams"]` pattern in ChatGPT Apps. Treat this as promising implementation evidence, not yet as a cross-plan/cross-surface product guarantee. A dedicated Step-6 test is required.

## 12. Option B — external/local Python companion with direct Git

Move the persistence-capable Python core outside the restricted Data Analysis sandbox, for example into:

- an HDM remote service;
- a local daemon/desktop companion;
- another execution host with authenticated GitHub network access.

Then Python can use ordinary Git or GitHub APIs directly.

This is the cleanest way to support the exact:

```text
Python creates commit C
Python/companion pushes exactly C
```

model.

Trade-offs:

- another deployable component;
- authentication/token lifecycle;
- hosting/availability/cost;
- local companion discovery/tunneling if not public;
- potentially requires a full/sufficient local Git object database to create exact commits without broad repository cloning.

OpenAI currently documents Secure MCP Tunnel as a way to connect a local MCP server to supported OpenAI products, but the same current plan/surface limits for write-capable MCP must be respected.

## 13. Option C — current built-in GitHub connector as a non-authoritative relay

This is technically viable today and is much stronger than arbitrary LLM-managed persistence if structured carefully.

Python owns:

```text
pinned H
complete paths + final contents/deletions
frozen owner generations
expected blob hashes
expected resulting tree hash
publication reason
expected target ref
```

The ChatGPT host/LLM invokes only a fixed relay sequence:

```text
create_tree(base=T(H), complete delta content)
create_commit(parent=H, returned verified tree)
update_ref(force=false)
```

Python verifies the returned tree against its precomputed SHA before commit creation and validates final outcome before dirty clearing.

Advantages:

- works with the current connected GitHub tool surface;
- preserves one coherent tree/commit/ref publication;
- no per-file commits;
- no manual text Base64 cycle;
- Python can detect content/path corruption before publication;
- current `create_tree` can include multiple inline file contents in one request.

Disadvantages:

- file contents still traverse model/tool arguments;
- model/tool-call latency remains;
- LLM/host still physically initiates GitHub mutations;
- exact repository retry/ambiguous-ack loops remain awkward across model/tool boundaries;
- large payloads consume context/tool bandwidth;
- this is weaker than canonical Step-5.6's intended no-LLM Git transport boundary.

If selected as an officially supported compatibility profile, Step 5.6 would need a narrow explicit refinement distinguishing **non-authoritative transport relay** from LLM-owned repository protocol. Do not silently treat this fallback as already canonical.

## 14. Option D — Python local commit + existing connector transparent push

Verdict: **not feasible with the current connector**.

Revisit only if the connector later exposes at least one of:

- Git pack/bundle upload;
- native push of a local checkout/ref;
- file-valued repository publication action that imports a deterministic bundle;
- another operation that transfers already-created Git objects without resending their contents through normal tool arguments.

## 15. Option E — GitHub Actions as persistence bridge

Not recommended as a base architecture.

A workflow could theoretically execute deterministic Git logic on GitHub infrastructure, but the runtime still needs a clean way to submit the transaction payload and trigger the workflow. Using staging commits/files merely to invoke publication defeats the single coherent campaign-commit goal.

A custom API/MCP endpoint that triggers a workflow is already a RepositoryPort bridge, so direct GraphQL/REST publication is simpler unless a future deployment requirement specifically justifies Actions.

## 16. Current recommendation ranking

### Long-term architecture target

**A — deterministic RepositoryPort service/backend** using:

1. GitHub GraphQL `createCommitOnBranch` where payload limits and authorship semantics fit;
2. Git Database REST when finer object-level control is required.

### Current ChatGPT compatibility fallback worth preserving for evaluation

**C — Python-verified connector relay**, optimized to:

```text
ONE create_tree carrying full textual delta
ONE create_commit
ONE force=false update_ref
```

with Python precomputing and verifying the exact resulting tree.

### Exact local-commit push

**B — external Python companion/direct Git** if we decide the extra deployment component is acceptable.

### Reject as current assumption

**D — local sandbox commit + built-in connector transparently pushes it.** Current connector cannot do this.

## 17. Important architectural consequence

The feasibility problem is narrower than initially feared.

We do **not** need the LLM to calculate Git state correctly.

The lab demonstrates that Python can deterministically own:

- exact file bytes;
- Git blob identity;
- resulting tree identity;
- frozen parent/frontier;
- dirty-generation membership;
- expected transaction closure.

What remains missing in the current sandbox is only an efficient authenticated **transport/execution boundary** from that deterministic state to GitHub.

Therefore the core architecture should continue to model `RepositoryPort` as a replaceable host capability rather than move persistence semantics back into LLM roles.

## 18. Step-6 mandatory tests

Before final deployment selection, rerun at least:

1. current plan/surface availability of custom write-capable MCP/apps;
2. file-param transfer from a Python-generated local artifact into a remote MCP tool without model serialization;
3. acting-principal preservation through OAuth/GitHub App credentials;
4. `createCommitOnBranch` payload/file limits using realistic worst-case campaign save bundles;
5. ambiguous network acknowledgement at the custom bridge boundary;
6. duplicate/replayed MCP tool calls and backend idempotency;
7. mobile/desktop/web support if those surfaces are product requirements;
8. latency versus the current connector relay;
9. current built-in GitHub connector surface — especially whether a future single-call commit/file-bundle action or pack upload exists;
10. whether the product requires consumer Free/Plus/Pro support versus managed-workspace-only capabilities.

## 19. No canonical change yet

This spike supplies evidence only.

Canonical Step 5.6 remains unchanged:

- Python core owns repository publication semantics;
- persistence-capable deployments require an authenticated RepositoryPort/equivalent;
- no LLM-Git fallback is currently canonical.

If Step 6 chooses the current connector relay as a supported degraded/compatibility deployment, Step 5.6 must be explicitly refined rather than silently violated.
