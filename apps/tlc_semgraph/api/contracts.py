from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, TypedDict


SafetyDomainId = Literal["epistemic", "human", "cognitive", "empirical"]
ImpactRisk = Literal["low", "medium", "high", "constitutional"]
DriftSeverity = Literal["none", "advisory", "review_required", "halt"]


class UnitRef(TypedDict, total=False):
    id: str
    kind: str
    path: str
    symbol: str


class DiffRef(TypedDict):
    base: str
    head: str


class ImpactReport(TypedDict):
    report_version: str
    diff: DiffRef
    direct_units: list[UnitRef]
    ripple_units: list[UnitRef]
    clusters_touched: list[str]
    domains_touched: list[SafetyDomainId]
    risk: ImpactRisk
    gaps: list[str]
    evidence_uri: str


class CrossDomainEdge(TypedDict):
    from_domain: SafetyDomainId
    to_domain: SafetyDomainId
    edge_kind: str
    count: int


class ShadowDrift(TypedDict):
    report_version: str
    snapshot_sha: str
    policy_sha: str
    unbound_clusters: list[str]
    orphan_units: list[str]
    cross_domain_edges: list[CrossDomainEdge]
    severity: DriftSeverity


@dataclass(frozen=True)
class SchemaPaths:
    impact_report: str = "verification/semgraph/ImpactReport.schema.json"
    shadow_drift: str = "verification/semgraph/ShadowDrift.schema.json"

