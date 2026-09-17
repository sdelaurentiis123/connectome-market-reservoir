# Connectome Market Reservoir

Research scaffold for testing a fixed *Drosophila* connectome subgraph as a recurrent reservoir for market regime and volatility prediction.

This is a research project, **not a trading system or financial advice**. The honest question is whether evolved graph topology offers useful memory or nonlinear separation relative to matched random reservoirs. It is not "a fly brain that trades."

## Targets

Prefer targets with a defensible signal-to-noise ratio:

- future realized-volatility bucket
- volatility-spike probability
- market/regime classification
- liquidity or spread stress

Raw next-tick price direction is not the primary target.

## Method

1. Query a tractable MaleCNS subgraph from `male-cns:v1.0`.
2. Feed standardized returns, realized volatility, volume, spread, and order-book imbalance into fixed input nodes.
3. Propagate state using explicit leaky nonlinear dynamics.
4. Train only a regularized linear/logistic readout.
5. Compare against degree-preserving rewires, Erdős-Rényi graphs, matched echo-state networks, logistic regression, gradient boosting, and a small recurrent baseline.

## Guardrails

- strict chronological walk-forward evaluation
- purge/embargo samples whose labels overlap the training window
- fit scalers and hyperparameters on training data only
- freeze graph, edge-sign assumptions, and hyperparameters before final test
- include fees, spread, slippage, latency, turnover, and capacity in any strategy simulation
- report calibration, AUROC/AUPRC, drawdown, turnover, and stability across regimes
- never infer an edge from one favorable backtest

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pytest
python demo.py
```

Set `NEUPRINT_TOKEN` only when querying neuPrint. Market data is not bundled; loaders require an explicit local file or adapter.

## Status

Cold-start scaffold. The included demo is synthetic and runnable. It proves plumbing only, not market efficacy.

## Data credit

Male CNS data: FlyEM at HHMI Janelia, Cambridge Connectomics Group, Google Research, and collaborators. See https://male-cns.janelia.org/ and follow dataset citation/license terms.

## License

MIT for repository code. External datasets retain their own terms.

## Backtesting and paper execution

Backtesting is core, not a demo afterthought. The intended harness must support:

- event-driven, timestamp-ordered simulation without look-ahead
- walk-forward retraining and purged/embargoed validation
- configurable spread, fees, slippage, latency, partial fills, and position limits
- position, cash, equity, realized/unrealized PnL, turnover, drawdown, and exposure logs
- graph/null-model sweeps with frozen final-test configuration
- reproducible run manifests and seeds

`PaperBroker` provides a runnable long/flat simulated execution loop. An Alpaca paper adapter is a documented future path; no live-money adapter belongs here until the model has repeated out-of-sample evidence and a separately reviewed risk layer.

### Prediction markets

The same reservoir can ingest Polymarket or Kalshi contract series: implied probability, bid/ask spread, depth, volume, time-to-expiry, and correlated-contract features. Targets can be probability calibration, regime shifts, or bounded paper-trading policies on binary event contracts. Historical snapshots must be timestamp-aligned and evaluated without using resolution information before it became public.
