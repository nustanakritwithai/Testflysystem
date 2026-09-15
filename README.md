# Testflysystem — MaleCNS Neural Dynamics Laboratory

Science-first experimental system for turning measured Drosophila MaleCNS connectivity into an executable neural graph and testing closed-loop sensorimotor dynamics.

## V0.1 target

**MaleCNS-derived executable neural system capable of producing closed-loop sensorimotor behavior through neural dynamics.**

Pipeline:

`MaleCNS → Data validation → Executable connectome → Neural dynamics → Sensory stimulation → Descending/VNC populations → Motor decoder → Virtual fly → Environment feedback`

V0.1 deliberately excludes LLMs, planners, symbolic world models, behavior trees, and high-level agent memory. The goal is to measure what behavior can arise from neural dynamics without hiding engineered decisions inside the controller.

## Scientific provenance

Every biological or modeled property must carry a provenance class:

- `MEASURED` — directly present in source data.
- `ANNOTATED` — expert/dataset annotation.
- `PREDICTED` — model-derived biological annotation such as transmitter prediction.
- `INFERRED` — derived computationally from measured/predicted data.
- `ASSUMED` — parameter not established by the dataset.
- `EXPERIMENTAL` — mechanism introduced specifically for a simulation experiment.

A measured connectome is **not** equivalent to measured neural dynamics. Unknown time constants, transfer functions, effective synaptic strengths, neuromodulation, sensory encoding and motor decoding must not be presented as measured facts.

## Roadmap

- P0 — scientific rules + repository scaffold
- P1 — MaleCNS data ingestion and validation
- P2 — executable graph + path tracing
- P3 — functional circuit maps
- P4 — Neural Dynamics Engine V0.1
- P5 — subgraph stability/performance experiments
- P6 — sensory encoder
- P7 — motor population decoder
- P8 — first closed neural loop
- P9 — neural-state analysis/visualization
- P10 — plasticity experiments
- P11 — cognition-oriented experiments

## Data policy

Large MaleCNS datasets are not committed to Git. Place downloaded source files under `data/raw/`; derived local artifacts go under `data/processed/`. Both are ignored. `data/manifest.json` records dataset identity and expected local roles.

## First pass

The initial implementation should prove four things before scaling:

1. Dataset rows can be validated and normalized.
2. A real subgraph can be extracted and traced forward/backward.
3. A deterministic leaky-rate dynamics engine can run on that graph.
4. Sensory stimulation can alter motor-population output through graph dynamics rather than an explicit `if stimulus -> action` rule.
