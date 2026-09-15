from src.connectome.graph import Connection, ConnectomeGraph
from src.dynamics.engine import Edge, NeuralDynamicsEngine


def test_graph_trace_and_path():
    graph = ConnectomeGraph([
        Connection(1, 2, 10),
        Connection(2, 3, 8),
        Connection(1, 4, 1),
    ])
    assert graph.trace_forward(1, depth=2, min_synapses=2) == {1, 2, 3}
    assert graph.trace_backward(3, depth=2) == {1, 2, 3}
    assert graph.shortest_path(1, 3) == [1, 2, 3]


def test_dynamics_propagates_without_action_rule():
    engine = NeuralDynamicsEngine(
        neuron_ids=[1, 2, 3],
        edges=[Edge(1, 2, 1.0), Edge(2, 3, 1.0)],
        tau=0.1,
    )
    engine.stimulate(1, 1.0)
    for _ in range(8):
        engine.step(0.02)
    assert engine.read_activity(1) > 0
    assert engine.read_activity(2) > 0
    assert engine.read_activity(3) > 0


def test_reset():
    engine = NeuralDynamicsEngine([1], [], tau=0.1)
    engine.stimulate(1, 1.0)
    engine.step(0.02)
    engine.reset()
    assert engine.snapshot() == {1: 0.0}
