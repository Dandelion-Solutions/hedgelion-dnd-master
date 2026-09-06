# Step 5.13 — Logical Git Ref Retirement — Canonical Amendment

Status: **CANONICAL AMENDMENT — WP-21 STEP-1 RECONCILIATION / SENIOR REVIEW PENDING**

Date: 2026-09-06

Scope: narrow reconciliation of Step 5.13 live branch/ref cleanup with the fixed Product Owner branch/ref deletion policy and the supported GitHub Connector surface.

Controlling Product Owner authority:

- `DEV/docs/superpowers/specs/2026-09-06-hdm-branch-ref-deletion-prohibition-owner-decision.md`.

Superseded only where inconsistent:

- `DEV/docs/superpowers/specs/2026-08-21-step-5-13-garbage-collection-orphan-cleanup-canonical-spec.md`, specifically its physical branch/ref-deletion assumptions in Sections 2, 6, 23-24, 34-38 and their machine/test carry-forward.

All Step-5.13 laws for current-tree semantic retirement, survivor-before-removal, closed blocker contracts, currentness, conservative failure, Story/chronology/checkpoint/message retention and host-managed unreachable-object reclamation remain unchanged unless this amendment says otherwise.

---

## 1. Fixed capability/policy boundary

### LAW 5.13-R1 — HDM AUTOMATION NEVER DELETES GIT BRANCHES/REFS

HDM automatic architecture MUST NOT design, capability-probe, invoke, retry or otherwise attempt physical Git branch/ref deletion.

The supported GitHub Connector surface does not expose branch/ref deletion. HDM SHALL NOT spend runtime probing for that operation and SHALL NOT substitute native Git/CLI, private HTTP, another undeclared transport, manual operator action or any out-of-band deletion fallback.

This is a fixed Product Owner policy, not a deferred capability request.

Therefore the old concepts equivalent to:

```text
optional RepositoryPort DeleteRef
CAPABILITY_DEFERRED because DeleteRef is missing
ambiguous DeleteRef verification/retry
```

are removed from the supported HDM automation model.

### LAW 5.13-R2 — REF RETIREMENT IS LOGICAL RETIREMENT

For Git-backed LIVE/prepared/noncurrent refs, retirement means only:

```text
authority ended under the native owner
+ current routing no longer selects the ref
+ retained consumers no longer require the ref as current resolvable authority
+ stale hosts cannot recreate authority from the old name
```

No physical branch/ref deletion is part of that transition.

### LAW 5.13-R3 — PHYSICAL REF EXISTENCE DOES NOT IMPLY AUTHORITY

Physical ref existence does not imply authority, liveness, currentness or eligibility for gameplay retrieval.

A logically retired absorbed/orphan/noncurrent ref may remain physically present indefinitely. Its continued presence is harmless unless some separate current contract incorrectly routes to or treats it as authority; that incorrect routing/selection is the defect, not the physical ref's existence.

Likewise, physical absence of an already-logically-retired ref does not establish that HDM deleted it and does not by itself prove the prior retirement decision.

---

## 2. Step-5.13 live-ref reconciliation

The existing Step-5.13 classification remains useful:

```text
ACTIVE
CLOSED_UNABSORBED
NONAUTHORITATIVE_ABSORBED
NONAUTHORITATIVE_PREPARED_ORPHAN
UNCLASSIFIED_NONCURRENT_REF
```

It now governs logical routing/authority disposition only.

### LAW 5.13-R4 — ACTIVE AND CLOSED_UNABSORBED REFS CANNOT LOGICALLY RETIRE

- `ACTIVE` remains selected live/writable authority.
- `CLOSED_UNABSORBED` remains truth/recovery authority until campaign absorption completes.

Neither may be de-routed or classified retired while its native contract still selects it.

### LAW 5.13-R5 — ABSORBED REF LOGICAL RETIREMENT REQUIRES DEPENDENCY DISCHARGE

A `NONAUTHORITATIVE_ABSORBED` ref may be logically retired only after bounded current campaign evidence proves final absorption/current route-away and no retained consumer requires that ref/source as current resolvable evidence.

The resulting maintenance success does not require physical ref removal.

### LAW 5.13-R6 — PREPARED ORPHAN LOGICAL RETIREMENT REQUIRES BOUNDED NONAUTHORITY PROOF

Branch/ref existence or absence from one route is insufficient. Use bounded preparation/opening/routing evidence. If nonauthority remains uncertain without broad history scan, retain/report as `UNCLASSIFIED_NONCURRENT_REF`.

No physical cleanup attempt follows either classification.

### LAW 5.13-R7 — UNCLASSIFIED NONCURRENT REF MAY REMAIN PHYSICALLY PRESENT

Unknown leftover ref clutter does not become authority and does not block gameplay unless a current routing or protected-consumer contract actually depends on it.

Do not scan arbitrary history and do not attempt deletion merely to make the repository cosmetically tidy.

### LAW 5.13-R8 — STALE HOST CANNOT RECREATE OLD AUTHORITY

The current owner/routing state selects authority. A stale host encountering an old physically present, absent, closed or de-routed ref must resynchronize/route forward and may not adopt or recreate the old epoch from cached ref identity.

---

## 3. Safe-retirement dispositions

The old generic `CAPABILITY_DEFERRED` disposition is not needed for ref deletion, because ref deletion is not an HDM operation.

For Step-5.13 retirement assessment, relevant supported dispositions remain equivalents of:

```text
SAFE_TO_RETIRE_CURRENT_REPRESENTATION
RETAIN_BLOCKED
RETRY_STALE
INTEGRITY_REQUIRED
```

For a Git ref, `SAFE_TO_RETIRE_CURRENT_REPRESENTATION` means safe logical retirement/de-routing under R2-R8. It does not schedule or imply physical branch/ref removal.

Current-tree file/record retirement remains a normal campaign semantic delta under Step 5.6 and is not changed by this amendment.

---

## 4. Current platform/Connector disposition

Current supported profile:

```text
branch/ref creation: supported where owning protocol permits it
non-force ref advancement: supported where owning publication protocol permits it
branch/ref deletion: NOT AN HDM AUTOMATION CAPABILITY
```

No later architecture/spec/implementation task should re-probe whether deletion appeared in the Connector unless the Product Owner explicitly reopens this policy first. External APIs possibly supporting deletion in principle do not create an HDM requirement or implementation route.

Host-managed unreachable-object reclamation remains separate and unchanged. HDM does not own generic Git object reclamation or secure erasure.

---

## 5. Machine-realization reconciliation

Step-5.13 implementation planning must therefore realize, for live refs:

1. classification of ACTIVE / CLOSED_UNABSORBED / absorbed / prepared-orphan / unclassified noncurrent refs;
2. nonreused authority epoch/ref identities;
3. bounded proof for absorption or prepared-orphan nonauthority;
4. logical de-authorization/de-routing without any delete operation;
5. stale-host rejection of old authority even when the old physical ref still exists;
6. diagnostics that distinguish physical existence from logical authority/currentness;
7. no capability probing, no `DeleteRef` invocation, no delete retry and no manual/out-of-band deletion fallback.

There is no `RepositoryPort.DeleteRef` debt and no deletion-job/queue debt.

---

## 6. Required regression cases

Current implementation-facing regression coverage for this surface must include at least:

1. ACTIVE ref cannot logically retire/de-route;
2. CLOSED_UNABSORBED ref cannot logically retire/de-route;
3. absorbed ref may logically retire only after current absorption plus retrieval-dependency discharge;
4. prepared orphan requires bounded nonauthority proof;
5. unclassified noncurrent ref stays harmless/retained rather than triggering broad history scan;
6. a logically retired physical ref may remain indefinitely without regaining authority;
7. physical ref existence does not imply authority/liveness/currentness;
8. physical ref absence does not substitute for bounded retirement proof;
9. stale host cannot recreate/adopt an old authority epoch from a physically present old ref;
10. HDM has no automatic ref-delete capability probe/invocation/retry path;
11. HDM has no manual/native-Git/private-HTTP/out-of-band deletion fallback;
12. gameplay correctness is unchanged by physical retention of logically retired refs.

Executable architecture regression coverage is in `DEV/TESTS/test_branch_ref_retirement_policy.py`.

---

## 7. Carry-forward and canonical exit reconciliation

Step-5.14 and later whole-project reviews must test logical ref retirement with physically persistent stale refs, not unavailable/ambiguous deletion outcomes.

The Step-5.13 canonical exit proof item previously describing live ref deletion as optional/capability-gated is superseded by:

```text
live Git ref retirement is post-authority logical de-authorization/de-routing only;
physical branch/ref deletion is outside the HDM automation model.
```

The Step-5.13 canonical summary is read accordingly:

> Every representation HDM removes from its current authoritative namespace is already semantically retired or sufficiently replaced under its native owner. Current-tree cleanup may remove current semantic clutter; live Git refs are only logically retired/de-routed and may remain physically present indefinitely. Neither their persistence nor their absence establishes gameplay authority.

```text
HUMAN_DECISION_REQUIRED: NO
NEEDS_PO: NONE
UPSTREAM_WHOLESALE_REOPEN_REQUIRED: NO
VERSIONING_TAXONOMY_REOPENED: NO
```
