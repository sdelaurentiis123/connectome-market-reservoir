import networkx as nx
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from reservoir import normalized_adjacency, run_reservoir


def main() -> None:
    rng = np.random.default_rng(11)
    graph = nx.gn_graph(64, seed=11).reverse(copy=True)
    nx.set_edge_attributes(graph, 1.0, "weight")
    nodes = list(graph.nodes)
    adjacency = normalized_adjacency(graph, nodes)
    regime = np.repeat([0, 1, 0, 1], 250)
    returns = rng.normal(scale=np.where(regime == 1, 2.0, 0.6))
    features = np.column_stack([returns, np.abs(returns)])
    weights = rng.normal(scale=0.15, size=(len(nodes), features.shape[1]))
    states = run_reservoir(adjacency, features, weights)
    split = 750
    model = LogisticRegression(max_iter=1000).fit(states[:split], regime[:split])
    auc = roc_auc_score(regime[split:], model.predict_proba(states[split:])[:, 1])
    print(f"synthetic held-out regime AUROC: {auc:.3f}")

if __name__ == "__main__":
    main()
