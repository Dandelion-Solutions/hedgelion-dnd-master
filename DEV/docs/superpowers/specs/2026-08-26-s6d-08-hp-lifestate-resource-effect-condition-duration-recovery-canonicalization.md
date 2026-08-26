# S6D-08 Step 8 — Canonicalization

Status: **CANONICAL / AUTHORITATIVE PUBLICATION**

Date: 2026-08-26

## Canonical result

S6D-08 adopts DEV/ARCHITECTURE/HEALTH_EFFECTS_RECOVERY.md as the integration owner and the identity-bound health-effects-recovery-seed.json as its bounded package machine contract.

Published deltas:

- Actor material health requires current, maximum_base, LifeState and LifeStatePolicy; supported Resource current is integer;
- unused generic resource.hit_points is removed;
- Second Wind/Tactical Mind shared-pool and recovery semantics are corrected;
- package identity expands to the exact character + health/effects/recovery content set;
- reference validator and focused tests close health/LifeState, Resource/boundary, Effect/Condition/Duration and durability-recovery behavior;
- S6D-07 readiness evidence pins the aggregate package content-set identity;
- PROJECT_MAP and roadmap route the new owner and mark S6D-08 closed.

## Non-activation result

Periodic Effect content, generic concentration content and Exhaustion remain nonselectable. No quarantined primitive is activated. The machine seed does not promise full SRD coverage or a production runtime implementation.

## Publication gate

Publish only from a fresh authoritative ref through the GitHub Connector, verify the final branch SHA and read back the owner, critic PASS, resolution gate, machine identity and roadmap. Stop before S6D-09.

