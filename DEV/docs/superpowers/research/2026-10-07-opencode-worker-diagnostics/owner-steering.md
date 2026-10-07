# Owner steering after PDF diagnosis

Date: 2026-10-07. This is a local diagnostic record, not a runtime configuration change or a claim that another running session has received this instruction.

The owner explicitly prohibits this agent from downloading or parsing any PDF files. The initial owner-provided Markdown source was `/home/denis/hdm/SRD_CC_v5.2.1.md`. The owner subsequently published it as `DEV/docs/SRD_CC_v5.2.1.md`; fresh fetch and fast-forward established that file at `19da5043fad068722caf0b2c8a2204b376325db2`. Current SRD reading starts from `DEV/docs/SRD_CC_v5.2.1_ToC.md` and follows only the relevant source sections. The diagnosis did not download or parse PDFs after this instruction; only non-PDF log/DB evidence, HTML license pages and the Markdown reference were consulted.

Native `read` of the initial external Markdown path was denied by the effective external-directory policy before returning bytes. After the repository copy became available, its legal section was inspected and its source/licensing notices confirmed. Conversion quality and complete rules coverage have not been claimed from that bounded inspection. No shell bypass or configuration mutation was used.

Publication question: official D&D Beyond SRD page confirms SRD5.2.1 under CC BY4.0. The Creative Commons legal code §2(a)(1) permits whole/partial reproduction and redistribution; §2(a)(4) permits technical format conversion; §3(a) requires retaining supplied attribution/notices, source/license references and indicating modifications. Checked HTML sources:

- https://www.dndbeyond.com/srd
- https://creativecommons.org/licenses/by/4.0/legalcode.en

Repository third-party owners already identify SRD5.2.1 as CC BY4.0: `THIRD_PARTY_NOTICES.md:5–13` and `LICENSES/SRD-5.2.1-ATTRIBUTION.md:1–7`. The root software license is Apache2.0; this does not relicense the SRD text. Stable SP00 plan forbids copying complete primary spell text into public fixtures; it does not state a blanket ban on a separately attributed third-party reference document under DEV. Engine recipe/fixture obligations and independently formulated runtime content remain distinct from retaining the licensed source. No full-source file has been added or published by this diagnostic task.

The owner suspects one-day token exhaustion. Logs prove large-media context-window failures, but this diagnosis has not measured their billed-token/account-quota contribution; it must not claim that those failures account for the entire expenditure.

VERSION_IMPACT: NONE — diagnostic instruction/provenance record only; no version-bearing HDM owner or projection changed.
