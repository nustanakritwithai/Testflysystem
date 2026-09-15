"""MaleCNS v1.0 local Feather loader and validator.

Large source files live under data/raw and are never committed. This loader is
schema-tolerant on column spelling but fails loudly when required biological
identifiers or connection counts cannot be resolved.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Optional, Sequence

from .graph import Connection, ConnectomeGraph


class MaleCNSDataError(RuntimeError):
    pass


@dataclass(frozen=True)
class ResolvedColumns:
    source: str
    target: str
    weight: str


SOURCE_CANDIDATES = ("body_pre", "source", "pre", "pre_id", "bodyId_pre")
TARGET_CANDIDATES = ("body_post", "target", "post", "post_id", "bodyId_post")
WEIGHT_CANDIDATES = ("weight", "synapse_count", "count", "n", "roiInfo")
BODY_ID_CANDIDATES = ("bodyId", "body_id", "body", "root_id")


def _pick(columns: Sequence[str], candidates: Sequence[str], role: str) -> str:
    for name in candidates:
        if name in columns:
            return name
    raise MaleCNSDataError(f"cannot resolve {role}; columns={list(columns)}")


def resolve_connectivity_columns(columns: Sequence[str]) -> ResolvedColumns:
    return ResolvedColumns(
        source=_pick(columns, SOURCE_CANDIDATES, "presynaptic/source neuron ID"),
        target=_pick(columns, TARGET_CANDIDATES, "postsynaptic/target neuron ID"),
        weight=_pick(columns, WEIGHT_CANDIDATES, "connection/synapse count"),
    )


def _read_feather(path: Path):
    try:
        import pandas as pd
    except ImportError as exc:
        raise MaleCNSDataError("pandas and pyarrow are required to read MaleCNS Feather files") from exc
    if not path.exists():
        raise MaleCNSDataError(f"missing dataset file: {path}")
    try:
        return pd.read_feather(path)
    except Exception as exc:
        raise MaleCNSDataError(f"failed reading {path}: {exc}") from exc


def load_connectivity(path: str | Path, min_synapses: int = 1) -> ConnectomeGraph:
    """Load neuron-to-neuron connectivity while preserving MaleCNS body IDs."""
    if min_synapses < 1:
        raise ValueError("min_synapses must be >= 1")
    frame = _read_feather(Path(path))
    cols = resolve_connectivity_columns(list(frame.columns))
    edges = []
    for source, target, count in frame[[cols.source, cols.target, cols.weight]].itertuples(index=False, name=None):
        try:
            source_i, target_i, count_i = int(source), int(target), int(count)
        except (TypeError, ValueError) as exc:
            raise MaleCNSDataError(f"invalid connectivity row: {(source, target, count)}") from exc
        if source_i == target_i:
            # Autapses are retained: they can matter to recurrent dynamics.
            pass
        if count_i < min_synapses:
            continue
        edges.append(Connection(source_i, target_i, count_i, provenance="MEASURED"))
    if not edges:
        raise MaleCNSDataError("connectivity file produced zero edges")
    return ConnectomeGraph(edges)


def load_annotations(path: str | Path):
    frame = _read_feather(Path(path))
    body_col = _pick(list(frame.columns), BODY_ID_CANDIDATES, "annotation body ID")
    if frame[body_col].isna().any():
        raise MaleCNSDataError("annotation table contains null body IDs")
    if frame[body_col].duplicated().any():
        raise MaleCNSDataError("annotation table contains duplicate body IDs")
    return frame, body_col


def load_neurotransmitters(path: str | Path):
    frame = _read_feather(Path(path))
    body_col = _pick(list(frame.columns), BODY_ID_CANDIDATES, "neurotransmitter body ID")
    return frame, body_col


def validate_cross_references(graph: ConnectomeGraph, annotation_ids: Iterable[int]) -> Mapping[str, int]:
    annotated = {int(x) for x in annotation_ids}
    graph_ids = set(graph.neurons)
    return {
        "graph_neurons": len(graph_ids),
        "annotated_neurons": len(annotated),
        "graph_without_annotation": len(graph_ids - annotated),
        "annotations_outside_graph": len(annotated - graph_ids),
    }
