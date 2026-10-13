# SP03 Step2 requirement/case/producer/consumer/recovery/proof accounting

Basis and source IDs: accompanying [source ledger](2026-10-13-sp03-auth-turn-step2-source-ledger.md). All rows are **design obligations**, not executed PASS. `A chain` = Interaction native accepted basis + Message + Plan/unique clause + Command/root. `A reader` = bound input/auth resolver + command/preflight/retry owner. `B chain` = admitted common definition + Procedure current-turn establishing cause + Actor progress/causal basis + accepted resource/segment closure. `B reader` = bound turn/progress resolver + cast/native validator. Those shorthand mappings have exact owners and fields in [research §§3/5](2026-10-13-sp03-auth-turn-step2-research.md); they are not new runtime entities.

Proof classes: **TC** trusted-composition deterministic contract/negative test; **NP** actual native producer/atomic/recovery proof; **DP** actual connected deployment issuer proof. Existing static test body references are precedent only. No test was run in this research slice.

## Brief A — complete assigned case set

| Case | Requirement/source | Carrier + producer | Reader and recovery/retention | Expected result / required proof |
|---|---|---|---|---|
| A01 valid MP original author | G01:49, E01§3, AC02 laws1–4 | A chain; input adapter/accepted Interaction; access route owner | A reader; retain accepted origin, reacquire current bounded route+Player | Positive only with exact origin/control/currentness. TC+NP+DP; DP HELD |
| A02 foreign campaign | G01:49, ST01/AC02 law7 | I/M/K native scope + adapter campaign binding | A reader; exact routes not similar IDs | Reject/hold before RNG/cost; TC |
| A03 foreign session | G01:49, E01§3/CL01 law17 | I accepted session vs basis; plan/command association | A reader; historical accepted session not executor's new session | Reject substituted historical linkage; cold different executor session not itself rejection. TC+NP |
| A04 foreign input/message | G01:49, RT01 laws3/4 | I.input_message_id ↔ M.interaction_id + accepted representation | A reader; stable I and M independent | Reject wrong M; digest cannot authenticate. TC+NP |
| A05 foreign invocation | G01:50, E01§3/§5 | adapter exact host invocation/revision basis | A reader; retained origin after loss | Reject substituted invocation/new key masquerading retry. TC+DP HELD |
| A06 mismatched plan / duplicate or missing clause / wrong command | G01:50, J03–05/E01§4 | I↔P; K.clause; exactly one C with C.command_id=K | command/A reader; direct finite P, preserve reciprocal links | Separate negatives for wrong P, zero/two C, empty/wrong K. TC+NP |
| A07 inactive Player | G01:51, AC02 laws2/41 | current campaign Player exact body + complete account route | access/A reader; old accepted Player attribution survives | Deny new gameplay; exact retry not replay/rewrite. TC+NP |
| A08 duplicate/rebound Player | G01:51, AC02 law2/C07 | all route-nominated Player bodies, account ID/envelope-state equality | access/A reader; no first-match/index absence/scans | Duplicate/foreign/rebound/stale body hold; TC+NP |
| A09 removed/transferred PC | G01:51, AC02 laws3/28/37–41 | current Player.controlled_pc_ids + principal binding | auth/native reader; current campaign auth before mutation | Deny old controller's new agency; retain prior accepted actions. TC+NP |
| A10 false substitutes | G01:51–52/H02§2 | arbitrary principal strings, DTO flag, actor_id, publisher/gameplay verdict | public data-plane auth boundary | Each alone fails origin/control. TC+DP |
| A11 exact transport retry | G01:52/54, E01§5, CL01 laws17/33 | stored I/K identity + accepted origin/fingerprint/result | retry lookup before ambient binding; protected idempotency anchor | Same accepted outcome/suspension, zero spend/RNG. TC+NP+DP HELD |
| A12 later identical prose | G01:52/54, E01§3/CL01 law34 | fresh adapter identity/new I despite same text | acceptance/current auth | New intentional input; not coalesced by digest/prose. TC+DP HELD |
| A13 edit / branch / regeneration | G01:52, RT01 laws2/21/22 | immutable accepted I/M/K; new correction input | recovery current routes, not host old cursor | No retcon/replay; branch recovers current campaign. TC+NP+DP HELD |
| A14 fresh Choice / Reaction response | G01:55, E01§13/J14–16 | new authenticated response basis + current generation/offer/responder/option | native resume/single-consume; fixed root inputs preserved | Responder can differ from root author; stale/foreign/wrong-option denies, no double consume. TC+NP+DP |
| A15 no-Player creator | G01:53/164–166, AC01:29–51/AC03 | creator_singleplayer I basis + native history + current login; message direction variant | creator auth/A reader; own I rooted and routed, not M | Positive only through history/current-login, no fake Player. TC+NP+DP |
| A16 creator login rename/unresolvable | G01:53, AC03 items1–7 | accepted immutable creator history vs current authenticated login | creator auth/read-only eligibility | Creator write fails closed; stable ID/admin does not repair. TC+DP |
| A17 cold durable resume / handle lost | G01:53, RC01 laws5/6/12, RC02 laws8/10/22 | durable A chain and fixed Continuation/execution; no process handle | recovery exact owner source+interpretation; derived handle reissue | Reconstruct accepted origin, no replay; current authority reacquired. TC+NP+DP |
| A18 unresolved pre-command input promise | G01:145–146, RC01§4.5, RC03 law13 | I/P/M material semantics or exact input; actual handoff promise/root companion | recovery/durability; all closure enters promised boundary | Promise-dependent root; no all-message immediate publication; prepromise SOFT loss not invented. TC+NP |
| A19 content compaction | G01:141–147/153, RT01 laws8–15, CL01 laws18–22 | normalized clause + origin provenance + exact slices if required | accepted semantic consumers/compactor/recovery | Retain until content sufficient; hash-only survivor fails. TC+NP |
| A20 acceptance vs compaction/retirement race | G01:167–169, RT03 law2/RT02 P1–P9 | forward accepted dependency + cleanup-visible protection/sufficient survivor/fence | acceptance and cleanup exact basis before edge | No eventual enrollment gap; missing negative proof retains. TC+NP failure injection |
| A21 I≠M/root/durability repair | G01:164–166, C05/C12/C14/C18/X06 | Interaction own envelope I, message M; root and route I | hydration/handoff/publication/collaboration | Distinct exact routes in MP and creator cases; no stranded root or ID alias. TC+NP |
| A22 controller change while waiting | G01:56, CL01 law27/32–40/AC02 | original immutable input vs current offer/obligation+Player | native response/collection owner; historical associations kept | Revalidate generation/opportunity; obsolete/successor only when lawful; no fabricated consent. TC+NP |
| A23 continuation with further protected work | G01:55–57, E01§13/AC02/CL01 | fixed original cause + current executor/input/purpose | execution/native auth; preserve accepted dependencies | Automatic descendants vs new voluntary input distinguished; current publisher alone insufficient, universal old-author equality forbidden. TC+NP+DP |
| A24 unavailable deployed issuer | G01:128–132/154–156, H01/H02/RT03 law5 | actual connected supported host observation unavailable | deployment acceptance gate, not local DTO validator | A positive deployed claim held; local absence≠platform impossibility. DP HELD |

## Brief B — complete assigned case set

| Case | Requirement/source | Carrier + producer | Reader and recovery/retention | Expected result / required proof |
|---|---|---|---|---|
| B01 exact active combat subtype | G01:85, DM01§4/J07 | concrete Procedure envelope/state/current start cause; registered native producer | B reader, active Procedure root | Positive observation only full definition/current occurrence/progress; TC+NP |
| B02 generic Procedure as combat | G01:85, J07/08 | distinct generic spent vs concrete capacity grammar | subtype validator/B reader | Reject flatten/substitution; generic progress cannot relocate gate. TC |
| B03 malformed permutation/budget/index/phase | G01:85–86, C11:198–215/J07 | exact participant permutation/resource keys/spent≤capacity/index/no pending active round | concrete native validator; exact route | Separate negative for each invariant, terminal/between-turn held; TC |
| B04 wrong participant | G01:86, DM01§4/C11 | Procedure start/spend participant vs actual active participant | turn/budget validator | Wrong Procedure action actor denies; not a blanket caster=active rule. TC+NP |
| B05 caster reaction on another creature's turn | G01:72/86, E02§5/E01§13 | actual other participant's turn occurrence + caster Actor gate | B reader + exact reaction cost owner; current response authority A | Gate uses actual other turn, action/reaction budgets separate. TC+NP |
| B06 second slot via other source | G01:87, G03:88–93 | one common gate across spell/class/item/mode; actual accepted slot cause | native cost/gate validator; retained current consumed cause | Reject second slot, no per-source bypass; TC+NP |
| B07 slotless source | G01:73/87, E02§5 | exact source slotless cost + common progress | preflight/native cost owner | No slot-gate consumption; source cost still applies. TC+NP |
| B08 ritual | G01:73/87, E02§5 | admitted ritual profile/actual time/components | source/native cost reader | No slot gate consume; no import ordinary slot cost. TC+NP |
| B09 countered without slot | G01:73/87, E02§5 | actual accepted Counterspell interruption/action boundary | native cast/reaction owner | Action spent per source; interrupted slot not spent/gate unconsumed. TC+NP |
| B10 interrupted long cast without slot | G01:73–74/87, E02§5 | long-cast Procedure/concentration interrupted before actual slot boundary | native lifecycle/cost owner | No slot consume/refund fiction; accepted other costs retained. TC+NP |
| B11 long start vs actual completion slot | G01:74/87, E02§5 | preparation/repeated Magic action vs accepted slot expenditure segment | B reader/native spend owner; stable execution | Start alone not consume; only actual slot boundary consumes same actual turn. TC+NP |
| B12 missing definition/progress/occurrence | G01:82–83/88, E03§8 | exact common descriptor/native progress/Procedure cause | B reader; no shape/string inference | Hold, never implicit unused=false/zero-cost permission; TC |
| B13 forged/wrong producer | G01:88, E01§17/TM01 law4 | native start producer/profile/generation/segment/local key | owner issued resolver from validated native basis | Reject arbitrary BoundaryOccurrence DTO/DEV receipt as issuer. TC+NP |
| B14 wrong scope/cause | G01:88, E01§17/RT03 | common subject/Procedure/cast execution/resource cause closure | B reader/native validator, direct protected cause basis | Reject wrong subject/provider/segment/slot cause even valid strings. TC+NP |
| B15 retry of same turn/reset/spend | G01:88–89, E01§5/10/TM01 | stable occurrence/start/reset/spend segment and stored outcome | lookup before fresh work; protected idempotency anchor | Same occurrence/one reset/one consume; no fresh false on retry. TC+NP |
| B16 equal round/index in distinct Procedure vs actual next turn | G01:88–89, TM01 law4/DM01 | Procedure identity+start segment+local boundary; seven transition mapping | B reader/native turn lifecycle | Distinct Procedure/start cause distinct, numeric equality insufficient; next genuine start new occurrence. TC+NP |
| B17 first-use/reset admission | G01:67–68/169–170, E03§8 | lawful Actor native initialization/reset + source admission/no prior hidden spend | B reader holds until actual producer; lazy exact subject or finite eager enrollment | Missing alone cannot initialize; reenrollment cannot erase same-turn spend. TC+NP |
| B18 crash around reset | G01:89, E01§9/HT01 law8/TM01 | coupled native reset/progress/cause/continuity/readset | recovery same promised durable closure | Before none; after same actual cause/progress; reader does not reset on recovery. NP crash injection |
| B19 crash around spend | G01:89, E01§9/E02§6 | progress/resource/fixed execution/event/receipt/dirty closure | native recovery/idempotency | Never slot spent+unused or consumed+unspent acknowledged; no double spend/RNG. NP |
| B20 termination/provider movement | G01:89, TM03 laws15–17/39–45/TM04 | current owner provider/Procedure terminality + retained accepted causal basis | exact native route re-resolution; old open dependencies protected | No new turn/reset from termination/movement; missing provider holds; NP |
| B21 cold recovery after old details compact | G01:90/141–147, TM03 laws26/43–50/RT02 | sufficient compact native gate/start/cost witness + existing exact sources | B reader reissues transient BoundaryOccurrence; bounded direct evidence | Same lawful gate/cause answer; hash or ordering summary not causal content. TC+NP |
| B22 LIVE movement + compaction race / split atomic domain | G01:90/167–169, RT03 law2/HT01/LV01/AC02 | current exact claimed Procedure/Actor/resource + protection/survivor/root movement | native source establishment/recovery/cleanup | Confirm survivor/protection first; CAS acceptance only, no SQLite+Git atomicity/half-spend, no all-LIVE scan. NP |
| B23 split principal/body/source/payer | G01:90–91, E02§4/E03§2/3 | exact compiled source-specific subject/control generation; one Actor gate owner | native subject/cost reader; preserve accepted binding | Ordinary witness cannot grant split equality/second gate; unproved split held. TC+NP |
| B24 unrelated revision/save/restart/absorption | G01:78–79, TM01 law11/TM04 laws38/39/45/46 | unchanged actual occurrence/progress amid technical movement | B reader/recovery | Same turn, no fresh gate/fiction/RNG; TC+NP |

## Cross-check of framing additions

| Retained brief addition | Accounting |
|---|---|
| Step5.2 laws2–13/§§4–6 and WP14 laws6–11/20–26 | Source RC01/02; A17/A18/A21/B18–B22; conditional root/promise, current authority + historical inputs |
| Step5.5/5.6/WP13 + Step5.8/WP16 | DU01–03/LV01/AC02; A09/A17/A20/B18/B19/B22 |
| Step5.14 laws2/5 with Step5.11/5.13 | RT01–03; A19/A20/A24/B21/B22 |
| WP17 laws16–22/27/32–40/material source retention | CL01; A06/A11–A14/A18/A19/A22/A23 |
| R2.6/host composition/WP16law1/actual adapter/current official route | H01–03/C01/C22; A01/A05/A11–A16/A24; DP held explicitly |
| WP11/WP12/HOT/recovery/durability/publication/LIVE/schemas/tests | ST01/HT01/C04–05/C12–17/J17–22/X01–06; A17/A21/B18–B22 |
| Input/Continuation/Choice/Reaction/execution/collaboration/history/context/turn/access/emission | J01–06/J13–16/C06–08/C18–22; A01–A24/B05/B23 |
| Full applicable version/clean-slate/WP20/WP25/native failures | V01–04/F01/J19/J21–22; main§7, all holds retain native distinctions |
| Domain coverage/concrete Procedure/native conformance producer | DM01/J07/J20–21/C11; B01–B04/B13/B16 |
| recovery_roots Player + input_message_id identity | C12/C14/C18/X04/X06; A15/A18/A21, one coherent identity repair |
| recovery858–897 not new closure proof | C13; A17/B18–B22, future extension not present PASS |
| Protection acceptance/movement races and finite enrolled alternative | A20/B17/B22; main§5/§6 and analytical gate |

Counts: 24 A cases + 24 B cases. Matrix is the assignment's complete disposition inventory, **not 48 passing tests**. Broader full preflight/support cases remain outside this two-bridge slice.
