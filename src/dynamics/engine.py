"""Minimal deterministic neural-dynamics core for Testflysystem V0.1.

This module is deliberately independent of MaleCNS file formats. Biological graph
loading belongs in src/connectome. Dynamics parameters here are simulation
assumptions and must be recorded as such by experiments.
"""

from dataclasses import dataclass
from math import tanh
from typing import Dict, Iterable, List


@dataclass(frozen=True)
class Edge:
    source: int
    target: int
    weight: float


class NeuralDynamicsEngine:
    """Sparse leaky-rate recurrent network with synchronous fixed-dt updates."""

    def __init__(self, neuron_ids: Iterable[int], edges: Iterable[Edge], tau: float = 0.1):
        if tau <= 0:
            raise ValueError("tau must be positive")
        self.ids: List[int] = list(neuron_ids)
        self.index: Dict[int, int] = {nid: i for i, nid in enumerate(self.ids)}
        if len(self.index) != len(self.ids):
            raise ValueError("neuron IDs must be unique")
        self.tau = float(tau)
        self.activity = [0.0] * len(self.ids)
        self.external = [0.0] * len(self.ids)
        self.incoming: List[List[tuple[int, float]]] = [[] for _ in self.ids]
        for edge in edges:
            if edge.source not in self.index or edge.target not in self.index:
                raise ValueError("edge references neuron outside graph")
            self.incoming[self.index[edge.target]].append((self.index[edge.source], float(edge.weight)))

    def stimulate(self, neuron_id: int, value: float) -> None:
        self.external[self.index[neuron_id]] += float(value)

    def step(self, dt: float) -> None:
        """Advance one synchronous Euler step of tau*dx/dt=-x+tanh(Wx+I)."""
        if dt <= 0 or dt > self.tau:
            raise ValueError("V0.1 requires 0 < dt <= tau")
        previous = self.activity
        next_state = [0.0] * len(previous)
        alpha = dt / self.tau
        for i, old in enumerate(previous):
            drive = self.external[i]
            for source_i, weight in self.incoming[i]:
                drive += weight * previous[source_i]
            target = tanh(drive)
            next_state[i] = old + alpha * (-old + target)
        self.activity = next_state
        self.external = [0.0] * len(self.ids)

    def read_activity(self, neuron_id: int) -> float:
        return self.activity[self.index[neuron_id]]

    def read_population(self, neuron_ids: Iterable[int]) -> float:
        values = [self.read_activity(nid) for nid in neuron_ids]
        return sum(values) / len(values) if values else 0.0

    def reset(self) -> None:
        self.activity = [0.0] * len(self.ids)
        self.external = [0.0] * len(self.ids)

    def snapshot(self) -> Dict[int, float]:
        return dict(zip(self.ids, self.activity))
