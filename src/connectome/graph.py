"""Executable sparse connectome representation preserving MaleCNS source IDs."""

from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Set


@dataclass(frozen=True)
class Connection:
    source: int
    target: int
    synapse_count: int
    provenance: str = "MEASURED"


class ConnectomeGraph:
    def __init__(self, connections: Iterable[Connection]):
        self.outgoing: Dict[int, List[Connection]] = defaultdict(list)
        self.incoming: Dict[int, List[Connection]] = defaultdict(list)
        self.neurons: Set[int] = set()
        for edge in connections:
            if edge.synapse_count < 0:
                raise ValueError("synapse_count cannot be negative")
            self.neurons.update((edge.source, edge.target))
            self.outgoing[edge.source].append(edge)
            self.incoming[edge.target].append(edge)

    def get_inputs(self, neuron_id: int) -> List[Connection]:
        return list(self.incoming.get(neuron_id, ()))

    def get_outputs(self, neuron_id: int) -> List[Connection]:
        return list(self.outgoing.get(neuron_id, ()))

    def trace_forward(self, start: int, depth: int = 1, min_synapses: int = 1) -> Set[int]:
        return self._trace(start, depth, min_synapses, forward=True)

    def trace_backward(self, start: int, depth: int = 1, min_synapses: int = 1) -> Set[int]:
        return self._trace(start, depth, min_synapses, forward=False)

    def _trace(self, start: int, depth: int, min_synapses: int, forward: bool) -> Set[int]:
        if depth < 0:
            raise ValueError("depth cannot be negative")
        seen = {start}
        queue = deque([(start, 0)])
        adjacency = self.outgoing if forward else self.incoming
        while queue:
            node, level = queue.popleft()
            if level >= depth:
                continue
            for edge in adjacency.get(node, ()):
                if edge.synapse_count < min_synapses:
                    continue
                nxt = edge.target if forward else edge.source
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, level + 1))
        return seen

    def shortest_path(self, source: int, target: int, min_synapses: int = 1) -> Optional[List[int]]:
        queue = deque([source])
        parent = {source: None}
        while queue:
            node = queue.popleft()
            if node == target:
                path = []
                while node is not None:
                    path.append(node)
                    node = parent[node]
                return list(reversed(path))
            for edge in self.outgoing.get(node, ()):
                if edge.synapse_count < min_synapses or edge.target in parent:
                    continue
                parent[edge.target] = node
                queue.append(edge.target)
        return None
