from __future__ import annotations
import os
import networkx as nx


def fetch_connectome_subgraph(neuron_type_regex: str = "DN.*") -> nx.DiGraph:
    """Fetch a small MaleCNS subgraph. Requires NEUPRINT_TOKEN and network access."""
    from neuprint import Client, NeuronCriteria as NC, fetch_adjacencies, fetch_neurons
    token = os.environ.get("NEUPRINT_TOKEN")
    if not token:
        raise RuntimeError("Set NEUPRINT_TOKEN before querying neuPrint")
    Client("https://neuprint.janelia.org", dataset="male-cns:v1.0", token=token)
    neurons, _ = fetch_neurons(NC(type=neuron_type_regex, regex=True))
    if neurons.empty:
        raise RuntimeError(f"No neurons matched {neuron_type_regex!r}")
    _, connections = fetch_adjacencies(None, NC(bodyId=int(neurons.iloc[0].bodyId)))
    graph = nx.DiGraph()
    for row in connections.itertuples():
        graph.add_edge(int(row.bodyId_pre), int(row.bodyId_post), weight=float(row.weight))
    return graph
