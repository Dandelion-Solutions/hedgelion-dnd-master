# SP03 Step2 external package — verification receipt

Date: 2026-10-13. Surface: OpenCode local static research/artifact checks. No behavior, deployed issuer, CI, build, audit, independent review or production PASS is asserted.

Retained siblings: [research](2026-10-13-sp03-auth-turn-step2-research.md), [source ledger](2026-10-13-sp03-auth-turn-step2-source-ledger.md), [case ledger](2026-10-13-sp03-auth-turn-step2-case-ledger.md).

## Frozen artifact identities (SHA-256)

| Artifact in `/tmp/hdm-dev/spell-recovery/` | Lines | SHA-256 |
|---|---:|---|
| `SP03-auth-turn-step2-research-20261013.md` | 246 | `7935928d917ea27d6d139a2b3e081c435ad6ed0c984e2c8bfc5043ba3d4df319` |
| `SP03-auth-turn-step2-source-ledger-20261013.md` | 154 | `b89290e0002124fb789e973ddcfc82a9a913c2cc40d8b60ef8a5231787af0b60` |
| `SP03-auth-turn-step2-case-ledger-20261013.md` | 82 | `02681c130070dc082e46c8a706b8121f3325dc36e8e0f72fe10cf3eb20826961` |

Retained coordinator brief SHA-256:
`a2730904ce3762f9cc5e0cfc12dd4ae25c091e0ce772e727f6276cc43d13759d`.

## Commands and actual results

1. Initial `git status --short`, branch, remote and HEAD inspection: exit0. Branch `v1/engine-rearchitecture`, configured `origin`, HEAD `39ab1b4a1c7a844f4df2e7886c4b2ac17e401243`. Only untracked coordinator Task Brief; no tracked local diff.
2. `git fetch --prune origin` then `git rev-parse refs/remotes/origin/v1/engine-rearchitecture`: exit0, same SHA. `git diff afca759c38480f0e4a5629236b08c9d401ecd10d HEAD --name-only` showed SP00 qualification/cursor/allocation changes, no GAME/bridge owning semantic/process changes.
3. Final `git status --short && git diff --name-only && git rev-parse HEAD && git ls-remote origin refs/heads/v1/engine-rearchitecture`: exit0. No tracked diff; the same untracked coordinator brief remains; local and remote SHA still39ab. No commit/push occurred.
4. Read-only Python artifact assertions: exit0. Verified ordered unique A01–A24 and B01–B24 rows, required HumanDecision/version/SystemImpact/HTTP403/NOT_ESTABLISHED/Step3 labels, all abbreviated ledger primary paths exist, line counts and hashes above. This is mechanical artifact coherence only; path existence is not a source-inspection/completeness proof. Actual reads/extraction are recorded separately in source ledger.
5. Final report read-back of analytical/completeness/next-unit section: source limitations and nonacceptance retained. Analytical challenge is self-performed, not independent Senior approval.
6. Exact official capability check: OpenAI Help GitHub article returned HTTP403. No current official page bytes obtained; no alternate supported-host capability inferred.

## Gate disposition

`STEP2_RESEARCH_DRAFT: PRODUCED`

`ANALYTICAL_GATE: SELF_CHALLENGE_RECORDED`

`CASE_ACCOUNTING: 24 A + 24 B REQUIRED DISPOSITIONS, NOT EXECUTED PASS`

`DEPLOYED_ORIGINAL_INPUT_ISSUER_PROOF: UNAVAILABLE / HELD`

`ACTUAL_GAME_TURN_RESET_SLOT_PRODUCER_PROOF: NOT_ESTABLISHED / HELD`

`HUMAN_DECISION_REQUIRED: NO ESTABLISHED WITHIN OWNER-CONFORMING DRAFTS`

`VERSION_IMPACT: NONE — external-only research, no namespace owner/projection edits`

`SYSTEM_IMPACT: ARCHITECTURE_REVIEW_REQUIRED REMAINS ON BOTH BRIDGE EDGES`

`STOP2 / CANONICAL_ACCEPTANCE / IMPLEMENTATION_GO: NOT CLAIMED`

Next process unit: coordinator's separately dispositioned Step3 Decision Briefs and recorded Step4 HumanDecision YES/NO, preserving exact deployment/native proof holds. Worker stops at the authorized Step2 boundary.
