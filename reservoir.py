from __future__ import annotations
import networkx as nx
import numpy as np


def normalized_adjacency(graph: nx.DiGraph, nodes: list[int]) -> np.ndarray:
    a = nx.to_numpy_array(graph, nodelist=nodes, weight="weight", dtype=float).T
    radius = max(abs(np.linalg.eigvals(a)), default=0.0)
    return a if radius == 0 else a / float(radius)


def run_reservoir(adjacency: np.ndarray, inputs: np.ndarray, input_weights: np.ndarray,
                  leak: float = 0.25, spectral_scale: float = 0.9) -> np.ndarray:
    state = np.zeros(adjacency.shape[0], dtype=float)
    states = []
    for sample in np.atleast_2d(inputs):
        proposal = np.tanh(spectral_scale * adjacency @ state + input_weights @ sample)
        state = (1.0 - leak) * state + leak * proposal
        states.append(state.copy())
    return np.asarray(states)
