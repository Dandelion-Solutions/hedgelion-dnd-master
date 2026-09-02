# R2.7 WP-12 — Step 7 Resolution Gate

Status: **COMPLETE — ALL BLOCKING/SIGNIFICANT FINDINGS RESOLVED**

## 1. Resolution summary

The Step-6 whole-project critic produced two `BLOCKING`, six `SIGNIFICANT` and
one `MINOR` findings. F01–F08 are accepted and mechanically repaired in the
current candidate v2. F09 is a documentation-consistency finding routed forward
to WP-26; it does not alter WP-12 architecture.

No finding exposes a residual product-semantic, canonical-authority,
hard-to-reverse compatibility or material risk-acceptance choice.

**Human decision required: NO.**

## 2. Item-level dispositions

### F01 — current-owner key accidentally included source basis

Severity: **BLOCKING**  
Agree: **YES**

Repair:

- candidate v2 LAW WP12-4 makes current semantic-owner uniqueness depend on the
  selected campaign/authority context + native family + complete native identity;
- source/ref/path/revision/writable partition is currentness/routing metadata only;
- source-specific historical payloads may exist only as explicitly non-current
  evidence/cache and cannot satisfy a current-owner mutation/read.

Architectural consequence: none beyond making the existing one-owner law
mechanically unambiguous.

Resolved: **YES**

### F02 — pre-CAS live prospective state could overwrite current HOT owner

Severity: **BLOCKING**  
Agree: **YES**

Repair:

- candidate v2 LAW WP12-22 requires pre-CAS live state to remain an ephemeral
  prospective transition and forbids replacing the accepted current owner row;
- LAW WP12-23 permits local current-owner adoption only after confirmed compatible
  live CAS;
- local-adoption failure after successful remote CAS recovers/reloads the accepted
  live source and never rolls back/replays the accepted mechanics.

Resolved: **YES**

### F03 — blanket source movement could destroy established local SOFT

Severity: **SIGNIFICANT**  
Agree: **YES**

Repair:

- candidate v2 LAW WP12-16 separates invalidation of source-derived clean copies/
  helpers from already-established local owner generations;
- proven-disjoint remote movement preserves accepted local semantics, identities
  and RNG while source/publication basis is rebuilt;
- overlapping dependency movement requires owner-specific revalidation/
  re-resolution rather than blind replay/merge.

Resolved: **YES**

### F04 — physical HOT possession could bypass information/access authority

Severity: **SIGNIFICANT**  
Agree: **YES**

Repair:

- candidate v2 LAW WP12-6 states that local possession is not permission;
- role-context/information eligibility remains owned by R2.3/Step 4;
- gameplay/publication authority remains owned by `ACCESS_CONTROL.md` and current
  routing/principal checks;
- derived query APIs cannot launder private/ineligible data.

Resolved: **YES**

### F05 — frozen publication omitted acting-principal/authorization basis

Severity: **SIGNIFICANT**  
Agree: **YES**

Repair:

- candidate v2 LAW WP12-20 freezes target repository/ref, source basis, acting
  principal/authorization basis, owner generations, dependency/read footprint,
  resulting path delta and publication reason;
- mutable authorization dependencies are revalidated at the owning protocol's
  required pre-mutation boundary;
- cached creator/PLAYER evidence remains derived evidence only.

Resolved: **YES**

### F06 — open accepted work could be reinterpreted under ambient newer mechanics

Severity: **SIGNIFICANT**  
Agree: **YES**

Repair:

- candidate v2 LAW WP12-12 preserves/resolves the compatible accepted catalog,
  rules, invocation and dependency context required by open Command/Procedure/
  Resolution/Continuation state;
- structural HOT representation migration cannot silently rebind accepted work;
- missing compatible interpretation context remains a typed Step-5.2
  compatibility/recovery failure.

Resolved: **YES**

### F07 — pooled SQLite could cross campaign/context boundaries

Severity: **SIGNIFICANT**  
Agree: **YES**

Repair:

- candidate v2 LAW WP12-2 scopes every owner lookup, hydration, query, mutation,
  transaction and publication preparation to one selected campaign/authority
  context;
- one-file-per-campaign is not mandated, but physical co-hosting requires hard
  namespace isolation and may not create cross-campaign inference/currentness.

Resolved: **YES**

### F08 — surviving unpublished local DB could be mistaken for recoverable canon

Severity: **SIGNIFICANT**  
Agree: **YES**

Repair:

- candidate v2 LAW WP12-25 makes current native authority/exact pins the cold
  recovery source;
- surviving local bytes are reusable only after source-equivalence/derivability
  proof as non-authoritative cache;
- unpublished local owner generations do not become established recovery state by
  mere physical survival.

Resolved: **YES**

### F09 — stale storage-v2 wording in `BRANCH_MODEL.md`

Severity: **MINOR**  
Agree: **YES**

Disposition:

- current shipped `dnd_storage.schema.yaml` / storage runtime surface uses the
  later structured storage-baseline provenance contract, while
  `DEV/ARCHITECTURE/BRANCH_MODEL.md` preserves older storage-v2 marker wording;
- the mismatch does not change the WP-12 law that storage baseline is
  storage/new-campaign configuration/provenance and never existing-campaign HOT
  or runtime-selection authority;
- route as WP-26 documentation/routing/supersession consistency work rather than
  editing unrelated accepted architecture during WP-12.

Resolved for WP-12: **YES — FORWARD CONSISTENCY ITEM**

## 3. Mandatory finding-propagation sweep

| Artifact / carrier | Propagation disposition |
|---|---|
| WP-12 Step-1 Task Brief | **RETAIN CURRENT** — framing already requires owner/currentness/access boundaries strongly enough; no rejected law is owned there. |
| WP-12 Source Manifest | **UPDATE** — add the Step-6 independently inspected Access Control, MechanicalContext, Branch Model, Integrity, Randomness, Multiplayer and Step-5.14 routes; preserve their actual authority roles. |
| Step-2 evidence / source accounting | **RETAIN AS DESIGN PROVENANCE** — evidence remains valid; candidate v2 is the current synthesis where critic precision was added. |
| Analytical challenge | **RETAIN AS DESIGN PROVENANCE** — selected realization unchanged; no critic finding invalidates the alternative comparison. |
| Step-3 Decision Brief | **RETAIN AS PRE-CRITIC DECISION PROVENANCE** — recommendation remains Alternative A / typed native-owner envelope; repaired candidate v2 controls exact current wording. |
| Step-4 collaborative review | **RETAIN AS PRE-CRITIC REVIEW PROVENANCE** — no human decision was introduced; candidate v2 controls exact final boundary. |
| Step-5 candidate v1 | **EXPLICITLY SUPERSEDED** by Step-5 candidate v2 for current candidate wording. |
| Step-5 candidate v2 | **CURRENT REPAIRED CANDIDATE** — F01–F08 incorporated. |
| Step-6 critic | **RETAIN FINDING EVIDENCE** — item-level attack and severity record. |
| Step-7 resolution | **CURRENT RESOLUTION RECORD** — owns critic disposition/propagation until Step-8 canonicalization. |
| Current progress / task-local cursor | **UPDATE** to Step 7 complete / Step 8 active, then Step 8 complete / mandatory Senior audit. |
| Roadmap | **NO CHANGE** — no sequencing, scope or dependency rebaseline occurred. |
| Canonical architecture index | **UPDATE AT STEP 8 IF REQUIRED FOR CURRENT ROUTING**; it remains derivative and may never duplicate the normative law. |
| Final canonical spec | **STEP 8** — must derive from candidate v2 only and include all repaired laws. |
| Forward/deferred work | **F09 -> WP-26**; WP-13/14/16/19/20/22/24 routes already preserved by candidate v2. |

No rejected formulation remains an unnamed current normative owner. Candidate v1
is historical design provenance and explicitly routes readers to candidate v2.

## 4. Scoped re-review after repairs

The repaired candidate v2 was re-attacked against the Step-6 failure mechanisms:

- one native owner identity cannot split into campaign/live current rows through
  source-basis keys;
- pre-CAS live prospective state cannot replace the accepted current HOT owner;
- disjoint source movement cannot erase established local SOFT semantics;
- physical SQLite possession cannot grant role/access/information authority;
- publication cannot rely solely on stale cached acting-principal evidence;
- open accepted execution cannot silently migrate to ambient newer mechanics;
- physical database co-hosting cannot cross campaign/context namespaces;
- surviving unpublished local bytes cannot outrank current native recovery
  authority.

No repair introduces a new semantic owner, global transaction, persistent journal,
new durable format or new architecture trade-off.

Re-review result:

```text
UNRESOLVED BLOCKING:     0
UNRESOLVED SIGNIFICANT:  0
HUMAN DECISION REQUIRED: NO
```

## 5. Gate

Step 7 is complete. Step 8 canonicalization is authorized automatically under the
approved WP-12 auto-continue instruction.

After completed Step 8, stop for the mandatory Senior audit. WP-13 and
implementation planning remain blocked until explicit Senior GO.
