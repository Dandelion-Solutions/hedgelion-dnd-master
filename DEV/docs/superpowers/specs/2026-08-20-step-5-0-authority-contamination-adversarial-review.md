# Step 5.0 — Authority / Contamination Adversarial Review

Status: **ADVERSARIAL REVIEW COMPLETE — NO OWNER BLOCKER / AMENDMENTS REQUIRED**

Date: 2026-08-20

Target: `2026-08-20-step-5-0-authority-contamination-candidate-spec.md`

Review objective: attempt to falsify the accepted cleanup by finding a surviving responsibility that would be lost, a duplicate authority that would remain, or a later Step-5 decision that the cleanup would accidentally pre-decide.

---

## 1. Review verdict

No new product/architecture decision is required from the owner.

The accepted cleanup is sound if the amendments below are applied. The review found no retired concept whose current independent identity/lifecycle is necessary for correctness.

Severity summary:

- BLOCKER: 0
- HIGH: 3
- MEDIUM: 5
- LOW: 2

The HIGH findings are mechanical/normative consistency issues, not new semantic choices.

---

## 2. HIGH findings

### H1 — Retiring `world.timeline_marker` must not accidentally ban useful local numeric ordering

Attack:

The old marker used numeric sparse slots. Removing the marker could be misread as requiring graph-only chronology and preventing cheap ordered-local sequences.

Resolution:

The Candidate already distinguishes representation from authority. Preserve `world_order.sequence` and local/domain ordering aids. Step 5.9 may choose sparse numeric keys inside explicit domains.

Required amendment:

Current chronology/catalog prose must say that retirement targets the standalone campaign-global placement owner, not numeric ordering values generally.

Status: **RESOLVED IN CANDIDATE; verify active docs.**

### H2 — Closed catalog retirement must update every enumerating schema, not only JSON instances

Attack:

The Step-4 Chapter cleanup previously exposed a failure where an identifier-policy instance removed a kind but the JSON Schema still required it. The same failure is possible for `world.timeline_marker`, `runtime.dirty_record`, and `runtime.publication_batch`.

Resolution:

Update catalog instances plus every closed schema enumerating retired kinds in one `1.6.0` change. Add a regression test.

Status: **REQUIRES MACHINE CLEANUP.**

### H3 — Empty template paths are real affordances because init copies template contents wholesale

Attack:

One could argue empty `WORLD/SECRETS/` and `STATE/TACTICAL/` directories are harmless placeholders.

Counterevidence:

`init_campaign.py` copies the entire engine `CAMPAIGN/` template contents into the campaign root. Therefore those empty paths are reproduced in every new campaign and actively advertise storage semantics.

Resolution:

Delete their tracked `.gitkeep` files; do not replace them with README placeholders.

Status: **REQUIRES TEMPLATE CLEANUP.**

---

## 3. MEDIUM findings

### M1 — Tactical capability must not be confused with tactical storage owner

Removing `STATE/TACTICAL/` does not remove combat, initiative, geometry, positioning, encounter state, procedure state, effects, or scene-local actionable facts. It only removes an untyped generic bucket.

If later exact geometry requires independently persisted identity/lifecycle, a later design may add a specific owner/storage contract.

Status: **RESOLVED.**

### M2 — `pending_global_consequences` retirement must preserve all actual pending-work classes

The generic array may not be removed by dropping future work.

Surviving mechanisms include:

- owner-local Effect temporal/scheduled-trigger state;
- root RuntimeCommand mandatory descendant closure;
- pending-child invocation descriptors;
- Continuation suspended execution state;
- domain owner state and causal Events;
- live compaction state where applicable.

Step 5.3 must inventory all pending-work classes and prove no-lost/no-double recovery.

Status: **RESOLVED / CARRY FORWARD 5.3.**

### M3 — Removing `runtime.dirty_record` and `runtime.publication_batch` must not remove the concepts

Dirty tracking is still required in the hot working set; publication still requires a coherent frozen transaction snapshot. The retirement removes only pre-approved independent record identity.

Step 5.5/5.6 may re-admit a runtime record if crash recovery, cross-call addressing, audit or idempotency proves independent lifecycle is required.

Status: **RESOLVED / CARRY FORWARD 5.5–5.6.**

### M4 — Sole MANIFEST checkpoint pointer requires atomic pointer publication with checkpoint creation

A sole pointer is correct only if the checkpoint record and pointer update cannot expose a pointer to a missing checkpoint. Existing campaign-tree transaction semantics can publish both paths in one tree/commit.

Step 5.7 still owns exact checkpoint path resolution and validation.

Status: **RESOLVED; carry invariant to 5.7.**

### M5 — Removing legacy `CAMPAIGN/...` current-storage wording must not delete the engine-source `GAME/CAMPAIGN/` template concept

There are two distinct meanings:

1. obsolete campaign-storage wrapper path `CAMPAIGN/...` — remove;
2. source tree template directory `GAME/CAMPAIGN/` — legitimate and retained.

Active runtime docs must not preserve obsolete storage aliases as if they were supported current paths.

Status: **RESOLVED.**

---

## 4. LOW findings

### L1 — `CURRENT.last_event_id` remains provisional and could later be retired

The field currently provides a compact log/recovery cursor. It must not become fictional total-order authority. Step 5.1/5.9 should either prove its role or remove/replace it.

Status: **DEFERRED 5.1/5.9.**

### L2 — Early proposal documents contain stale retired vocabulary

Historical/proposal documents may mention retired IDs and old storage models. They must not be treated as current authority.

For documents that are still easy to mistake for current design, add/retain an explicit supersession warning pointing to current inventory/canonical specs. Do not rewrite historical decision artifacts merely to erase history.

Status: **DOCUMENTATION HYGIENE REQUIRED.**

---

## 5. Accidental capability-loss tests

The cleanup is safe only if all of these remain true after retirement:

1. combat and procedure mechanics still have concrete owners;
2. suspended choices/reactions retain Continuation authority;
3. mandatory post-commit work retains pending-child identity;
4. temporal obligations remain on their real owners and Temporal Agenda remains rebuildable;
5. chronology still supports causal edges, `after` edges, local sequence and optional time;
6. checkpoint records remain addressable and MANIFEST can point to the latest selected checkpoint;
7. campaign publication can still track an in-memory dirty set and frozen transaction snapshot without catalogued record identity;
8. current live scene state remains routable through `LIVE/LIVE_STATE.yaml`;
9. Step-4 truth/knowledge/disclosure owners are not replaced by `SECRETS` storage;
10. no later slice is forced to use a global scalar timeline, generic tactical bucket, generic pending-consequence bucket, dirty-record class or publication-batch class.

---

## 6. Resolution gate

Proceed with cleanup if and only if implementation satisfies:

```text
catalog 1.6.0 coherent
retired IDs absent from active machine registries and enumerating schemas
obsolete template paths absent
one latest-checkpoint pointer
current-root live paths only
partial-order chronology preserved
accepted Step-3 owners preserved
later questions explicitly deferred
full exact-HEAD validation green
```

No additional human decision is required before this bounded cleanup.
