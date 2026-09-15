# Circuit 001 — Vision → Descending → VNC/Motor

Status: **DATA-BOUND / implementation started**

## Objective

Extract the first evidence-traceable sensorimotor circuit from MaleCNS v1.0 and run it through the Testflysystem dynamics engine without a hard-coded stimulus→action rule.

## Biological starting point

The MaleCNS release includes the full neuron-to-neuron connection graph, annotations and predicted neurotransmitters. Published/official exploration resources identify DNp01 (giant-fiber pathway) as a useful descending-neuron landmark and report strong visual inputs including LC4/LPLC2-associated pathways. These names are starting hypotheses for dataset queries, not hard-coded circuit membership.

## Extraction protocol

1. Download official v1.0 flat-connectome tables with `python scripts/download_data.py`.
2. Validate/checksum them with `scripts/inspect_dataset.py`.
3. Search the annotation table for candidate visual sensory/visual projection populations and descending neurons.
4. Preserve MaleCNS body IDs and all measured synapse counts.
5. Trace candidate paths forward from visual populations and backward from descending/VNC targets.
6. Intersect/score paths by connection evidence; do not insert missing biological edges.
7. Export the selected circuit as JSON with provenance per node/edge.
8. Convert measured synapse counts to *inferred simulation weights* in a separate transformation step.
9. Run deterministic stimulation experiments and compare left/right or target motor-population activity.

## Pass criteria

Circuit 001 passes only if:

- every biological node/edge maps to a source MaleCNS ID;
- measured connectivity is never relabeled as measured neural activity;
- stimulus reaches downstream populations through graph dynamics;
- no `if visual stimulus: execute action` behavior rule exists;
- the experiment records dataset checksums, extraction threshold, dynamics parameters and random seed (if any).

## Current blocker

The repository intentionally does not store the ~1.1 GB source connectome. The downloader is now present, but an execution environment must run it once to populate `data/raw/`. After that, the existing loader/extractor can operate on the real graph.
