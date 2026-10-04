# Spell architecture candidate publication/read-back receipt

Status: PUBLISHED REVIEW-READY CANDIDATE / EXACT PAYLOAD READ-BACK AND HOSTED CI PASS. This receipt verifies the immutable payload commit below, not canonical Step8/Stop2 acceptance, recipe implementation or target latency.

Repository: Dandelion-Solutions/hedgelion-dnd-master.
Branch: v1/engine-rearchitecture.
Source parent: `05576261665280c3f424d791c19d8c4080343c6a`.
Payload commit: `25829437479dedb94a6f2ed1226089fdf2fd04a9`.
Payload tree: `b99a4361767ae1ca0cd3639da3cd979a114fbbff`.

Connector-only publication used a fresh unchanged parent read, create_tree/create_commit, non-force ref update, then exact fresh file read-back. All29 prepared files equaled published contents; a complete remote-tree comparison proved exactly29 changed blobs, zero GAME or protected sources changes. Fresh ref after read-back equaled the payload commit. Seven prepublication control tests and corpus/reproduction/independent-review checks are qualified in verification.md.

Hosted Validate run [37204842454](https://github.com/Dandelion-Solutions/hedgelion-dnd-master/actions/runs/37204842454), exact head `25829437479dedb94a6f2ed1226089fdf2fd04a9`: completed/success. Job111443772482: Run full maintenance audit SUCCESS; Run DEV unit tests SUCCESS. The API job/run conclusions are the evidence; no locally executed full DEV or test count is claimed. This CI does not establish a composed spell cast or latency.

## Exact payload read-back manifest

Hashes below mean LF UTF-8 evidence-content identity, not runtime/package digest authority. Each applies at payload commit `25829437479dedb94a6f2ed1226089fdf2fd04a9`; a later receipt/navigation/control-only commit may add this receipt and reference it without rewriting the evidence.

| File at payload commit | LF UTF-8 SHA-256 |
|---|---|
| `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/README.md` | `e5192f0755ee41caa0e404edd764c23cf11d76ce0f475b0c9fe4c493c2d089ae` |
| `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/task-brief.md` | `d4591771d7873d90958b5909314b2798390b2abeedaaa4f767d4736593d86474` |
| `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/step1-critic.md` | `40d0018595d85ee0ccb051e5489dfef99386a12eadb035e116b18cb5a9fa2174` |
| `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/step1-senior.md` | `cc2db8f4d7c5fcd93f4834ce6b327693e8a3c72844569fe198e01d2378a72a78` |
| `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/product-input.md` | `69f44d37026da06f79498f194ce5bf8e2cc2dcff4c324f2c07cfa18babc211da` |
| `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/candidate-spec.md` | `33116b918af862371eb3b54f393bfe31233d0194dac71dc2e221364704520b75` |
| `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/decision-brief.md` | `421920a6cd5730278f2f02623ffa824968a669a0353636a26f38eb944e32b718` |
| `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/system-impact.md` | `03411cf1af3631ac4a4b9e509917447d5508321ebc61e536c678ccada2750033` |
| `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/production-trace.md` | `b085fa25dc61f4aebae913f47c445bb5fe98fcfd79b751ea9f904ba34e154908` |
| `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/performance-offline.md` | `2da0caff150fbced79a01bd2f64456befca3edba34bdd460d9fe9e93d2838479` |
| `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/capability-closure.md` | `26625e60bec32268a1ba7bbfcf2774218b77ac354bba9c454387952edcbaaa52` |
| `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/source-pass-0-2.json` | `23b8872290b5f9786468103faec036de153a4f62ad8dc568cf54f57f6f35c2c1` |
| `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/source-pass-3-5.json` | `2a57acf7829e680e15952ee30b175a42be0eb62cc67b4951beeb0de8fbaf0d17` |
| `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/source-pass-6-9.json` | `23f57b38f89c326fa46b7961d9994342bb7cc92d664201ce1289eb3668955cd6` |
| `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/source-obligation-resolution.md` | `1f1df020f65c040a10756576b257218906798b9dc0a766eaefba665a508cd950` |
| `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/source-body-witnesses.json` | `4b5b19147ad31407a4495921f74d35cd20030e54e588b9e634b777dc5db70d41` |
| `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/requirement-matrix.json` | `254bde30639bc0071fd944d738407f4e01987065ef6b6448a82b11eae2438372` |
| `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/requirement-matrix.csv` | `a5e0be78ad054b39c04e2564780d1a87c2670e5f3311a65f1fe63b4878e8db52` |
| `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/build_requirements.py` | `0b0ae04b43ebcfe26f9416efe8a3f90e0592471a8c471e552106600c33de5535` |
| `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/resolution.md` | `6ebfce6f6654111a53b99e23d53f08d5cf9397de36a3acfb4ccd28dba413bbaa` |
| `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/adversarial-review.md` | `ff77d9d712adf925deca5896604fa9fc42b9fefa98d8e44fb2b46af1178ccfd9` |
| `DEV/docs/superpowers/design/2026-10-04-spell-execution-architecture/verification.md` | `249454ea24492a1979f3ca6895fa1235faaafae4cad6c1ce76f1517fbee4df99` |
| `DEV/PRODUCT_OWNER_INPUT.md` | `64b6befaf4aa01c80dcbf7326dd20a5f8c7988cf2dfe6b3a8f096b99a969f061` |
| `DEV/CURRENT_PROGRESS.md` | `797ea6ffd12997118cafba3a1b57ad893123457be53b774924b85e9c872f183c` |
| `DEV/PROJECT_MAP.md` | `c222a96e565691776d61617760699662da853495942906a23d6091e772f61b4d` |
| `DEV/ARCHITECTURE/NEAR_TERM_ROADMAP.md` | `f1ac9a01175b47fefd41d8ff0de2c483dfd89bddbbe1ac2c9a72c200ba3082b1` |
| `DEV/docs/superpowers/plans/implementation-wave-05-machine-bootstrap-integration-execution-status.md` | `ed6b4ce6e4fd6e395eabdac41421688cf130e70b904f368b8bcce9264f50cbb0` |
| `DEV/docs/superpowers/design/2026-10-04-w05-t06-p1a-sorcerer-override-senior-review.md` | `4bfb50940cc555410daf2daec2976c93e13952fdddec700a6b5b6cc30a2eb5c7` |
| `DEV/docs/superpowers/plans/implementation-plan-index.md` | `56a5a8950b1fe2358dbb5b4cd65e970b3bef22e60a79c5b89ffdd1ab13e0289c` |

## Exact continuation

Only SP14 Wish Roll Redo remains NEEDS_PO. Candidate architecture and source routing are review-ready. After actual judgment: formalize selected accepted owner amendments -> complete Step8/propagation/verification/publication/read-back -> independent Senior Stop2 -> authorized stable implementation-plan reconciliation. No repeated six-versus339 scope question, no ordinary task-boundary permission request and no new production GO from this receipt. Preserve accepted S1/S2/P0, prior waves and independent P2/P3 dependency routes; Story remains dormant. Global current state stays solely CURRENT_PROGRESS.

VERSION_IMPACT: NONE. No secrets/private research/source-specific proprietary implementation was introduced. Source licensed-content qualifications and attribution remain in owning input/evidence artifacts.
