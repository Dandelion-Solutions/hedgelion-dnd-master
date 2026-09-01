# R2.7 WP-11 — Physical Storage Topology, Identity and Indexing — Task-Brief Critic

Status: **WHOLE-PROJECT STEP-1 CRITIC COMPLETE — REPAIRS APPLIED**

## Method

The critic reconstructed the WP-11 dependency subgraph through the current
project map, global owner matrix, Step-5 persistence/recovery/live/chronology
owners, R2.1–R2.5 constraints, closed WP-09/WP-10 results, current GAME storage
and campaign consumers, DEV schemas/catalogs and focused verification routes.
It treated the proposed brief as a framing artifact, not as authority.

## Findings and dispositions

| ID | Dependency route | Finding in initial brief framing | Severity | Repair / disposition |
|---|---|---|---|---|
| C01 | scope discovery → WP-10 → all accepted record families | A Round-2-only inventory would omit legacy and current high-cardinality world/history/runtime families. | BLOCKING | AUTO_RESOLVED: mandate and Step-2 exit criteria require whole-project family and lookup accounting. |
| C02 | Branch Model → STORAGE/PERSISTENCE → generator/template | Campaign branch root, storage-default metadata, local template and HOT working set could be collapsed into one physical tree. | BLOCKING | AUTO_RESOLVED: added explicit four-way lifecycle boundary and exact storage/bootstrap consumers. |
| C03 | R2.2/R2.3 → indexes/discovery → access/disclosure | Index design could leak secrets, make index omission a negative proof, or make A-to-B relationship symmetric. | BLOCKING | AUTO_RESOLVED: added eligibility/non-secret/rebuild constraints and dedicated failure probes. |
| C04 | Step-5.8/5.9 → LIVE/chronology → Git transport | Path/ref/commit ordering could be misread as fictional chronology or live/current authority. | BLOCKING | AUTO_RESOLVED: preserved chronology, live and publication boundaries in constraints and primary owner set. |
| C05 | WP-10 canonical allocation → WP-11 → WP-12/13/14/18/19/20/24 | Topology framing could silently choose schema, HOT, transaction, recovery, bootstrap, migration or scale realization. | BLOCKING | AUTO_RESOLVED: expanded out-of-scope routing and requires forward obligations only. |
| C06 | GAME schemas/templates → DEV schemas/catalogs → tests/audit | Existing names/templates could receive topology credit without machine consumer evidence; DEV contracts could be mistaken for shipped format. | SIGNIFICANT | AUTO_RESOLVED: Source Manifest lists both exact current consumers and focused machine/test/audit routes; Step-2 proof distinguishes their roles. |
| C07 | index API/directory constraints → monolithic indexes → potential large families | The first draft named indexing but did not demand a bounded composition path for every lookup. | SIGNIFICANT | AUTO_RESOLVED: made bounded lookup, deterministic routing and no-directory-enumeration explicit Step-2 proof and exit criteria. |

## Actual-owner and consumer check

The critic opened the direct Branch Model, entity/Actor ownership, Step-5
durability/publication/recovery/live/chronology sources, WP-09/WP-10 canonical
boundaries, GAME storage/persistence/identity/consumer surfaces, relevant
schemas, DEV contracts and focused tests/audit/CI routes on the verified current
public ref. No Source Manifest path used for Step-1 framing was unreadable.

## Conclusion

After repairs, the Task Brief has an auditable owner-to-consumer discovery route,
preserves prior semantic allocation and clearly separates topology framing from
downstream realization. No material human decision is hidden in the Step-1
package. The next gate is mandatory Senior review before Step 2.
