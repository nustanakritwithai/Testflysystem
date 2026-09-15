# Scientific Rules

## Core rule

Testflysystem must preserve the boundary between biological evidence and simulation assumptions.

## Provenance classes

| Class | Meaning |
|---|---|
| MEASURED | Direct observation in source dataset |
| ANNOTATED | Dataset/expert annotation |
| PREDICTED | Biological property predicted by a model |
| INFERRED | Computed from source evidence |
| ASSUMED | Unknown parameter chosen for simulation |
| EXPERIMENTAL | New mechanism being tested |

## Example

```text
connection      MEASURED
synapse_count   MEASURED
cell_type       ANNOTATED
transmitter     PREDICTED
dynamic_weight  INFERRED
time_constant   ASSUMED
transfer_model  EXPERIMENTAL
```

## Prohibited scientific shortcuts

1. Do not call connectivity a functioning brain.
2. Do not claim a simulated state is measured neural activity unless activity data actually supports it.
3. Do not describe emergent intelligence merely because a graph is large.
4. Do not hide explicit behavior rules in sensory or motor adapters and attribute the resulting behavior to neural dynamics.
5. Preserve source IDs when creating subgraphs so every biological edge can be traced back to the source dataset.
6. Record dataset version, transformation, thresholds, normalization and random seed for every experiment.

## V0.1 falsifiable hypothesis

A MaleCNS-derived subgraph supplied with explicitly documented dynamical assumptions can transform sensory stimulation into differentiated continuous motor-population activity without an explicit stimulus-to-action decision rule.

Failure is valid. If the network is unstable, silent, insensitive, or requires extensive behavior-specific engineering, record that result rather than redefining success.
