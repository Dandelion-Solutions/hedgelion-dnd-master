# Persistence Transaction Regression Cases

These cases protect campaign branch transactions from self-races, whole-tree reconstruction, unrelated file rewriting and formatting drift.

## PT01 — Existing campaign uses base tree
Campaign branch already has scaffold or later history and PC/NPC/scene state becomes dirty.
Pass: create_tree uses the pinned HEAD tree as `base_tree_sha`; routine save MUST NOT create a from-scratch tree.

## PT02 — Only semantically dirty paths enter delta
Save changes PC, PC_INDEX, scene, CURRENT and card.
Pass: tree delta contains those paths (and any directly required related records) only. Unrelated files inherit their exact blobs from base tree.

## PT03 — README guide survives ordinary save byte-for-byte
README contains current overview/player-guide markers. Save does not need campaign identity overview change.
Pass: README is absent from tree delta and remains byte-identical.

## PT04 — Narrow README overview update preserves guide
Campaign identity materially changes during an already-required save and README overview is stale.
Pass: only content between `CAMPAIGN_OVERVIEW_BEGIN/END` changes; player-guide block, markers and outside bytes are preserved exactly from base content.

## PT05 — HOUSE_RULES survives unrelated save
No house rule changed, but runtime locally parsed campaign files.
Pass: `RULES/HOUSE_RULES.md` is absent from dirty delta and inherits exact base blob. Do not shorten/rewrite explanatory template prose.

## PT06 — YAML formatting is not dirtiness
Runtime parsed YAML and serializer would change quotes, inline arrays or key formatting without semantic change.
Pass: unchanged semantic paths are inherited from base tree; no formatting-only diff is published.

## PT07 — Unexpected unrelated changed path aborts plan
Local planned tree would modify a path with no semantic dirty reason.
Pass: fail local planned-tree assertion and rebuild before commit creation.

## PT08 — Blank scaffold remains the from-scratch exception
New campaign initialization runs exact `TOOLS/init_campaign.py` and publishes its generated empty scaffold.
Pass: this initialization MAY create tree from scratch as required by NEW_CAMPAIGN_FAST_PATH. Subsequent campaign writes use base-tree deltas.
