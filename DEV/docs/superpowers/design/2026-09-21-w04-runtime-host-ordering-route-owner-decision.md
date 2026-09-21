# W04 Runtime Host Composition + Native Ordering Route — Owner Decision

Status: **ACCEPTED SENIOR / DESIGN OWNER DECISION**

Date: **2026-09-21**

Reviewed stop head:
`256c4916fecaf38c40c890570f65815cae4df2bb`

This decision resolves the remaining W04.T01A, W04.T05A and W04.T07A
System-Impact stops. It supersedes only the incomplete machine-route portions of
the earlier W04 Senior rulings. The accepted collaboration, Context, native
history, Story/T0 and CLS↔HDM semantics remain unchanged.

## 1. Bounded Source Manifest

Current owning evidence used for this decision:

| Owner/evidence | Blob |
|---|---|
| Step-3 execution boundary canonical spec | `96c5f87bd8cc9a62a9b3d179ec1b4cbc7f564cbe` |
| Step-5.6 campaign publication / RepositoryPort canonical spec | `4ec13a292e91acb692c6e54d8c0ca9f49d79bed9` |
| Step-5.8 LIVE ownership / transport canonical spec | `dbecaee7cdaec62f57bf51941cc31034531cc157` |
| Step-5.10 Story projection durability canonical spec | `0e2d6db8fcfabb2073c43ab8ae62dde778e25530` |
| Story baseline source-domain contracts | `4e85a2899657f43c2bb812e9608d9d0c254b4a96` |
| WP-17 collaboration canonical spec | `d49d817d796929c816ea2ae7bcd815d0986f1102` |
| Stable Wave-04 plan | `cdbc1d2bbc651ff6b087e22b8d502ec46bbc7386` |
| Stable Wave-05 plan | `df288238c77fe6371e4504f22d7a4a9f9eb690f8` |
| T01A round-4 brief | `f591cfc3ef3f7bd4b166bb1b644e82a34b124235` |
| T05A round-4 brief | `a5b41a3fa988ad366bdc6bed942a4974fd916d01` |
| T07A round-3 brief | `3ec4b78eafd359304c14f2f01656e73e18dd5d2d` |
| current RepositoryPort owner | `b99d9a5e509d8fad6231b4853b207ff89219277e` |
| current LIVE owner | `c986225f40701b248b696d66076813b0ba2a98d5` |
| current runtime execution owner | `ae7470b1d4b5b103103445b0e35f9e6545f727fa` |
| Procedure schema | `9edc194482d455257b01a2f8c4926c345b6d714c` |
| Resolution schema | `28fd5844a343f32e4718584d10b2e4c0a2a8733b` |
| Continuation schema | `f657dd3e37db14027d98437285bd7c7d61ef6f08` |
| ChoiceRequest schema | `8b821452e5351cc3478299c479ea831bfb381469` |
| ReactionOffer schema | `db1539403e2883bbd3d4113578bcb58d6fd71395` |

Bounded dependency subgraph:

```text
Step-5.6 runtime host prerequisite
        +
Step-5.8 selected LIVE source read/CAS
        |
        v
W04.T00H runtime host composition
   |           |             |
   v           v             v
T01A        T05A          T07A
   |           |             |
Step-3      Context       Step-5.10
Resolution/  owners       evt source domain
Continuation
```

No wider repository preload is needed for this ruling.

## 2. Trust-boundary clarification

The remaining forged-host loop was caused by treating arbitrary code execution
inside deterministic Python as if it were an untrusted gameplay caller.

That is not the HDM authority model.

### 2.1 Trusted computing base

For this boundary, the trusted computing base is:

```text
tracked deterministic HDM Python
+ runtime host/bootstrap composition code
+ authenticated deployment adapters supplied under Step-5.6 / Step-5.8
```

Untrusted inputs include:

- player/model text and model-shaped objects;
- campaign/live repository bytes before owner validation;
- candidate mappings, indexes, caches and projections;
- callbacks/objects supplied through gameplay/domain APIs;
- remote transport responses before deterministic validation.

### 2.2 Unsupported attacker model

Arbitrary in-process Python code execution that can call
`object.__new__`, `object.__setattr__`, monkeypatch module globals, import
private issuers or replace private attributes is **TCB compromise**, not an
ordinary gameplay authority path.

If a deployment permits untrusted code to execute inside that TCB, that
deployment profile is unsupported until Step-6/deployment isolation supplies an
actual process/tool boundary.

This is not permission to trust caller data or to use Python privacy as semantic
authority. It defines where the canonical Step-5.6 statement "the runtime host
supplies authenticated RepositoryPort capability to deterministic Python" begins.

Independent review MUST still attack every admitted public/model/gameplay data
surface. It MUST NOT classify arbitrary direct mutation of internal Python
objects as a gameplay authority bypass unless such an object can cross an
admitted untrusted API boundary.

## 3. W04.T00H — concrete runtime host composition prerequisite

A new coordinator-owned prerequisite is authorized:

```text
W04.T00H — runtime host composition boundary
OUTPUT:
  W04_RUNTIME_HOST_COMPOSITION_READY
  W04_RUNTIME_HOST_BOOTSTRAP_DELTA_READY
```

Direct implementation scope:

```text
GAME/TOOLS/runtime_host.py
DEV/TESTS/test_runtime_host_composition.py
task-local cursor / bounded Wave-05 bootstrap delta evidence
```

No persisted schema is created by T00H.

### 3.1 Concrete composition root

`GAME/TOOLS/runtime_host.py` owns one infrastructure entry point equivalent to:

```text
compose_runtime_host(
    selected_campaign_id,
    authenticated_repository_port,
    selected_live_transport
) -> RuntimeHost
```

The authenticated repository bridge is supplied by the deployment/runtime host
under Step-5.6. The LIVE transport is supplied by the same host under Step-5.8.

The engine does not try to cryptographically authenticate arbitrary Python
objects after they are already inside the TCB. It validates that the supplied
host adapters satisfy the required operations and immediately binds them to one
campaign-scoped runtime root.

The root:

1. binds one selected campaign identity;
2. owns the RepositoryPort dependency for that root lifetime;
3. creates/owns the selected-LIVE read capability through the existing LIVE
   owner;
4. owns fixed native-family routing dispatch;
5. creates sibling bound services for Context, native History and native
   ordering evidence;
6. re-pins/revalidates current sources per operation; it is not a lease;
7. exposes no setter/rebind operation for repository/LIVE capability;
8. is ephemeral and never serialized into campaign state.

Changing campaign/storage selection creates a new RuntimeHost.

### 3.2 Public/data-plane API rule

After composition, no Collaboration/Context/History gameplay-facing call may
accept any of the following from its caller:

```text
RepositoryPort
LIVE transport / reader
route resolver
RuntimeHost replacement
Context/History service replacement
semantic currentness / eligibility callback
```

The bound RuntimeHost invokes owner modules; callers provide domain requests and
untrusted candidate data only.

Unit tests may compose the root with fixture adapters because the test harness
is acting as the trusted deployment host. That fixture injection is not a
gameplay authority path.

Required T00H negatives:

- no public domain method accepts repository/LIVE/capability override;
- root is campaign-bound and rejects cross-campaign use;
- root methods re-pin/revalidate rather than cache a perpetual currentness lease;
- serialized/caller data cannot name or replace a transport object;
- Context and History are sibling services under the root; History is not
  constructed from Context;
- no token/weak-registry/marker is introduced merely to "authenticate" the host
  root.

The later physical product/bootstrap wiring of the deployment adapters into this
root is Wave-05-owned.

## 4. W04.T01A — native RULE_OWNED_ORDERED producer

The rejected `GAME/TOOLS/mechanics.py` helper is not an authority route and
must be removed before reimplementation.

The positive generation-1 ordered-owner route is owned by the existing Step-3
execution graph.

### 4.1 Exact producer

`GAME/TOOLS/runtime_execution.py` is authorized to add one owner-native,
ephemeral producer equivalent to:

```text
resolve_native_ordering_evidence(...)
    -> RULE_OWNED_ORDERED evidence
     | NO_ORDERED_OWNER
     | fail-closed currentness/integrity error
```

It is called only through the bound RuntimeHost owner-reader path.

The result is derived evidence. It is not a new Procedure/Continuation owner and
is never persisted.

### 4.2 Exact positive proof

Generation 1 positively proves `RULE_OWNED_ORDERED` only through the current:

```text
runtime.resolution
    status = AWAITING_CHOICE | AWAITING_REACTION
    continuation_id = C
        |
        v
runtime.continuation C
    exact current generation
    resolution_id matches
    pending_response exists
        |
        +-> ChoiceRequest
        |     kind = choice
        |     parent_resolution_id matches
        |     continuation_generation matches
        |     responder_id + option_ids
        |
        +-> ReactionOffer
              kind = reaction
              parent_resolution_id matches
              continuation_generation matches
              responder_id + candidate_activity_ids
```

If Resolution/Continuation carries `procedure_id`, exact current
`runtime.procedure` is also loaded and must validate as schema version 2,
`lifecycle=ACTIVE`, with consistent identity/linkage.

An ACTIVE Procedure by itself does **not** prove responder/order semantics.
There is no generation-1 Procedure-only positive ordered route because the
current Procedure schema contains no such ordering contract.

Likewise, an unspecified "another native ordered owner" is not guessed. It
requires a future admitted machine contract.

### 4.3 Currentness proof

The RuntimeHost owner-reader supplies the exact current source basis:

- campaign owner: current `PinnedCampaign` + deterministic WP-11 path + exact
  record at that pinned revision;
- LIVE owner: current selected LIVE route + exact selected source revision +
  owner record from that source.

The ordering evidence records at least:

```text
campaign_id
source scope/key/revision
resolution_id
continuation_id
continuation generation
offer kind
offer_id
responder_id
procedure_id? 
```

It does not own those values.

### 4.4 Collaboration use

The collaboration-relevant IntentClause may contain a bounded
`ordering_resolution_id`/equivalent native ref. The caller cannot provide a
Continuation body, Procedure body, status or final family.

If that ref is present:

- exact owner resolution succeeds with pending Choice/Reaction ->
  `RULE_OWNED_ORDERED`;
- ref is stale/missing/inconsistent -> fail closed;
- ref points to a current non-awaiting Resolution -> fail closed as stale/mismatched
  intent, not `INDEPENDENT_IMMEDIATE`.

If no ordering ref exists, T01A evaluates only the already accepted bounded
collective dependency contract.

This satisfies WP-17 without a second Mechanics authority.

## 5. W04.T05A — Context route

T05A consumes `W04_RUNTIME_HOST_COMPOSITION_READY`.

Context no longer owns or accepts a RepositoryPort/LIVE/runtime object parameter
through its gameplay/domain API.

The RuntimeHost Context service:

1. receives the registered `RoleContextRequest` + bounded discovery hints;
2. uses its bound repository/LIVE owner-reader;
3. dispatches exact owner validation through fixed engine code;
4. applies the registered `ContextNeedProfile` role/purpose/subject/recipient
   contract;
5. emits internal post-resolution current/eligible basis only after those
   validations.

The accepted role/purpose owner remains Context; no new external eligibility
record is introduced.

`object.__new__(BoundContextRuntime)` is not a supported caller path and should
not remain the public API shape. Refactor/remove caller-supplied
`BoundContextRuntime` parameters rather than trying to authenticate such an
object with a local token.

## 6. W04.T07A — native History route

T07A consumes `W04_RUNTIME_HOST_COMPOSITION_READY` plus its already-PASSed
CLS↔HDM preflight.

History is a sibling RuntimeHost service, not a child of Context.

No gameplay-facing API accepts RepositoryPort, LIVE reader, RuntimeHost,
BoundContextRuntime or History service replacement.

The History service implements the already accepted Step-5.10 source contract:

```text
campaign.semantic_events@S
lane evt
evt:<ordinal>
origin LOCAL | LIVE:<epoch>
```

using the root's bound campaign/LIVE source access.

The current W01 `semantic_order` remains the generation-1 per-origin native
enrollment ordinal selected by the previous ruling; it retains no fictional
ordering meaning.

LOCAL currentness is exact pinned campaign-source evidence.
LIVE currentness is exact selected-LIVE source evidence.
Missing routed LIVE source never falls back to campaign.

History validates source-window identity/completeness and then issues its
ephemeral accepted-event/publication values. It never accepts a caller-provided
repository/service/owner port or raw "accepted history" verdict.

## 7. Mandatory clean-basis restore before T00H

The current stop head still contains rejected implementation bytes.

Before T00H RED, restore these paths exactly to the accepted clean basis
`80d1cedfce7f529df96ea2c4b2342ce466cc8806`, including deletion when absent:

```text
DEV/SCHEMAS/context-need-profile.schema.json
DEV/SCHEMAS/context-trace.schema.json
DEV/SCHEMAS/intent-clause.schema.json
DEV/SCHEMAS/native-history-currentness.schema.json
DEV/SCHEMAS/native-history-publication.schema.json
DEV/SCHEMAS/runtime-collaboration-obligation-state.schema.json
DEV/TESTS/test_rd09_access_live.py
DEV/TESTS/test_rd11_context_runtime.py
DEV/TESTS/test_rd12_collaboration.py
DEV/TESTS/test_rd13_story_t0_commentator.py
GAME/SCHEMA/collaboration_obligation.schema.yaml
GAME/TOOLS/collaboration.py
GAME/TOOLS/context_runtime.py
GAME/TOOLS/history.py
GAME/TOOLS/live_state.py
GAME/TOOLS/mechanics.py
```

Preserve:

- current System-Impact briefs and version-impact evidence;
- current execution cursor and CURRENT_PROGRESS;
- accepted build/tool-discovery changes outside this task surface;
- this owner decision.

Restore checkpoint has `VERSION_IMPACT: NONE` because it removes rejected,
non-accepted versions.

Run baseline focused suites, maintenance audit after removing local generated
cache artifacts, local `hdm-reviewer`, non-force publish and remote read-back.

## 8. Resumption DAG

```text
restore rejected task surfaces
  -> reviewer PASS / publish / read-back
  -> W04.T00H runtime host composition
      -> reviewer PASS / W04_RUNTIME_HOST_COMPOSITION_READY
      -> T01A
      -> T05A
      -> T07A   (CLS preflight remains PASS unless its semantic trigger fires)
```

After T00H PASS, T01A/T05A/T07A may run concurrently subject to normal write-set
isolation.

No dependent task starts until its normal producer review checkpoint.

## 9. Wave-05 ownership

Wave 04 owns the deterministic composition/root module and owner-local consumer
contracts.

Wave 05 owns final product/deployment wiring:

- W05.T06 product paths create/use one RuntimeHost after campaign selection and
  never expose transport injection to gameplay callers;
- W05.T08 integrates the runtime-host bootstrap delta into
  `BOOTSTRAP_RUNTIME` / install/shipped CORE and verifies the selected
  deployment supplies the authenticated RepositoryPort and LIVE adapter required
  by Steps 5.6/5.8;
- W05.T08 PROCESSES/AI_REASONING inputs include the accepted native-ordering and
  Context composition semantics.

If a real deployment profile cannot supply the authenticated external adapters,
that profile fails Step-6/deployment feasibility. The engine does not weaken
authority semantics or add an in-process pseudo-security token to compensate.

## 10. Version/System Impact

```text
THIS DECISION DOCUMENT:
  VERSION_IMPACT: NONE

CLEAN RESTORE:
  VERSION_IMPACT: NONE

W04.T00H:
  new runtime_host module -> task performs normal new-module Version Impact
  no persistent schema by design

T01A/T05A/T07A:
  fresh task-local Version Impact Gate from restored basis
  rejected historical version transitions are non-precedential

SYSTEM_IMPACT:
  RESOLVED
  ARCHITECTURE_REVIEW_REQUIRED: NO
```

Wave 05 remains unauthorized until Wave 04 closes through its normal final
Senior audit.
