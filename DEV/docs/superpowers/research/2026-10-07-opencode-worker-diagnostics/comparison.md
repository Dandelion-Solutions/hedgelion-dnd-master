# Bounded comparison evidence

Source: `/home/denis/.local/share/opencode/opencode.db`, supported `opencode db` SELECTs; independent read-only diagnostic agent `ses_eea03cea2ffeHC3bbIc7Voc2GU`. Parent in every row: `ses_f0e3bd4e4ffem8jmapJbWHWjLz`. Millisecond timestamps are original DB values; durations are `(end-start)/1000`. Text dispositions below summarize returned responses, not acceptance of their technical claims.

| Child / episode | Parent task part ID | Start ms | End ms | Duration seconds | Persisted terminal state / return |
|---|---|---:|---:|---:|---|
| `ses_ef4efdaacffesFcTKCaW6bIgLg` P2 initial | `prt_10b102542001YgZi8QLMYnqJ5j` | 1791186969947 | 1791187319138 | 349.191 | completed; Senior review required, no production changes |
| same P2 preparation | `prt_10b93b7f9001IpPFoFLNzWrrih` | 1791195592713 | 1791198218804 | 2626.091 | completed; preparatory slice returned; full P2 held |
| `ses_eed992904ffetnnsCdZm0LOxUX` SP02 initial | `prt_11266d61c001m6lnKJPIXYZ9Jz` | 1791310092039 | 1791310824889 | 732.850 | completed; technical System-Impact gate |
| same SP02 resumed | `prt_1128260a4001GhtP2EQFfpjmF2` | 1791311897133 | 1791323665377 | 11768.244 | completed; dirty implementation delta returned |
| same SP02 freeze | `prt_11336dec7001IaLuqyQZ0PX1UU` | 1791323725585 | 1791324963215 | 1237.630 | completed; local candidate commit returned |
| same SP02 F1–F5 repair | `prt_11387775f001LhviQjlctC3h8U` | 1791329007477 | 1791337770365 | 8762.888 | completed; repair incomplete, explicit System-Impact gate |
| `ses_eeb20c6a0ffeDCYxnnj59coD9g` SP03 initial | `prt_114df3950001jaDoRG5W6LprWM` | 1791351535990 | 1791352851104 | 1315.114 | completed; safe partial commit, full task held |
| same SP03 repair | `prt_11515ca1c001vby36j5ncDRhBO` | 1791355120476 | 1791355892226 | 771.750 | completed; repair returned review-ready |

UTC windows: P2 2026-10-05 07:56:09–08:01:59 and 10:19:52–11:03:38; SP02 2026-10-06 18:08:12–18:20:24, 18:38:17–21:54:25, 21:55:25–22:16:03 and 23:23:27–2026-10-07 01:49:30; SP03 2026-10-07 05:38:55–06:00:51 and 06:38:40–06:51:32. Rounded for display only; calculations use original milliseconds.

| Episode | Terminal assistant message | Final text part | Assistant completed ms |
|---|---|---|---:|
| P2 initial | `msg_10b148335001GM7dx4RnLYsZrf` | `prt_10b149240001VQ9MpFc9h3F1Pl` | 1791187313663 |
| P2 preparation | `msg_10bb98b320010a1RGlmN7w8Lye` | `prt_10bbacf970010qHPxGGbyjbC0o` | 1791198213588 |
| SP02 initial | `msg_112718f04001a2buYnjzOecLul` | `prt_11271e0980014VCMGfEuV1Ooe4` | 1791310820375 |
| SP02 resumed | `msg_1133215dc0015eCTcCIuGOApKp` | `prt_11335ca390012zrR0OAwXJt2TZ` | 1791323659153 |
| SP02 freeze | `msg_1134811fe001ENxq0bmHJvw5Ch` | `prt_113494cb7001mGkSL2DtmRkOKS` | 1791324957736 |
| SP02 F1–F5 repair | `msg_1140cbcd0001obTz4sSlbMDlmj` | `prt_1140cf716001gujrtIJzH4GEMu` | 1791337763428 |
| SP03 initial | `msg_114f305440017pu94L4lXKvE0G` | `prt_114f310c9001a3FLXdq9cf6a37` | 1791352846750 |
| SP03 repair | `msg_115216dbd001d71nYIvusNMbch` | `prt_115217bad001lXqGWJ4bNqrlXE` | 1791355886022 |

All eight terminal messages have `finish=stop`, `error=NULL`, and completion before parent task end. All eight episodes have zero pending/running child tool parts.

| Whole child session | Messages / assistants | Incomplete assistants / assistant errors | Completed / errored tool parts | Pending/running tool parts |
|---|---:|---:|---:|---:|
| original P2 | 106 / 104 | 0 / 0 | 150 / 5 | 0 |
| original SP02 | 864 / 856 | 0 / 0 | 1135 / 41 | 0 |
| SP03 | 98 / 96 | 0 / 0 | 163 / 7 | 0 |

Conclusion: these are useful controls for long execution and explicit gates, not confirmed comparable hangs. The normal replacement-SP01 verification at the exact `651c70d5` bytes is an additional, closer control: `evidence.jsonl:22–23`. There is insufficient evidence for a replicated hang cause.
