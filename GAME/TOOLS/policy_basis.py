"""Ephemeral verification of the exact House-Rules basis for accepted input.

This module is deliberately a read-side adapter.  Repository, access-control,
currentness and catalog owners remain authoritative; this adapter does not
persist proof, create a policy epoch, or select a current policy on its own.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
import re
from types import MappingProxyType
from typing import Final, Protocol

from .catalog_runtime import (
    BoundCatalogContext,
    CatalogBindingError,
    bind_interpreter_candidate,
    validate_executable_binding,
)


# framework_module_version: 1.0.1
HOUSE_RULES_SIDECAR_PATH: Final = "RULES/HOUSE_RULES.yaml"
HOUSE_RULES_MANIFEST_PATH: Final = "MANIFEST.yaml"
_REVISION_PATTERN: Final = re.compile(r"^[a-f0-9]{40}(?:[a-f0-9]{24})?$")
_POLICY_ID_PATTERN: Final = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")
_ID_PATTERN: Final = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")
_HEADING_PATTERN: Final = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*$")
_FORBIDDEN_UNTRUSTED_FIELDS: Final = frozenset(
    {"authority_validated", "applicable", "campaign_revision", "source_path"}
)
_ADJUDICATED_BINDING_FIELDS: Final = frozenset(
    {
        "source_class",
        "value",
        "provenance_ref",
        "eligibility_basis_fingerprint",
        "rules_context_fingerprint",
        "policy_basis_refs",
        "candidate_set_fingerprint",
    }
)
_INVOCATION_FACT_FIELDS: Final = frozenset(
    {
        "fact_id",
        "value",
        "provenance_class",
        "provenance_ref",
        "consumer_id",
        "binding_fingerprint",
        "rules_context_fingerprint",
        "policy_basis_refs",
    }
)


class PolicyBasisResolutionError(ValueError):
    """A pinned policy basis cannot be admitted for deterministic execution."""

    failure_code: str

    def __init__(self, message: str, *, failure_code: str = "failure.adjudication_input_invalid"):
        super().__init__(message)
        self.failure_code = failure_code


class RepositoryPort(Protocol):
    """Exact campaign currentness/read capability supplied by the runtime owner."""

    def pin_campaign(self, campaign_id: str) -> PinnedCampaign:
        """Return the authoritative campaign revision selected by the owner."""

    def read_exact_path(self, pinned: PinnedCampaign, path: str) -> object:
        """Read one path from the exact pinned commit/tree."""


class AccessControlPort(Protocol):
    """Existing authenticated-principal, creator and PLAYER authority owner."""

    def resolve_principal(self, pinned: PinnedCampaign) -> AuthenticatedPrincipalEvidence:
        """Resolve the current authenticated principal for the pinned campaign."""

    def resolve_creator(self, pinned: PinnedCampaign) -> CreatorEvidence:
        """Resolve creator provenance for the pinned campaign."""

    def resolve_active_player(
        self, pinned: PinnedCampaign, principal: AuthenticatedPrincipalEvidence
    ) -> PlayerEvidence | None:
        """Resolve the one active PLAYER bound to the authenticated principal."""

    def prove_policy_adoption(
        self,
        pinned: PinnedCampaign,
        policy: Mapping[str, object],
        principal: AuthenticatedPrincipalEvidence,
        creator: CreatorEvidence,
        player: PlayerEvidence | None,
    ) -> AdoptionEvidence:
        """Prove policy-adoption authority through the native access owner."""


class ApplicabilityPort(Protocol):
    """Existing Context Runtime/currentness owner for policy eligibility."""

    def prove_policy_applicability(
        self, pinned: PinnedCampaign, policy: Mapping[str, object], consumer_id: str
    ) -> ApplicabilityEvidence:
        """Prove applicability; failure is represented by raising, not a caller flag."""


def _nonempty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise PolicyBasisResolutionError(f"{label} must be a nonempty string")
    return value


def _native_id(value: object, label: str) -> str:
    value = _nonempty_string(value, label)
    if _ID_PATTERN.fullmatch(value) is None:
        raise PolicyBasisResolutionError(f"{label} must be a native identifier")
    return value


def _revision(value: object, label: str) -> str:
    if not isinstance(value, str) or _REVISION_PATTERN.fullmatch(value) is None:
        raise PolicyBasisResolutionError(f"{label} must be an exact lowercase commit revision")
    return value


def _mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise PolicyBasisResolutionError(f"{label} must be an object")
    return value


def _string_array(value: object, label: str, *, allow_empty: bool = True) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise PolicyBasisResolutionError(f"{label} must be an array")
    values = tuple(_nonempty_string(item, f"{label} item") for item in value)
    if not allow_empty and not values:
        raise PolicyBasisResolutionError(f"{label} must not be empty")
    if len(values) != len(set(values)):
        raise PolicyBasisResolutionError(f"{label} must be unique")
    return values


def _deep_freeze(value: object) -> object:
    if isinstance(value, Mapping):
        return MappingProxyType({key: _deep_freeze(item) for key, item in value.items()})
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return tuple(_deep_freeze(item) for item in value)
    return value


def _thaw(value: object) -> object:
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [_thaw(item) for item in value]
    return value


@dataclass(frozen=True, slots=True)
class PinnedCampaign:
    """Opaque result of the native campaign currentness/pinning owner."""

    campaign_id: str
    revision: str
    tree_sha: str

    def __post_init__(self) -> None:
        _native_id(self.campaign_id, "pinned campaign_id")
        _revision(self.revision, "pinned campaign revision")
        _revision(self.tree_sha, "pinned campaign tree")


@dataclass(frozen=True, slots=True)
class PolicySelection:
    """Typed semantic policy selection; paths, revisions and trust flags are absent."""

    policy_id: str
    consumer_id: str

    def __post_init__(self) -> None:
        policy_id = _native_id(self.policy_id, "policy_id")
        consumer_id = _native_id(self.consumer_id, "consumer_id")
        if policy_id != self.policy_id or consumer_id != self.consumer_id:
            raise PolicyBasisResolutionError("policy selection contains a noncanonical identifier")


@dataclass(frozen=True, slots=True)
class AuthenticatedPrincipalEvidence:
    """Principal evidence returned by the authenticated access owner."""

    principal_id: str

    def __post_init__(self) -> None:
        _native_id(self.principal_id, "authenticated principal_id")


@dataclass(frozen=True, slots=True)
class CreatorEvidence:
    """Creator provenance evidence returned by the campaign ownership owner."""

    principal_id: str

    def __post_init__(self) -> None:
        _native_id(self.principal_id, "creator principal_id")


@dataclass(frozen=True, slots=True)
class PlayerEvidence:
    """Active PLAYER evidence returned by the campaign access owner."""

    player_id: str
    mechanical_override_policy: bool

    def __post_init__(self) -> None:
        _native_id(self.player_id, "active PLAYER id")
        if not isinstance(self.mechanical_override_policy, bool):
            raise PolicyBasisResolutionError("PLAYER mechanical override evidence must be boolean")


@dataclass(frozen=True, slots=True)
class AdoptionEvidence:
    """Typed adoption proof returned by the existing access-control owner."""

    authority_class: str
    adoption_basis: str
    adopted_by_player_id: str | None

    def __post_init__(self) -> None:
        if self.authority_class not in {"INTERPRETIVE_POLICY", "MECHANICAL_OVERRIDE_POLICY"}:
            raise PolicyBasisResolutionError("unsupported adoption authority class")
        if self.adoption_basis not in {
            "campaign_creator",
            "active_player_interpretive",
            "creator_delegated_mechanical_override",
        }:
            raise PolicyBasisResolutionError("unsupported policy adoption basis")
        if self.adopted_by_player_id is not None:
            _native_id(self.adopted_by_player_id, "adopted_by_player_id")


@dataclass(frozen=True, slots=True)
class ApplicabilityEvidence:
    """Typed applicability evidence returned by the existing context owner."""

    policy_id: str
    consumer_id: str

    def __post_init__(self) -> None:
        _native_id(self.policy_id, "applicable policy_id")
        _native_id(self.consumer_id, "applicable consumer_id")


@dataclass(frozen=True, slots=True, init=False)
class ResolvedPolicyBasis:
    """Ephemeral verified evidence; no persistence/serialization API is provided."""

    campaign_id: str
    campaign_revision: str
    policy_id: str
    policy_ref: str
    consumer_id: str
    authority_class: str
    adoption_basis: str
    adopted_by_player_id: str | None
    source_path: str
    source_anchor: str
    realization_refs: tuple[str, ...]
    realization_bindings: tuple[Mapping[str, object], ...]

    def __init__(
        self,
        *,
        campaign_id: str,
        campaign_revision: str,
        policy_id: str,
        policy_ref: str,
        consumer_id: str,
        authority_class: str,
        adoption_basis: str,
        adopted_by_player_id: str | None,
        source_path: str,
        source_anchor: str,
        realization_refs: tuple[str, ...],
        realization_bindings: tuple[Mapping[str, object], ...],
        _verified: object = None,
    ) -> None:
        if _verified is not _VERIFIED_BASIS_SEAL:
            raise PolicyBasisResolutionError("resolved policy basis must come from PolicyBasisResolver")
        object.__setattr__(self, "campaign_id", campaign_id)
        object.__setattr__(self, "campaign_revision", campaign_revision)
        object.__setattr__(self, "policy_id", policy_id)
        object.__setattr__(self, "policy_ref", policy_ref)
        object.__setattr__(self, "consumer_id", consumer_id)
        object.__setattr__(self, "authority_class", authority_class)
        object.__setattr__(self, "adoption_basis", adoption_basis)
        object.__setattr__(self, "adopted_by_player_id", adopted_by_player_id)
        object.__setattr__(self, "source_path", source_path)
        object.__setattr__(self, "source_anchor", source_anchor)
        object.__setattr__(self, "realization_refs", realization_refs)
        object.__setattr__(self, "realization_bindings", realization_bindings)


_VERIFIED_BASIS_SEAL: Final = object()


def _policy_ref(policy_id: str, revision: str) -> str:
    return f"{policy_id}@{revision}"


def _validate_policy_ref(value: object, label: str) -> str:
    if not isinstance(value, str) or "@" not in value:
        raise PolicyBasisResolutionError(f"{label} must be an exact policy_id@revision reference")
    policy_id, revision = value.rsplit("@", 1)
    if _POLICY_ID_PATTERN.fullmatch(policy_id) is None:
        raise PolicyBasisResolutionError(f"{label} has an invalid policy identity")
    _revision(revision, label)
    return value


def _normalize_refs(value: object, label: str) -> tuple[str, ...]:
    if not isinstance(value, list):
        raise PolicyBasisResolutionError(f"{label} must be a list")
    refs = tuple(_validate_policy_ref(item, f"{label} item") for item in value)
    if len(refs) != len(set(refs)):
        raise PolicyBasisResolutionError(f"{label} must contain unique references")
    if refs != tuple(sorted(refs)):
        raise PolicyBasisResolutionError(f"{label} must be unique and lexicographically sorted")
    return refs


def _validate_parameter_bindings(value: object) -> dict[str, object]:
    raw = _mapping(value, "parameter_bindings")
    result: dict[str, object] = {}
    for parameter_id, raw_binding in raw.items():
        parameter = _native_id(parameter_id, "parameter id")
        if isinstance(raw_binding, Mapping) and raw_binding.get("source_class") == "INVOCATION_ADJUDICATED":
            if set(raw_binding) - _ADJUDICATED_BINDING_FIELDS or not {
                "source_class",
                "value",
                "provenance_ref",
                "eligibility_basis_fingerprint",
                "rules_context_fingerprint",
                "policy_basis_refs",
            }.issubset(raw_binding):
                raise PolicyBasisResolutionError("adjudicated parameter binding has unexpected or missing fields")
            if _FORBIDDEN_UNTRUSTED_FIELDS & set(raw_binding):
                raise PolicyBasisResolutionError("adjudicated parameter binding contains untrusted authority fields")
            scalar = raw_binding["value"]
            if isinstance(scalar, (Mapping, list, tuple)):
                raise PolicyBasisResolutionError("adjudicated parameter value must be scalar")
            refs = _normalize_refs(raw_binding["policy_basis_refs"], "policy_basis_refs")
            normalized = {key: deepcopy(raw_binding[key]) for key in raw_binding}
            normalized["policy_basis_refs"] = list(refs)
            result[parameter] = normalized
        else:
            if isinstance(raw_binding, Mapping) and _FORBIDDEN_UNTRUSTED_FIELDS & set(raw_binding):
                raise PolicyBasisResolutionError("parameter binding contains untrusted authority fields")
            result[parameter] = deepcopy(raw_binding)
    return result


def _validate_invocation_facts(value: object) -> list[dict[str, object]]:
    if not isinstance(value, list):
        raise PolicyBasisResolutionError("invocation_facts must be a list")
    facts: list[dict[str, object]] = []
    seen: set[tuple[str, str]] = set()
    for raw_fact in value:
        fact = _mapping(raw_fact, "invocation fact")
        if set(fact) != _INVOCATION_FACT_FIELDS:
            raise PolicyBasisResolutionError("invocation fact has unexpected or missing fields")
        if _FORBIDDEN_UNTRUSTED_FIELDS & set(fact):
            raise PolicyBasisResolutionError("invocation fact contains untrusted authority fields")
        fact_id = _native_id(fact["fact_id"], "invocation fact_id")
        consumer_id = _native_id(fact["consumer_id"], "invocation consumer_id")
        if not isinstance(fact["value"], bool):
            raise PolicyBasisResolutionError("invocation fact value must be boolean")
        if fact["provenance_class"] != "INVOCATION_ADJUDICATED":
            raise PolicyBasisResolutionError("invocation fact provenance class is not admitted")
        _nonempty_string(fact["provenance_ref"], "invocation fact provenance_ref")
        _nonempty_string(fact["binding_fingerprint"], "invocation fact binding_fingerprint")
        _nonempty_string(fact["rules_context_fingerprint"], "invocation fact rules_context_fingerprint")
        refs = _normalize_refs(fact["policy_basis_refs"], "invocation fact policy_basis_refs")
        key = (fact_id, consumer_id)
        if key in seen:
            raise PolicyBasisResolutionError("invocation fact identities must be unique")
        seen.add(key)
        normalized = {key: deepcopy(fact[key]) for key in fact}
        normalized["policy_basis_refs"] = list(refs)
        facts.append(normalized)
    return facts


def _refs_in_inputs(parameter_bindings: Mapping[str, object], invocation_facts: Sequence[Mapping[str, object]]) -> tuple[str, ...]:
    refs: set[str] = set()
    for binding in parameter_bindings.values():
        if isinstance(binding, Mapping) and binding.get("source_class") == "INVOCATION_ADJUDICATED":
            refs.update(binding["policy_basis_refs"])
    for fact in invocation_facts:
        refs.update(fact["policy_basis_refs"])
    return tuple(sorted(refs))


@dataclass(frozen=True, slots=True)
class AcceptedAdjudicationBasis:
    """Complete frozen parameter/fact input plus ephemeral resolver witnesses."""

    parameter_bindings: Mapping[str, object]
    invocation_facts: tuple[Mapping[str, object], ...]
    verified_policies: tuple[ResolvedPolicyBasis, ...]

    def __post_init__(self) -> None:
        parameters = _validate_parameter_bindings(self.parameter_bindings)
        facts = _validate_invocation_facts(list(self.invocation_facts))
        policies = tuple(self.verified_policies)
        if any(not isinstance(policy, ResolvedPolicyBasis) for policy in policies):
            raise PolicyBasisResolutionError("accepted basis requires resolver-produced policy evidence")
        policy_refs = tuple(policy.policy_ref for policy in policies)
        if len(policy_refs) != len(set(policy_refs)) or policy_refs != tuple(sorted(policy_refs)):
            raise PolicyBasisResolutionError("verified policy references must be unique and sorted")
        input_refs = _refs_in_inputs(parameters, facts)
        if input_refs != policy_refs:
            raise PolicyBasisResolutionError("accepted inputs and verified policy basis are incomplete")
        object.__setattr__(self, "parameter_bindings", MappingProxyType(_deep_freeze(parameters)))
        object.__setattr__(self, "invocation_facts", tuple(_deep_freeze(fact) for fact in facts))
        object.__setattr__(self, "verified_policies", policies)

    def runtime_parameter_bindings(self) -> dict[str, object]:
        return _thaw(self.parameter_bindings)  # type: ignore[return-value]

    def runtime_invocation_facts(self) -> list[dict[str, object]]:
        return _thaw(self.invocation_facts)  # type: ignore[return-value]


class PolicyBasisResolver:
    """Resolve exact policy evidence using only existing native owner ports."""

    def __init__(
        self,
        repository: RepositoryPort,
        access_control: AccessControlPort,
        applicability: ApplicabilityPort,
    ) -> None:
        self._repository = repository
        self._access_control = access_control
        self._applicability = applicability

    def resolve(
        self,
        campaign_id: str,
        selection: PolicySelection,
        *,
        catalog_context: BoundCatalogContext | None = None,
    ) -> ResolvedPolicyBasis:
        if not isinstance(selection, PolicySelection):
            raise PolicyBasisResolutionError("typed policy selection is required")
        campaign = self._pin_campaign(campaign_id)
        manifest = self._read(campaign, HOUSE_RULES_MANIFEST_PATH)
        sidecar = self._read(campaign, HOUSE_RULES_SIDECAR_PATH)
        source_path, policy = self._select_policy(manifest, sidecar, selection.policy_id)
        normative = self._read(campaign, source_path)
        if not isinstance(normative, str):
            raise PolicyBasisResolutionError("normative House-Rules source must be text")
        if not _normative_anchor_exists(normative, str(policy["source_anchor"])):
            raise PolicyBasisResolutionError("policy normative anchor is missing")

        principal = self._owner_result(
            self._access_control.resolve_principal(campaign),
            AuthenticatedPrincipalEvidence,
            "authenticated principal evidence",
        )
        creator = self._owner_result(
            self._access_control.resolve_creator(campaign),
            CreatorEvidence,
            "creator evidence",
        )
        player_value = self._access_control.resolve_active_player(campaign, principal)
        if player_value is not None and not isinstance(player_value, PlayerEvidence):
            raise PolicyBasisResolutionError("active PLAYER evidence must be owner-typed")
        adoption = self._owner_result(
            self._access_control.prove_policy_adoption(
                campaign, policy, principal, creator, player_value
            ),
            AdoptionEvidence,
            "policy adoption evidence",
        )
        self._validate_adoption(policy, adoption, player_value)

        applicable = self._owner_result(
            self._applicability.prove_policy_applicability(
                campaign, policy, selection.consumer_id
            ),
            ApplicabilityEvidence,
            "policy applicability evidence",
        )
        if applicable.policy_id != selection.policy_id or applicable.consumer_id != selection.consumer_id:
            raise PolicyBasisResolutionError("policy applicability evidence identity mismatch")

        realization_refs = _string_array(policy["realization_refs"], "realization_refs")
        realization_bindings = self._resolve_realizations(realization_refs, catalog_context)
        return ResolvedPolicyBasis(
            campaign_id=campaign.campaign_id,
            campaign_revision=campaign.revision,
            policy_id=selection.policy_id,
            policy_ref=_policy_ref(selection.policy_id, campaign.revision),
            consumer_id=selection.consumer_id,
            authority_class=str(policy["authority_class"]),
            adoption_basis=str(policy["adoption_basis"]),
            adopted_by_player_id=policy["adopted_by_player_id"],
            source_path=source_path,
            source_anchor=str(policy["source_anchor"]),
            realization_refs=tuple(sorted(realization_refs)),
            realization_bindings=realization_bindings,
            _verified=_VERIFIED_BASIS_SEAL,
        )

    def resolve_many(
        self,
        campaign_id: str,
        selections: Sequence[PolicySelection],
        *,
        catalog_context: BoundCatalogContext | None = None,
    ) -> tuple[ResolvedPolicyBasis, ...]:
        results = tuple(
            self.resolve(campaign_id, selection, catalog_context=catalog_context)
            for selection in selections
        )
        refs = tuple(result.policy_ref for result in results)
        if len(refs) != len(set(refs)):
            raise PolicyBasisResolutionError("policy basis references must be unique")
        return tuple(sorted(results, key=lambda result: result.policy_ref))

    @staticmethod
    def bind_accepted_basis(
        parameter_bindings: Mapping[str, object],
        invocation_facts: Sequence[Mapping[str, object]],
        verified_policies: Sequence[ResolvedPolicyBasis],
    ) -> AcceptedAdjudicationBasis:
        return AcceptedAdjudicationBasis(
            parameter_bindings=parameter_bindings,
            invocation_facts=tuple(invocation_facts),
            verified_policies=tuple(sorted(verified_policies, key=lambda policy: policy.policy_ref)),
        )

    def _pin_campaign(self, campaign_id: str) -> PinnedCampaign:
        if not isinstance(campaign_id, str) or not campaign_id:
            raise PolicyBasisResolutionError("selected campaign identity is required")
        pinned = self._repository.pin_campaign(campaign_id)
        if not isinstance(pinned, PinnedCampaign) or pinned.campaign_id != campaign_id:
            raise PolicyBasisResolutionError("repository did not return trusted exact campaign pin")
        return pinned

    def _read(self, campaign: PinnedCampaign, path: str) -> object:
        try:
            return self._repository.read_exact_path(campaign, path)
        except (AttributeError, KeyError, OSError, TypeError) as exc:
            raise PolicyBasisResolutionError(
                f"exact pinned campaign read failed for {path}"
            ) from exc

    @staticmethod
    def _select_policy(
        manifest_value: object, sidecar_value: object, policy_id: str
    ) -> tuple[str, Mapping[str, object]]:
        manifest = _mapping(manifest_value, "campaign manifest")
        rules = _mapping(manifest.get("rules"), "campaign manifest rules")
        source_path = _nonempty_string(rules.get("house_rules_path"), "manifest house_rules_path")
        if not _safe_relative_rules_path(source_path):
            raise PolicyBasisResolutionError("House-Rules source path is not an exact safe path")
        sidecar = _mapping(sidecar_value, "House-Rules sidecar")
        if set(sidecar) != {"schema_version", "source_path", "policies"}:
            raise PolicyBasisResolutionError("House-Rules sidecar has unexpected or missing fields")
        if sidecar["schema_version"] != 1:
            raise PolicyBasisResolutionError("unsupported House-Rules sidecar schema")
        sidecar_source_path = _nonempty_string(sidecar["source_path"], "sidecar source_path")
        if sidecar_source_path != source_path:
            raise PolicyBasisResolutionError("sidecar and manifest House-Rules paths differ")
        raw_policies = sidecar["policies"]
        if not isinstance(raw_policies, list):
            raise PolicyBasisResolutionError("House-Rules sidecar policies must be a list")
        policies: list[Mapping[str, object]] = []
        ids: set[str] = set()
        anchors: set[str] = set()
        expected_fields = {
            "policy_id",
            "kind",
            "authority_class",
            "lifecycle",
            "source_anchor",
            "routing_keys",
            "adoption_basis",
            "adopted_by_player_id",
            "supersedes_policy_ids",
            "realization_refs",
        }
        for raw_policy in raw_policies:
            policy = _mapping(raw_policy, "House-Rules policy")
            if set(policy) != expected_fields:
                raise PolicyBasisResolutionError("House-Rules policy has unexpected or missing fields")
            current_id = _native_id(policy["policy_id"], "policy_id")
            if _POLICY_ID_PATTERN.fullmatch(current_id) is None:
                raise PolicyBasisResolutionError("policy_id has invalid identity")
            if current_id in ids:
                raise PolicyBasisResolutionError("policy IDs must be unique")
            ids.add(current_id)
            anchor = _nonempty_string(policy["source_anchor"], "source_anchor")
            if anchor in anchors:
                raise PolicyBasisResolutionError("policy source anchors must be unique")
            anchors.add(anchor)
            if policy["kind"] not in {"house_rule", "ruling"}:
                raise PolicyBasisResolutionError("unsupported House-Rules policy kind")
            if policy["authority_class"] not in {"INTERPRETIVE_POLICY", "MECHANICAL_OVERRIDE_POLICY"}:
                raise PolicyBasisResolutionError("unsupported House-Rules authority class")
            if policy["lifecycle"] not in {"active", "superseded", "retired"}:
                raise PolicyBasisResolutionError("unsupported House-Rules lifecycle")
            _string_array(policy["routing_keys"], "routing_keys")
            _string_array(policy["supersedes_policy_ids"], "supersedes_policy_ids")
            _string_array(policy["realization_refs"], "realization_refs")
            adopted = policy["adopted_by_player_id"]
            if adopted is not None:
                _native_id(adopted, "adopted_by_player_id")
            policies.append(policy)
        matches = [
            policy
            for policy in policies
            if policy["policy_id"] == policy_id and policy["lifecycle"] == "active"
        ]
        if len(matches) != 1:
            raise PolicyBasisResolutionError("policy ID is not uniquely active")
        return source_path, matches[0]

    @staticmethod
    def _owner_result(value: object, expected_type: type[object], label: str):
        if not isinstance(value, expected_type):
            raise PolicyBasisResolutionError(f"{label} must be owner-typed evidence")
        return value

    @staticmethod
    def _validate_adoption(
        policy: Mapping[str, object], adoption: AdoptionEvidence, player: PlayerEvidence | None
    ) -> None:
        if adoption.authority_class != policy["authority_class"] or adoption.adoption_basis != policy["adoption_basis"]:
            raise PolicyBasisResolutionError("policy adoption evidence does not match sidecar")
        expected_player = policy["adopted_by_player_id"]
        if adoption.adopted_by_player_id != expected_player:
            raise PolicyBasisResolutionError("policy adopter attribution differs from sidecar")
        if adoption.adoption_basis == "active_player_interpretive":
            if player is None or adoption.adopted_by_player_id != player.player_id:
                raise PolicyBasisResolutionError("active PLAYER adoption evidence is missing")
        elif adoption.adoption_basis == "creator_delegated_mechanical_override":
            if player is None or not player.mechanical_override_policy:
                raise PolicyBasisResolutionError("mechanical override grant evidence is missing")

    @staticmethod
    def _resolve_realizations(
        realization_refs: Sequence[str], catalog_context: BoundCatalogContext | None
    ) -> tuple[Mapping[str, object], ...]:
        if not realization_refs:
            return ()
        if catalog_context is None or not catalog_context._is_admitted():
            raise PolicyBasisResolutionError("mechanically material policy requires admitted catalog context")
        bindings: list[Mapping[str, object]] = []
        for realization_ref in realization_refs:
            dependency = next(
                (
                    row
                    for row in catalog_context.definition_dependencies
                    if row.get("definition_id") == realization_ref
                ),
                None,
            )
            if dependency is None:
                raise PolicyBasisResolutionError("policy realization gap")
            try:
                binding = bind_interpreter_candidate(
                    catalog_context,
                    {"definition_id": realization_ref, "kind": dependency["kind"]},
                )
                validate_executable_binding(catalog_context, binding)
            except (CatalogBindingError, KeyError, TypeError) as exc:
                raise PolicyBasisResolutionError("policy realization gap") from exc
            bindings.append(MappingProxyType(deepcopy(binding)))
        return tuple(bindings)


def _safe_relative_rules_path(path: str) -> bool:
    parts = path.split("/")
    return (
        path.startswith("RULES/")
        and not path.startswith("/")
        and all(part not in {"", ".", "..", "latest"} for part in parts)
    )


def _normative_anchor_exists(normative: str, source_anchor: str) -> bool:
    anchor = source_anchor.strip()
    if not anchor.startswith("#"):
        return False
    expected = _slug(anchor.lstrip("#"))
    for line in normative.splitlines():
        match = _HEADING_PATTERN.match(line)
        if match is None:
            continue
        heading = match.group(1).rstrip("#").strip()
        if _slug(heading) == expected:
            return True
    return False


def _slug(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"<[^>]*>", "", value)
    value = re.sub(r"[^\w\- ]+", "", value, flags=re.UNICODE)
    return re.sub(r"[\s_]+", "-", value).strip("-")


def validate_frozen_adjudication_basis(
    parameter_bindings: object, invocation_facts: object
) -> tuple[dict[str, object], list[dict[str, object]], tuple[str, ...]]:
    """Validate persisted accepted inputs without consulting current policy/grants."""

    parameters = _validate_parameter_bindings(parameter_bindings)
    facts = _validate_invocation_facts(invocation_facts)
    return parameters, facts, _refs_in_inputs(parameters, facts)
