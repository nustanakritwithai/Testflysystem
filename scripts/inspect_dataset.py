#!/usr/bin/env python3
"""Inspect local MaleCNS files and emit a reproducible validation report."""

import argparse
import hashlib
import json
from pathlib import Path

from src.connectome.malecns_loader import (
    load_annotations,
    load_connectivity,
    load_neurotransmitters,
    validate_cross_references,
)


def sha256(path: Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def file_info(path: Path) -> dict:
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha256(path)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connectivity", required=True, type=Path)
    parser.add_argument("--annotations", required=True, type=Path)
    parser.add_argument("--neurotransmitters", type=Path)
    parser.add_argument("--min-synapses", type=int, default=1)
    parser.add_argument("--output", type=Path, default=Path("data/processed/validation_report.json"))
    args = parser.parse_args()

    graph = load_connectivity(args.connectivity, min_synapses=args.min_synapses)
    annotations, body_col = load_annotations(args.annotations)
    report = {
        "connectivity": file_info(args.connectivity),
        "annotations": file_info(args.annotations),
        "min_synapses": args.min_synapses,
        "cross_reference": validate_cross_references(graph, annotations[body_col]),
        "edge_count": sum(len(v) for v in graph.outgoing.values()),
    }
    if args.neurotransmitters:
        nt, nt_body_col = load_neurotransmitters(args.neurotransmitters)
        report["neurotransmitters"] = file_info(args.neurotransmitters)
        report["neurotransmitter_rows"] = len(nt)
        report["neurotransmitter_unique_bodies"] = int(nt[nt_body_col].nunique())

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
