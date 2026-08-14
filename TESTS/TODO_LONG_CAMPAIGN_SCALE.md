# TODO — Long-campaign scalability review

Deferred until real campaign usage provides meaningful data.

Review target: around 2026-09-14 or after roughly a month of actual production play, whichever makes the measurements useful.

Observe before changing architecture:
- total repository/file-count growth and whether campaign storage itself becomes noisy or expensive;
- NPC index size and lookup/context cost;
- frequency of unrelated sessions contending on the same index file;
- whether index maintenance noticeably affects persistence latency;
- whether long-campaign reads still scale with the active working set rather than total campaign age.

Do not shard indexes preemptively.

If `NPC_INDEX` or another entity index becomes a demonstrated hotspot, evaluate partitioning. Candidate approaches include stable ID-prefix/hash shards, stable anchor/home-region shards, or a small root routing index pointing to shards. Avoid using current physical location as the only partition key if that would require moving records between shards whenever an NPC travels.

Cross-location references/secondary routing may be considered if real play needs them, but avoid duplicate authoritative index state unless a clear ownership/reconciliation rule exists.

The decision should be driven by measured repository growth, lookup cost and conflict frequency, not hypothetical thousands-of-NPC scale.
