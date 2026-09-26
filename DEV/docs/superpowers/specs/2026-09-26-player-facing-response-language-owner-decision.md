# HDM Player-Facing Response Language Owner Decision

Status: **ACCEPTED OWNER DECISION / PO-011 INCORPORATED / IMPLEMENTATION ROUTED**

Date: 2026-09-26

Product input: `DEV/PRODUCT_OWNER_INPUT.md` — PO-011.

## 1. Decision

HDM separates the language of human-visible Master communication from the language of internal machine/system representation.

The current ordinary human-visible response has one transient semantic basis:

```text
ResolvedResponseLanguage
```

It determines the language targeted by Master-to-human communication for that response.

It is not a persistent PLAYER preference, campaign/state authority, language-policy/plugin identifier, catalog generation, knowledge/disclosure owner, or permission to add another model call merely for translation.

PO-011 does not require a persistent PLAYER language/locale field.

## 2. Master-to-human law

All ordinary human-visible Master communication MUST target the current `ResolvedResponseLanguage`, including where applicable:

- Narrator prose;
- OOC Master answers;
- clarification/control acknowledgements;
- finite fallback, degradation, unavailability and safety notices;
- player-facing bootstrap/session/setup notices;
- player-facing mechanical explanations.

A missing optional language-specific style/quality policy, local phrase catalog or language-specialized asset:

```text
does not block the requested response language
does not authorize visible fallback to English
does not authorize visible fallback to Russian
does not authorize visible fallback to any other language
```

If required player-visible text cannot be realized in the current response language, HDM follows the applicable fail/degrade/no-delivery contract. It does not silently switch the Master to another visible language.

## 3. Internal and diagnostic language

Internal and technical representations may remain English/technical where appropriate, including machine IDs, enum/status/error codes, schema/property names, tool/connector internals, logs/traces and raw maintenance/debug records.

Those values do not become ordinary Master utterances merely because they are available to the runtime.

A diagnostic/debug surface is a separate technical surface. Raw technical diagnostic material may retain its technical language when intentionally exposed as diagnostics and after recipient/disclosure checks.

If the Master explains, summarizes or acknowledges a diagnostic result through the ordinary Master channel, that Master-authored human communication again follows `ResolvedResponseLanguage`.

## 4. Foreign-language content is not a fallback-language switch

The response-language law controls the Master communication carrier; it does not rewrite content whose identity or meaning requires another language.

Eligible exact or diegetic material may remain in another language where semantically required, for example:

- an exact inscription, code or quotation;
- a character's deliberately foreign-language utterance;
- a proper name or term whose identity is preserved;
- text explicitly being translated or discussed as an object.

Surrounding Master explanation remains in `ResolvedResponseLanguage`.

This exception does not permit internal diagnostics, fallback prose or machine labels to leak into ordinary narration.

## 5. Resolution and lifetime

`ResolvedResponseLanguage` is a transient presentation/control value for the relevant human-visible response.

The baseline may resolve it from the active human conversation and explicit/current communicative intent. Exact language-detection algorithms are not selected by this decision.

It may be carried through one turn/response as an ephemeral typed control so Narrator and emission can prove agreement on the intended response language.

This decision does not authorize silent cross-session learning of a durable language preference. A future requirement for durable language preference/personalization needs its own owner, provenance and lifecycle decision.

## 6. T06B realization boundary

W04.T06A remains unchanged: it owns phase/context rebinding and accepted Context basis, not response-language realization.

W04.T06B is the first active machine consumer.

Minimum realization:

```text
current ResolvedResponseLanguage
  -> transient Narrator phase binding
  -> narration_result response-language binding
  -> protected emission equality/current-turn check
  -> visible payload
```

The implementation may use a nonempty opaque language identifier for equality/binding within the current turn. This decision creates no global language registry.

T06B SHALL:

1. require Narrator result language binding to equal the accepted current Narrator phase language basis;
2. reject caller-shaped/raw/unbound language claims;
3. keep finite fallback IDs semantic/internal until player-visible realization;
4. require player-visible fallback text to use the same accepted response-language basis;
5. prevent internal role keys, enum/status tokens and diagnostic text from becoming ordinary visible prose;
6. preserve protected Context/disclosure and execution-handoff requirements;
7. add no new persistent language state and no extra model call solely for language conversion.

Deterministic code is not required to infer the natural language of generated prose. Machine proof owns binding/currentness; prompt/role instructions and later acceptance/evaluation own language-realization quality.

## 7. Diagnostics / maintenance composition

The maintenance architecture remains the diagnostics/authorization/disclosure owner.

```text
ordinary Master reply
  -> ResolvedResponseLanguage

separate technical diagnostic artifact/record
  -> technical language permitted
  -> recipient/disclosure filtering still mandatory

Master explanation of that diagnostic
  -> ResolvedResponseLanguage
```

Debug/diagnostic enablement MUST NOT change gameplay truth, information eligibility, model authority, Narrator language basis or campaign state.

## 8. Current and future consumers

```text
PO-011 semantic owner
  -> W04.T06B protected Narrator emission
  -> W04.T08B visible session/status consumer where applicable
  -> W05 shipped bootstrap/session/setup/AI/policy/install projections
  -> W06 negative/currentness + exact-head proof
```

Current W04.T07 Story/Commentator semantics are not reopened by this decision.

Private CLS implementation remains a separate subsystem. Cross-project compatibility follows the existing CLS↔HDM coordination process; private implementation details are not public HDM authority.

## 9. Non-goals

PO-011 does not authorize:

- persistent PLAYER language state solely for this requirement;
- a global language-policy registry as a prerequisite for speaking a language;
- English/Russian hard-coded player-visible fallback;
- translating every machine identifier;
- treating diagnostics as ordinary Master narration;
- an extra model invocation solely to localize already-generated Master prose;
- language choice becoming knowledge/disclosure/authorization authority.

## 10. Impact

```text
VERSION_IMPACT: NONE for this owner/control publication
SYSTEM_IMPACT: bounded existing presentation/emission consumer; no new authority or persistence owner
MIGRATION: NONE
DUAL_READ: NONE
PRODUCT_OWNER_DECISION_REQUIRED: NONE
```

T06B still runs the normal Version Impact Gate against its actual transient code/schema changes.

## 11. Current gate

```text
PO-011: INCORPORATED
W04.T06A: MAY CONTINUE
W04.T06B: MUST CONSUME THIS OWNER BEFORE RED
W04.T07D: UNAFFECTED / MAY CONTINUE
WAVE_05: still unauthorized until the existing Wave-04 gate
```
