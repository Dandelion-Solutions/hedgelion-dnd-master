# W04.T07A — Selected-LIVE reader system-impact brief

**DATE:** 2026-09-22
**TASK:** W04.T07A — native history publication/recovery
**PUBLISHED REVIEW BASIS:** `c37c517136a78dd57edde09320e7f1dc0fd3cb0e`
**CURRENT PUBLISHED HEAD:** `b50f490cf8dc1d5448cf3ee3c84ce4112e5f8772`
**STATUS:** **SENIOR_REVIEW_REQUIRED — T07A ONLY**

## Exact owner references

- Accepted T07A owner ruling: `DEV/docs/superpowers/design/2026-09-21-w04-t01a-t05a-t07a-senior-design-rulings.md`, §3 `SR-W04-T07A`.
- Canonical physical routing owner: `DEV/docs/superpowers/specs/2026-09-01-r2-7-WP-11-physical-storage-topology-identity-indexing-canonical-spec.md`, route law, `runtime.semantic_event`, and index rules.
- Published realization under review: `GAME/TOOLS/history.py::_read_bound_native_history` and `GAME/TOOLS/runtime_host.py::SelectedLiveTransport` at `c37c517`.

## Trigger and observed conflict

The accepted T07A ruling authorizes a narrow `campaign.semantic_events@S` / `evt`
enrollment-window adapter. The published `c37c517` realization instead reads the
LOCAL family root `LOG/SEMANTIC_EVENTS` as one aggregate. Its selected-LIVE path
asks for `read_selected_live_source(route, source)`, but the currently exposed
`SelectedLiveTransport` contract and `RuntimeHost` composition require only
`read_selected_live(campaign_id, pinned_campaign) -> LiveRouting`. That reader
does not provide the exact compact `INDEX/EVENT_INDEX.yaml` discovery plus exact
deterministic semantic-event record reads needed by the evt-lane adapter.

This is a T07A implementation/system-boundary conflict, not a T01A or T05A
finding. T01A is accepted after independent re-review at `b50f490`; T05A is
accepted after independent re-review at
`995924b2a5448dbf9ae4a52555f64de69f7fd699`.

## Protected invariants

- WP-11 known-ID reads derive one exact native route; indexes are compact
  discovery aids only and never identity, chronology, currentness, eligibility,
  publication, or absence authority.
- T07A reads only the accepted `campaign.semantic_events@S` `evt` lane, with
  stable event identity, preserved LOCAL/selected-LIVE origin, positive native
  admission ordinal, exact source revision, and bounded interval completeness.
- Selected LIVE remains exact selected-source/CAS authority; a missing or stale
  selected LIVE source never falls back to campaign data.
- History/Story/Commentator remain projections over native semantic-event
  authority; no second history payload store, global sequence, broad scan, or
  latest-looking selection is introduced.

## Required Senior choice

Identify and admit the existing host/composition route that can supply the
selected-LIVE evt lane with compact index discovery and exact deterministic
record reads, while keeping the ruling’s narrow adapter and owner boundaries; or
return that transport/composition boundary to the owning design route if no such
existing capability is available. This brief does not choose or implement a new
interface.

```text
VERSION_IMPACT: NONE
SYSTEM_IMPACT: SENIOR_REVIEW_REQUIRED — W04.T07A only
UNPUBLISHED_WORK: NONE
```
