#!/usr/bin/env python3
"""Extract a traceable MaleCNS circuit around one or more seed body IDs."""

import argparse
import json
from pathlib import Path

from src.connectome.malecns_loader import load_connectivity


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--connectivity", required=True, type=Path)
    p.add_argument("--seed", required=True, type=int, nargs="+")
    p.add_argument("--depth", type=int, default=2)
    p.add_argument("--min-synapses", type=int, default=5)
    p.add_argument("--direction", choices=("forward", "backward", "both"), default="both")
    p.add_argument("--output", type=Path, default=Path("data/processed/subgraph.json"))
    args = p.parse_args()

    graph = load_connectivity(args.connectivity, min_synapses=args.min_synapses)
    selected = set(args.seed)
    for seed in args.seed:
        if args.direction in ("forward", "both"):
            selected |= graph.trace_forward(seed, args.depth, args.min_synapses)
        if args.direction in ("backward", "both"):
            selected |= graph.trace_backward(seed, args.depth, args.min_synapses)

    edges = []
    for source in selected:
        for edge in graph.get_outputs(source):
            if edge.target in selected and edge.synapse_count >= args.min_synapses:
                edges.append({
                    "source": edge.source,
                    "target": edge.target,
                    "synapse_count": edge.synapse_count,
                    "provenance": edge.provenance,
                })

    result = {
        "source_dataset": "male-cns:v1.0",
        "seed_body_ids": args.seed,
        "depth": args.depth,
        "direction": args.direction,
        "min_synapses": args.min_synapses,
        "neurons": sorted(selected),
        "edges": edges,
        "counts": {"neurons": len(selected), "edges": len(edges)},
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result["counts"], indent=2))


if __name__ == "__main__":
    main()
